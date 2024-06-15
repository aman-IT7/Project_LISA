#include <Arduino.h>
#include "DHT.h"
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char *ssid = "Aman"; // Wifi ssid and Password
const char *password = "1234567890";
const char *mqtt_broker = "mqtt.eclipseprojects.io"; // mqtt broker address and port number
const int mqtt_port = 1883;

float *ambient = nullptr;
float *soil = nullptr;

#define DHTPIN D6
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

#define BUS D8
OneWire onewire(BUS);
DallasTemperature temperature_sensor(&onewire);

#define moisture_sensor A0

unsigned long int current_time, previous_time = 0;
uint32_t interval = 2000;

WiFiClient esp;
PubSubClient client(esp);

void connectify(const char *network, const char *pass)
{
  int times = 0;
  Serial.println("connecting to ");
  Serial.print(network);
  Serial.println("----------------------------------------------------");
  WiFi.begin(network, pass);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
    times += 1;
  }
  Serial.println("----------------------------------------------------");
  Serial.println("Connecting tries = ");
  Serial.println(times);
  Serial.println("----------------------------------------------------");
  Serial.println("IP address ----> ");
  Serial.println(WiFi.localIP());
}

void reconnect()
{

  // Loop until we're reconnected
  while (!client.connected())
  {

    Serial.println("Attempting MQTT connection...");

    if (client.connect("esp"))
    {
      Serial.println("connected");
    }
    else
    {
      Serial.print("failed to connect, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

float *read_ambient()
{

  float h = dht.readHumidity();
  float t = dht.readTemperature();
  static float data[2];

  if (isnan(h) || isnan(t))
  {
    data[0] = -1;
    data[1] = -1;
  }

  else
  {
    data[0] = h;
    data[1] = t;
  }

  return data;
}

float *read_soil()
{
  float moisture = 0.0;
  static float soil_data[3];

  moisture = (float)(analogRead(moisture_sensor) / 1024.00);
  soil_data[0] = moisture;
  soil_data[1] = (100 - moisture * 100);

  temperature_sensor.requestTemperatures();
  soil_data[2] = temperature_sensor.getTempCByIndex(0);

  return soil_data;
}

void setup()
{
  Serial.begin(115200);
  connectify(ssid, password);
  client.setServer(mqtt_broker, mqtt_port);

  dht.begin();
  temperature_sensor.begin();
  pinMode(moisture_sensor, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.println("Done setup");
}

void loop()
{

  if (!client.connected())
  {
    reconnect();
  }
  client.loop();

  current_time = millis();

  if (current_time - previous_time >= interval)
  {
    char buffer[10]; // publish buffer

    ambient = read_ambient();
    /*{humidity in percentage , temperature in celcius}
      { *(ambient) , *(ambient+1) }*/

    soil = read_soil();
    /*{moisture in 1024 , moisture in % 0-100 , temperature in celcius}
    {*(soil) , *(soil+1) , *(soil+2) }*/

    if (*(ambient) == -1 || *(ambient + 1) == -1)
    { // error detection for dht22
      Serial.println("failed to read data from sensor");
    }

    else
    {

      dtostrf(*(ambient), 6, 2, buffer);
      client.publish("ambient/humidity", buffer);

      dtostrf(*(ambient + 1), 6, 2, buffer);
      client.publish("ambient/temperature", buffer);

      dtostrf(*(soil), 6, 2, buffer);
      client.publish("soil/moisture/1024", buffer);

      dtostrf(*(soil + 1), 6, 2, buffer);
      client.publish("soil/moisture/percentage", buffer);

      dtostrf(*(soil + 2), 6, 2, buffer);
      client.publish("soil/temperature", buffer);
    }
    digitalWrite(LED_BUILTIN, HIGH);
    previous_time = current_time;
  }
  digitalWrite(LED_BUILTIN, LOW);
}
