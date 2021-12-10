/**
 * 
 * @todo
 *  - move strings to flash (less RAM consumption)
 *  - fix deprecated convertation form string to char* startAsAnchor
 *  - give example description
 *  
 */

#define USE_USBCON
#include <ros.h>
#include <SPI.h>
#include "DW1000Ranging.h"
#include <ros/time.h>
#include <localization/TimestampDistance.h>

// connection pins
const uint8_t PIN_RST = 4; // reset pin
const uint8_t PIN_IRQ = 7; // irq pin
const uint8_t PIN_SS = 3; // spi select pin


//ros variables
ros::NodeHandle nh;
localization::TimestampDistance distance_msg;
ros::Publisher range_pub("distance_3", &distance_msg);

void setup() {
  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.advertise(range_pub);
  //init the configuration
  DW1000Ranging.initCommunication(PIN_RST, PIN_SS, PIN_IRQ); //Reset, CS, IRQ pin
  //define the sketch as anchor. It will be great to dynamically change the type of module
  DW1000Ranging.attachNewRange(newRange);
  DW1000Ranging.attachBlinkDevice(newBlink);
  DW1000Ranging.attachInactiveDevice(inactiveDevice);
  byte id[2] = {1, 1};
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
  distance_msg.distance = DW1000Ranging.getDistantDevice()->getRange();
  distance_msg.header.stamp = nh.now();
  range_pub.publish(&distance_msg);
  nh.spinOnce();
  delay(3);
//  int timE = (DW1000Ranging.getDistantDevice()->timeRangeReceived.getAsMicroSeconds())/(1000);
//  Serial.print("\t from: "); Serial.print(DW1000Ranging.getDistantDevice()->getShortAddress(), HEX);
//  Serial.print("\t Range: "); Serial.print(range); Serial.print(" m");
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
