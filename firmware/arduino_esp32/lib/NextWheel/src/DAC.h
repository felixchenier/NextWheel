#ifndef _DAC_H_
#define _DAC_H_

#include <Arduino.h>
#include <NextWheel.h>

// Taken from example here:
// https://github.com/espressif/esp-idf/blob/master/examples/peripherals/i2s/i2s_adc_dac/main/app_main.c


class DAC
{
public:
    DAC();
    void setup();
    void setVoltage(uint8_t voltage);
    size_t writeFrame(const void* samples, uint32_t length);
    uint32_t getSampleRate() const { return m_sample_rate; }

private:
    uint32_t m_sample_rate;
};
#endif  // _DAC_H_
