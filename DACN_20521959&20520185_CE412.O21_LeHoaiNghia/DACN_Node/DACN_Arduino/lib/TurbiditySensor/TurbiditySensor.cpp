#include "TurbiditySensor.h"

TurbiditySensor::TurbiditySensor(int pin) : sensorPin(pin) {}

float TurbiditySensor::getTurbidityValue()
{
    int sensorValue = analogRead(sensorPin);               // read the input on the analog pin
    float turbidityVoltage = sensorValue * (5.0 / 1024.0); // Convert the analog reading to a voltage
    return calculateNTU(turbidityVoltage);
}

float TurbiditySensor::calculateNTU(float voltage)
{
    float ntu = -1120.4 * sq(voltage) + 5742.3 * voltage - 4352.9;
    if (ntu < 0)
    {
        ntu = 0;
    }
    if (voltage < 2.5)
    {
        ntu = 3000;
    }
    return ntu;
}
