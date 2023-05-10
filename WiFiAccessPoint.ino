/*
   Copyright (c) 2015, Majenko Technologies
   All rights reserved.

   Redistribution and use in source and binary forms, with or without modification,
   are permitted provided that the following conditions are met:

 * * Redistributions of source code must retain the above copyright notice, this
     list of conditions and the following disclaimer.

 * * Redistributions in binary form must reproduce the above copyright notice, this
     list of conditions and the following disclaimer in the documentation and/or
     other materials provided with the distribution.
*/

/* Create a WiFi access point and provide a web server on it. */

#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

#ifndef APSSID
#define APSSID "ESP_ap"
#define APPSK "thereisnospoon"
#endif

/* Set these to your desired credentials. */
const char *ssid = APSSID;
const char *password = APPSK;

ESP8266WebServer server(80);

/* Just a little test message.  Go to http://192.168.4.1 in a web browser
   connected to this access point to see it.
*/
void handleSentVar() {
  if (server.hasArg("sensor_reading")) {
    int readingInt = server.arg("sensor_reading").toInt();
    if(readingInt==HIGH) {
      digitalWrite(D5, HIGH);
    }
    else digitalWrite(D5, LOW);
    Serial.println(readingInt);
    server.send(200, "text/html?", "Data Received");
  }
}

void setup() {
  delay(1000);
  Serial.begin(115200);
  /* You can remove the password parameter if you want the AP to be open. */
  WiFi.softAP(ssid, password);
  pinMode(D5, OUTPUT);
  server.on("/data/", HTTP_GET, handleSentVar);
  server.begin();
}

void loop() {
  server.handleClient();
}
