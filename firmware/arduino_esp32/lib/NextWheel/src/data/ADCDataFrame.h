#ifndef _ADC_DATA_FRAME_H_
#define _ADC_DATA_FRAME_H_


#include "data/DataFrame.h"

class ADCDataFrame : public DataFrame
{
public:
    // NOTE : We are only using 6 out of 8 channels
    const static size_t NUM_ADC_CHANNELS = 6;
    const static size_t ADC_DATA_FRAME_SIZE = NUM_ADC_CHANNELS * sizeof(uint16_t);

    ADCDataFrame(uint64_t timestamp = DataFrame::getCurrentTimeStamp());

    ADCDataFrame(const ADCDataFrame& other);

    virtual size_t serializePayload(uint8_t* buffer, size_t buffer_size) const override;

    virtual DataFrame* clone() const override;

    uint16_t getChannelValue(uint8_t channel);

    void setChannelValue(uint8_t channel, uint16_t value);

    virtual void print() override;

private:
    uint16_t m_data[NUM_ADC_CHANNELS];
};

#endif  // _ADC_DATA_FRAME_H_
