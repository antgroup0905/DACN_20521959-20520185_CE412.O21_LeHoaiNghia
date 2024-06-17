#ifndef PHSENSOR_H
#define PHSENSOR_H

#include <Arduino.h>

class pHSensor
{
public:
    pHSensor(uint8_t pin, float offset = 0.25, size_t arrayLength = 40, unsigned int samplingInterval = 20);
    void begin();

    float getpHValue();

private:
    uint8_t pHPin;
    float Offset;
    size_t ArrayLength;
    unsigned int samplingInterval;
    int *pHArray;
    size_t pHArrayIndex;
    unsigned long samplingTime;
    float pHValue;
    float voltage;

    double averageArray(int *arr, size_t number);
};

#endif // PHSENSOR_H
