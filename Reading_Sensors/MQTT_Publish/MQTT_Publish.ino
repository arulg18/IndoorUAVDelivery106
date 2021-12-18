#include <WiFi.h>
#include <PubSubClient.h>
#include <ros.h>

#include <ros/time.h>
#include <geometry_msgs/Point.h>
#include <std_msgs/String.h>



WiFiClient wifiClient;
PubSubClient mqttClient(wifiClient);

char* ssid = "NETGEAR17";
char* password = "noisycartoon636";
const char* data;
int test_data =47;
char *mqttServer = "broker.hivemq.com";
int mqttPort = 1883;
ros::NodeHandle nh;
geometry_msgs::Point goal_pos_msg;


ros::Publisher pub_pos("Start_positions", &goal_pos_msg);
//ros::Subscriber<std_msgs::String> sub("Is-Done_Topic", &messageCb);
void msgcallback(const std_msgs::String &msg)
{
 data = msg.data;

}

ros::Subscriber<std_msgs::String> sub("Is_Reached_Dest", &msgcallback);


void setupMQTT() {
  mqttClient.setServer(mqttServer, mqttPort);
  mqttClient.setCallback(callback);
}

void reconnect() {
  Serial.println("Connecting to MQTT Broker...");
  while (!mqttClient.connected()) {
      Serial.println("Reconnecting to MQTT Broker..");
      String clientId = "ESP32Client-";
      clientId += String(random(0xffff), HEX);
     
      if (mqttClient.connect(clientId.c_str())) {
        Serial.println("Connected.");
        // subscribe to topic
        mqttClient.subscribe("esp32/x_output");
        mqttClient.subscribe("esp32/y_output");
      }      
  }
}

void setup() {
  Serial.begin(115200);

  Serial.print("Start Print");
  WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print("Excuse me ");
    }
    Serial.println("");
     Serial.println("Connected to Wi-Fi");


  setupMQTT();
  nh.initNode();
  nh.advertise(pub_pos);
}


void loop() {
  if (!mqttClient.connected())
    reconnect();
  mqttClient.loop();
  long now = millis();
  long previous_time = 0;
 
  if (now - previous_time > 1000) {
    previous_time = now;
   
   
    //Serial.print("/t test data: ");
    mqttClient.publish("esp32/test_data",data);
    nh.spinOnce();
    //Serial.print("esp32/X_data");
    //Serial.print("/t y data: ");
   
    //Serial.print(esp32/Y_data);
   
  }
}

 

  void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
 
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Feel free to add more if statements to control more GPIOs with MQTT

  // If a message is received on the topic esp32/output, you check if the message is either "on" or "off".
  // Changes the output state according to the message
  if (String(topic) == "esp32/xy_output") {
    Serial.print("Changing XY destination to ");//should be of form x y
    Serial.print(messageTemp);
    goal_pos_msg.x = (char)messageTemp[0] - '0';
    goal_pos_msg.y = (char)messageTemp[2] - '0';
    pub_pos.publish(&goal_pos_msg);
    nh.spinOnce();
  }


}
