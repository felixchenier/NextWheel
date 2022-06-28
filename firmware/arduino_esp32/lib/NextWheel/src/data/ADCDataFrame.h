#ifndef _ADC_DATA_FRAME_H_
#define _ADC_DATA_FRAME_H_


#include "data/DataFrame.h"

class ADCDataFrame : public DataFrame
{
public:
    const static size_t NUM_ADC_CHANNELS = 8;
    const static size_t ADC_DATA_FRAME_SIZE = NUM_ADC_CHANNELS * sizeof(float);

    ADCDataFrame(uint64_t timestamp = DataFrame::getCurrentTimeStamp())
        : DataFrame(DataFrame::DATA_FRAME_TYPE_ADC, ADC_DATA_FRAME_SIZE, timestamp)
    {
        memset(m_data, 0, ADC_DATA_FRAME_SIZE);
    }

    ADCDataFrame(const ADCDataFrame& other) : DataFrame(other) { memcpy(m_data, other.m_data, ADC_DATA_FRAME_SIZE); }

    virtual size_t serializePayload(uint8_t* buffer, size_t buffer_size) const override
    {
        memcpy(buffer, m_data, ADC_DATA_FRAME_SIZE);
        return ADC_DATA_FRAME_SIZE;
    }

    virtual DataFrame* clone() const override { return new ADCDataFrame(*this); }

    float getChannelValue(uint8_t channel)
    {
        if (channel >= 0 && channel < NUM_ADC_CHANNELS)
        {
            return m_data[channel];
        }
        return 0;
    }

    void setChannelValue(uint8_t channel, float value)
    {
        if (channel >= 0 && channel < NUM_ADC_CHANNELS)
        {
            m_data[channel] = value;
        }
    }

    virtual void print() override
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

private:
    float m_data[NUM_ADC_CHANNELS];
};

#endif  // _ADC_DATA_FRAME_H_
