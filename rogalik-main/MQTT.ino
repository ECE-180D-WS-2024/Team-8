#include <WiFi.h>
#include <PubSubClient.h>
#include "ICM_20948.h" // Click here to get the library:http://librarymanager/All#SparkFun_ICM_20948_IMU
//#define USE_SPI // Uncomment this to use SPI
#define SERIAL_PORT Serial
#define SPI_PORT SPI // Your desired SPI port. Used only when "USE_SPI" is defined
#define CS_PIN 2 // Which pin you connect CS to. Used only when "USE_SPI" is defined
#define WIRE_PORT Wire // Your desired Wire port. Used when "USE_SPI" is not defined
// The value of the last bit of the I2C address.
// On the SparkFun 9DoF IMU breakout the default is 1, and when the ADR jumper is closed the value becomes 0
#define AD0_VAL 1

#ifdef USE_SPI
ICM_20948_SPI myICM; // If using SPI create an ICM_20948_SPI object
#else
ICM_20948_I2C myICM; // Otherwise create an ICM_20948_I2C object
#endif

// WiFi
const char *ssid = "Eugenephone"; // Enter your WiFi name
const char *password = "yortyort"; // Enter WiFi password

// MQTT Broker
const char *mqtt_broker = "mqtt.eclipseprojects.io";
const char *topic = "lol123";
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

float prev_gyr_Z = 0;
float angular_position = 0;
long int t1 = 0;
long int t2 = 0; 
int sector = 0; 
int prev_sector = 0;

void setup() {
 // Set software serial baud to 115200;
 Serial.begin(115200);
 // connecting to a WiFi network
 WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
 }
 Serial.println("Connected to the WiFi network");
 //connecting to a mqtt broker
 client.setServer(mqtt_broker, mqtt_port);
 client.setCallback(callback);
 
 while (!client.connected()) {
   String client_id = "esp32-client-";
   client_id += String(WiFi.macAddress());
   Serial.printf("The client %s connects to the public mqtt broker\n", client_id.c_str());
   if (client.connect(client_id.c_str())) { //, mqtt_username, mqtt_password)) {
     Serial.println("mqtt broker connected");
   }else {
     Serial.print("failed with state ");
     Serial.print(client.state());
     delay(2000);
   }
 }
 // publish and subscribe
 client.publish(topic, "Hi I’m ESP32 ^^");
 client.subscribe(topic);
 #ifdef USE_SPI
 SPI_PORT.begin();
 #else
 WIRE_PORT.begin();
 WIRE_PORT.setClock(400000);
 #endif

 bool initialized = false;
 while (!initialized) {
   #ifdef USE_SPI
   myICM.begin(CS_PIN, SPI_PORT);
   #else
   myICM.begin(WIRE_PORT, AD0_VAL);
   #endif
  
   SERIAL_PORT.print(F("Initialization of the sensor returned: "));
   SERIAL_PORT.println(myICM.statusString());
   if (myICM.status != ICM_20948_Stat_Ok) {
     SERIAL_PORT.println("Trying again...");
     delay(500);
   } else {
     initialized = true;
  
   }
 }
}

void callback(char *topic, byte *payload, unsigned int length) {
   Serial.print("Message arrived in topic: ");
   Serial.println(topic);
   Serial.print("Message:");
   for (int i = 0; i < length; i++) {
      Serial.print((char) payload[i]);
   }
   Serial.println();
   Serial.println("-----------------------");
}

void loop()
{

   if (myICM.dataReady())
   {
     t1 = t2;
     myICM.getAGMT(); // The values are only updated when you call ’getAGMT’
     t2 = millis();
     printScaledAGMT(&myICM);
       client.loop();
     }
     else
     {
       SERIAL_PORT.println("Waiting for data");
       client.loop();
       delay(500);
     }
}

 // Below here are some helper functions to print the data nicely!

void printPaddedInt16b(int16_t val)
{
 if (val > 0)
 {
   SERIAL_PORT.print(" ");
   if (val < 10000)
   {
      SERIAL_PORT.print("0");
   }
   if (val < 1000)
   {
      SERIAL_PORT.print("0");
   }
   if (val < 100)
   {
      SERIAL_PORT.print("0");
   }
   if (val < 10)
   {
      SERIAL_PORT.print("0");
  
   }
 }
 else
 {
   SERIAL_PORT.print("-");
   if (abs(val) < 10000)
   {
      SERIAL_PORT.print("0");
   }
   if (abs(val) < 1000)
   {
      SERIAL_PORT.print("0");
   }
   if (abs(val) < 100)
   {
      SERIAL_PORT.print("0");
   }
   if (abs(val) < 10)
   {
      SERIAL_PORT.print("0");
   }
 }
 SERIAL_PORT.print(abs(val));
}

