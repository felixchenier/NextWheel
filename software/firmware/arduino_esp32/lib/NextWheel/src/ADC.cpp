#include "ADC.h"

ADC::ADC() : m_ads8688(PIN_SPI_CS1) {}

void ADC::begin()
{
    uint8_t spd = 0b00000000;

    for (auto i = 0; i < ADCDataFrame::NUM_ADC_CHANNELS; i++)
    {
        spd |= (1 << i);
    }

    m_ads8688.setChannelSPD(spd);
    // VREF 4.096V (default)
    // R1 = Input range to -1.25/+1.25
    m_ads8688.setGlobalRange(R1);  // set range for all channels
    m_ads8688.autoRst();  // reset auto sequence
}

void ADC::update(ADCDataFrame& frame)
{
    for (auto i = 0; i < ADCDataFrame::NUM_ADC_CHANNELS; i++)
    {
        uint16_t val = m_ads8688.noOp();  // trigger samples
        // This gets the value in volts
        // frame.setChannelValue(i, m_ads8688.I2V(val, R1));
        // This gets the value in counts
        frame.setChannelValue(i, val);
    }
    frame.setTimestamp(DataFrame::getCurrentTimeStamp());
}
