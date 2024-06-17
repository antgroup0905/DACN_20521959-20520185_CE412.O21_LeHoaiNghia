#ifndef TURBIDITYSENSOR_H
#define TURBIDITYSENSOR_H

#include <Arduino.h>

class TurbiditySensor
{
public:
    TurbiditySensor(int pin);
    float getTurbidityValue();

private:
    int sensorPin;
    float calculateNTU(float voltage);
};

#endif // TURBIDITYSENSOR_H
