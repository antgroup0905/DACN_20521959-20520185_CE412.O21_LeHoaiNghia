#include <OneWire.h>
#include <DallasTemperature.h>
// #include <pHSensor.h>
#include <TurbiditySensor.h>

#define pHPin A0        // pH meter Analog output to Arduino Analog Input 0
#define turbidityPin A1 // Turbidity meter Analog output to Arduino Analog Input 1
#define Offset 0.25     // deviation compensate
#define LED 13
#define samplingInterval 20 // Sampling interval in milliseconds
#define ArrayLength 40      // times of collection
#define ONE_WIRE_BUS 3
int pHArrayIndex = 0;
int pHArray[ArrayLength];

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature temperatureSensor(&oneWire);
TurbiditySensor myTurbiditySensor(turbidityPin);

void setup()
{
  pinMode(LED, OUTPUT);
  Serial.begin(9600);
  temperatureSensor.begin();
  //  Serial.println("pH meter experiment!");	// Test the serial monitor
}

double averageArray(int *arr, int number);

void loop()
{
  // Run the function of pH sensor
  // float pHValue = myPHSensor.getpHValue();
  static unsigned long samplingTime = millis();
  static float pHValue, voltage;

  if (millis() - samplingTime > samplingInterval)
  {
    pHArray[pHArrayIndex++] = analogRead(pHPin);
    if (pHArrayIndex == ArrayLength)
      pHArrayIndex = 0;
    voltage = averageArray(pHArray, ArrayLength) * 5.0 / 1024;
    pHValue = 3.5 * voltage + Offset;
    samplingTime = millis();
  }
  delay(100);

  // Run the function of Turbidity sensor
  float ntu = myTurbiditySensor.getTurbidityValue();
  delay(100);

  // Run the function of Temperature sensor
  temperatureSensor.requestTemperatures();
  float temperature = temperatureSensor.getTempCByIndex(0);
  delay(100);

  // Sending value to ESP32 via UART (TX/RX)
  Serial.print("pH value: ");
  Serial.println(pHValue, 2);

  Serial.print("Turbidity value: ");
  Serial.println(ntu, 2);

  Serial.print("Temperature value: ");
  Serial.println(temperature, 2);

  delay(5000);
}

double averageArray(int *arr, int number)
{
  int i;
  int max, min;
  double avg;
  long amount = 0;

  if (number <= 0)
  {
    Serial.println("Error: Invalid array size for averaging!");
    return 0;
  }

  if (number < 5)
  { // less than 5, calculate direct statistics
    for (i = 0; i < number; i++)
    {
      amount += arr[i];
    }
    avg = amount / number;
    return avg;
  }
  else
  {
    if (arr[0] < arr[1])
    {
      min = arr[0];
      max = arr[1];
    }
    else
    {
      min = arr[1];
      max = arr[0];
    }
    for (i = 2; i < number; i++)
    {
      if (arr[i] < min)
      {
        amount += min; // arr < min
        min = arr[i];
      }
      else
      {
        if (arr[i] > max)
        {
          amount += max; // arr > max
          max = arr[i];
        }
        else
        {
          amount += arr[i]; // min <= arr <= max
        }
      }
    }
    avg = (double)amount / (number - 2);
  }
  return avg;
}