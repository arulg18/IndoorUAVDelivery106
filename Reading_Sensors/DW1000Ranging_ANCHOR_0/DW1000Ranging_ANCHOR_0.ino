/**

   @todo
    - move strings to flash (less RAM consumption)
    - fix deprecated convertation form string to char* startAsAnchor
    - give example description

*/

#define USE_USBCON
#include <ros.h>
#include <SPI.h>
#include "DW1000Ranging.h"
#include <ros/time.h>
#include <delivery/TimestampDistance.h>

// connection pins
const uint8_t PIN_RST = 4; // reset pin
const uint8_t PIN_IRQ = 7; // irq pin
const uint8_t PIN_SS = 3; // spi select pin

// float arr[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
// int count = 0;
// float average = 0;


// median
#define N (5)
struct cir {
    float a[N];
    unsigned h;
    unsigned t;
    unsigned n;
};
typedef volatile struct cir cir_t;

cir_t *cir_new() {
    cir_t *cir = malloc(sizeof(*cir));
    cir->h = 0;
    cir->t = N - 1;
    cir->n = N;
    return cir;
}


// if adding 1 to tail == head, then there is nothing
float cir_empty(cir_t *cir) {
    return (cir->t + 1) % N == cir->h;
}

// if adding 1 to head = tail, then we have no space.
float cir_full(cir_t *cir) {
    return cir->h == cir->t;
}

void cir_enqueue(cir_t *cir, float x) {
    if (cir_full(cir)) cir->t = (cir->t + 1) % N;
    cir->a[cir->h] = x;
    cir->h = (cir->h + 1) % N;
}


int compare(const void *x, const void * y) {
    float ix = *(float*)x;
    float iy = *(float*)y;
    return (int)(ix - iy);
}

float cir_median(cir_t *cir) {
    float q[cir->n];
    int qcount = 0;
    // Populate the array
    if(cir_empty(cir)) return 0;
    else if(cir_full(cir)) {
        qcount = cir->n;
        for(int i = 0; i < cir->n; i++) {
            q[i] = cir->a[i];
        }
    } else if(cir->t > cir->h) {
        for(int i = 0; i < cir->h; i++) {
            q[qcount] = cir->a[i];
            qcount++;
        }
        for(int i = cir->t; i < cir->n - 1; i++) {
            q[qcount] = cir->a[i];
            qcount++;
        }
    } else {
        for(int i = cir->t; i < cir->h; i++) {
            q[qcount] = cir->a[i];
            qcount++;
        }
    }
    // Sort the array
    qsort(q, qcount, sizeof(float), compare);
    return q[qcount/2];
}

cir_t *cir1 = cir_new();


//ros variables
ros::NodeHandle nh;
delivery::TimestampDistance distance_msg;
ros::Publisher range_pub("distance_0", &distance_msg);

void setup() {
  Serial.begin(115200);
  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.advertise(range_pub);
  //init the configuration
  DW1000Ranging.initCommunication(PIN_RST, PIN_SS, PIN_IRQ); //Reset, CS, IRQ pin
  //define the sketch as anchor. It will be great to dynamically change the type of module
  DW1000Ranging.attachNewRange(newRange);
  DW1000Ranging.attachBlinkDevice(newBlink);
  DW1000Ranging.attachInactiveDevice(inactiveDevice);
  byte id[2] = {0, 0};
  //Enable the filter to smooth the distance
  //  DW1000Ranging.useRangeFilter(true);
  //we start the module as an anchor
  DW1000Ranging.startAsAnchor("82:17:5B:D5:A9:9A:E2:9C", id, DW1000.MODE_LONGDATA_RANGE_LOWPOWER);

}

void loop() {
  DW1000Ranging.loop();
  //  Serial.print(distance_msg.header.stamp);
  //  Serial.print('\t');
  //  Serial.println(distance_msg.distance);
  //  newRange();
}

void newRange() {

  float dist = DW1000Ranging.getDistantDevice()->getRange();
  cir_enqueue(cir1,dist);
  distance_msg.distance = cir_median(cir1);

  distance_msg.header.stamp = nh.now();
  range_pub.publish(&distance_msg);
  nh.spinOnce();
  delay(3);
  //  int timE = (DW1000Ranging.getDistantDevice()->timeRangeReceived.getAsMicroSeconds())/(1000);
  //  Serial.print("\t from: "); Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
//  Serial.println(dist); 
//  Serial.print('\t'); 
//  Serial.println(average); 
//  Serial.println(" m");
  //  Serial.print("\t RX power: "); Serial.print(DW1000Ranging.getDistantDevice()->getRXPower()); Serial.println(" dBm");
  //  Serial.print("\t Time Stamp: "); Serial.print(time); Serial.println(" ms");



  //  int time = DW1000Ranging.getDistantDevice()->timeRangeReceived.getAsMicroSeconds();
}

void newBlink(DW1000Device* device) {
  //  Serial.print("blink; 1 device added ! -> ");
  //  Serial.print(" short:");
  //  Serial.println(device->getShortAddress(), HEX);
}

void inactiveDevice(DW1000Device* device) {
  //  Serial.print("delete inactive device: ");
  //  Serial.println(device->getShortAddress(), HEX);
}