void printRawAGMT(ICM_20948_AGMT_t agmt)
{
 SERIAL_PORT.print("RAW. Acc [ ");
 printPaddedInt16b(agmt.acc.axes.x);
 SERIAL_PORT.print(", ");
 printPaddedInt16b(agmt.acc.axes.y);
 SERIAL_PORT.print(", ");
 printPaddedInt16b(agmt.acc.axes.z);
 SERIAL_PORT.print(" ], Gyr [ ");
 printPaddedInt16b(agmt.gyr.axes.x);
 SERIAL_PORT.print(", ");
 printPaddedInt16b(agmt.gyr.axes.y);
 SERIAL_PORT.print(", ");
 printPaddedInt16b(agmt.gyr.axes.z);
 SERIAL_PORT.print(" ], Mag [ ");
 printPaddedInt16b(agmt.mag.axes.x);
 SERIAL_PORT.print(", ");
 printPaddedInt16b(agmt.mag.axes.y);
 SERIAL_PORT.print(", ");
 printPaddedInt16b(agmt.mag.axes.z);
 SERIAL_PORT.print(" ], Tmp [ ");
 printPaddedInt16b(agmt.tmp.val);
 SERIAL_PORT.print(" ]");
 SERIAL_PORT.println();
}

void printFormattedFloat(float val, uint8_t leading, uint8_t decimals)
{
 float aval = abs(val);
 if (val < 0)
 {
    SERIAL_PORT.print("-");
 }
 else
 {
    SERIAL_PORT.print(" ");
 }
 
 for (uint8_t indi = 0; indi < leading; indi++)
 {
   uint32_t tenpow = 0;
   if (indi < (leading - 1))
   {
      tenpow = 1;
   }
   
   for (uint8_t c = 0; c < (leading - 1 - indi); c++)
   {
      tenpow *= 10;
   }
   
   if (aval < tenpow)
   {
      SERIAL_PORT.print("0");
   }
   else
   {
      break;
   }
 }
 if (val < 0)
 {
 SERIAL_PORT.print(-val, decimals);
 }
 else
 {
 SERIAL_PORT.print(val, decimals);
 }
}

#ifdef USE_SPI
void printScaledAGMT(ICM_20948_SPI *sensor)
{
#else
void printScaledAGMT(ICM_20948_I2C *sensor)
{
 #endif
// SERIAL_PORT.print("Scaled. Acc (mg) [ ");
//  printFormattedFloat(sensor->accX(), 5, 2);
//  SERIAL_PORT.print(", ");
//  printFormattedFloat(sensor->accY(), 5, 2);
//  SERIAL_PORT.print(", ");
//  printFormattedFloat(sensor->accZ(), 5, 2);
//  SERIAL_PORT.print(" ], Gyr (DPS) [ ");
//  printFormattedFloat(sensor->gyrX(), 5, 2);
//  SERIAL_PORT.print(", ");
//  printFormattedFloat(sensor->gyrY(), 5, 2);
//  SERIAL_PORT.print(", ");
//  printFormattedFloat(sensor->gyrZ(), 5, 2);
//  SERIAL_PORT.print(" ], Mag (uT) [ ");
//  printFormattedFloat(sensor->magX(), 5, 2);
//  SERIAL_PORT.print(", ");
//  printFormattedFloat(sensor->magY(), 5, 2);
//  SERIAL_PORT.print(", ");
//  printFormattedFloat(sensor->magZ(), 5, 2);
//  SERIAL_PORT.print(" ], Tmp (C) [ ");
//  printFormattedFloat(sensor->temp(), 5, 2);
//  SERIAL_PORT.print(" ]");
//  SERIAL_PORT.println();

  if(t2 != 0 && t1 != 0 && abs(sensor->gyrZ()) > .8)
  {
      angular_position = angular_position + ((prev_gyr_Z + sensor->gyrZ())*(t2-t1)/2000);
      angular_position = fmod(angular_position,360);
      prev_gyr_Z = sensor->gyrZ();
      sector = fmod((angular_position + 360),360);
      sector = int(fmod((sector + 22.5) / 45,8) + 1);
      //Serial.println(angular_position);
   }
   if(abs(sensor->accZ())>1000)
   {
      sector = 0;
   }
   //Serial.println(sector);
   if(prev_sector != sector)
   {
      char msg_out[2];
      sprintf(msg_out, "%d", sector);
      //Serial.println(msg_out);
      client.publish(topic, msg_out);
   }
   prev_sector = sector; 
}
