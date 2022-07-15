#ifndef _ADC_DATA_FRAME_H_
#define _ADC_DATA_FRAME_H_


#include "data/DataFrame.h"

class ADCDataFrame : public DataFrame
{
public:
    const static size_t NUM_ADC_CHANNELS = 8;
    const static size_t ADC_DATA_FRAME_SIZE = NUM_ADC_CHANNELS * sizeof(float);

    ADCDataFrame(uint64_t timestamp = DataFrame::getCurrentTimeStamp());

    ADCDataFrame(const ADCDataFrame& other);

    virtual size_t serializePayload(uint8_t* buffer, size_t buffer_size) const override;

    virtual DataFrame* clone() const override;

    float getChannelValue(uint8_t channel);

    void setChannelValue(uint8_t channel, float value);

    virtual void print() override;

private:
    float m_data[NUM_ADC_CHANNELS];
};

#endif  // _ADC_DATA_FRAME_H_
