#include "pHSensor.h"

pHSensor::pHSensor(uint8_t pin, float offset, size_t arrayLength, unsigned int samplingInterval)
    : pHPin(pin), Offset(offset), ArrayLength(arrayLength), samplingInterval(samplingInterval), pHArrayIndex(0), samplingTime(0), pHValue(0.0), voltage(0.0)
{
    pHArray = new int[ArrayLength];
}

void pHSensor::begin()
{
    Serial.begin(9600);
}

float pHSensor::getpHValue()
{
    voltage = averageArray(pHArray, ArrayLength) * 5.0 / 1024;
    pHValue = 3.5 * voltage + Offset;
    return pHValue;
}

double pHSensor::averageArray(int *arr, size_t number)
{
    if (number <= 0)
    {
        Serial.println("Error: Invalid array size for averaging!");
        return 0;
    }

    int min, max;
    long amount = 0;

    if (number < 5)
    {
        for (size_t i = 0; i < number; i++)
        {
            amount += arr[i];
        }
        return (double)amount / number;
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
        for (size_t i = 2; i < number; i++)
        {
            if (arr[i] < min)
            {
                amount += min;
                min = arr[i];
            }
            else if (arr[i] > max)
            {
                amount += max;
                max = arr[i];
            }
            else
            {
                amount += arr[i];
            }
        }
        return (double)amount / (number - 2);
    }
}
