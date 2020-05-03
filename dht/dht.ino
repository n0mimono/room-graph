#include <DHT.h>

const int PIN_LED = 13;

const int PIN_DHT = 8;
DHT dht(PIN_DHT, DHT11);

void setup()
{
  pinMode(PIN_LED, OUTPUT);

  Serial.begin(9600);
  Serial.println("DHT11");
  dht.begin();
}

void loop()
{
  digitalWrite(PIN_LED, HIGH);
  delay(1000);

  digitalWrite(PIN_LED, LOW);
  delay(4000);

  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  Serial.print(humidity);
  Serial.print(",");
  Serial.print(temperature);
  Serial.println(",");
}
