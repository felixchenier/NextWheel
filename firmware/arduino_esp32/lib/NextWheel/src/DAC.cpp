#include "DAC.h"
#include "driver/dac.h"

void DAC::setup() {
    dac_output_enable(DAC_CHANNEL_1);
    dac_output_voltage(DAC_CHANNEL_1, 0); //(VDD * 200 / 255)

    /*
    if (!I2S.begin(ADC_DAC_MODE, 8000, 16))
    {
        Serial.println("I2S failed to start");
    }
    else
    {
        Serial.println("I2S started");
    }
    */
}

void DAC::setVoltage(uint8_t voltage)
{
    dac_output_voltage(DAC_CHANNEL_1, voltage); //(VDD * 200 / 255)
}
