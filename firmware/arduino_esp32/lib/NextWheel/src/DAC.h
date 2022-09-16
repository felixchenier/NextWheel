#ifndef _DAC_H_
#define _DAC_H_

#include <Arduino.h>
#include <I2S.h>
#include <NextWheel.h>

class DAC {
    public:
    DAC() = default;
    void setup();
    void setVoltage(uint8_t voltage);
};

#endif // _DAC_H_
