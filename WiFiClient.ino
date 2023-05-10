#include <ESP8266WiFi.h>


const char *ssid = "ESP_ap";
const char *password = "thereisnospoon";
int sensorValue = 13;        // value read from the PIR
int outputValue;        //value to send to the server

void setup() {
  Serial.begin(115200);
  delay(10);

  // Explicitly set the ESP8266 to be a WiFi-client
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  pinMode(sensorValue, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  
}



void loop() {
  long val = digitalRead(sensorValue);
  // builtin led to debug motion sensor, activates when motion sensor sends signal, deactivates when motion sensor is off
  if (val == HIGH) {
    digitalWrite(LED_BUILTIN, LOW);
    Serial.println("Motion Detected!");
    Serial.println(sensorValue);
    outputValue = 1;
  }
  else if (val == LOW) {
    digitalWrite(LED_BUILTIN, HIGH);
    Serial.println("Motion not detected :(");
    Serial.println(sensorValue);    
    outputValue = 0;
  }

  // Use WiFiClient class to create TCP connections
  WiFiClient client;
  const char * host = "192.168.4.1";
  const int httpPort = 80;

  if (!client.connect(host, httpPort)) {
    Serial.println("connection failed");
    return;
  }


  // We now create a URI for the request. Something like /data/?sensor_reading=123
  String url = "/data/";
  url += "?sensor_reading=";
  url += outputValue;

  // This will send the request to the server
  client.print(String("GET ") + url + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n");
 
  
//  unsigned long timeout = millis();
//  while (client.available() == 0) {
//    if (millis() - timeout > 5000) {
//      Serial.println(">>> Client Timeout !");
//      client.stop();
//      return;
//    }
//  }

  delay(500);
}
