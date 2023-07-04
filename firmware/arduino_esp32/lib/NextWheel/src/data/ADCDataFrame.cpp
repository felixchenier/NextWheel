#include "data/ADCDataFrame.h"

ADCDataFrame::ADCDataFrame(uint64_t timestamp)
    : DataFrame(DataFrame::DATA_FRAME_TYPE_ADC, ADC_DATA_FRAME_SIZE, timestamp)
{
    memset(m_data, 0, ADC_DATA_FRAME_SIZE);
}

ADCDataFrame::ADCDataFrame(const ADCDataFrame& other) : DataFrame(other)
{
    memcpy(m_data, other.m_data, ADC_DATA_FRAME_SIZE);
}

size_t ADCDataFrame::serializePayload(uint8_t* buffer, size_t buffer_size) const
{
    memcpy(buffer, m_data, ADC_DATA_FRAME_SIZE);
    return ADC_DATA_FRAME_SIZE;
}

DataFrame* ADCDataFrame::clone() const
{
    return new ADCDataFrame(*this);
}

float ADCDataFrame::getChannelValue(uint8_t channel)
{
    if (channel >= 0 && channel < NUM_ADC_CHANNELS)
    {
        return m_data[channel];
    }
    return 0;
}

void ADCDataFrame::setChannelValue(uint8_t channel, float value)
{
    if (channel >= 0 && channel < NUM_ADC_CHANNELS)
    {
        m_data[channel] = value;
    }
}

void ADCDataFrame::print()
{
    DataFrame::print();
    Serial.print("ADC Data: ");
    for (int i = 0; i < NUM_ADC_CHANNELS; i++)
    {
        Serial.print(m_data[i]);
        Serial.print(" ");
    }
    Serial.println();
}