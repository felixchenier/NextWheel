#ifndef _QUAD_ENCODER_DATA_FRAME_H_
#define _QUAD_ENCODER_DATA_FRAME_H_

#include "data/DataFrame.h"

class QuadEncoderDataFrame : public DataFrame
{
public:
    const static size_t QUAD_ENCODER_DATA_FRAME_SIZE = sizeof(int64_t);

    QuadEncoderDataFrame(int64_t count, uint64_t timestamp = DataFrame::getCurrentTimeStamp());

    QuadEncoderDataFrame(uint64_t timestamp = DataFrame::getCurrentTimeStamp());
    QuadEncoderDataFrame(const QuadEncoderDataFrame& other);
    virtual size_t serializePayload(uint8_t* buffer, size_t buffer_size) const override;
    virtual DataFrame* clone() const override;
    int64_t getCount() const;
    void setCount(int64_t count);

protected:
    int64_t m_count;
};

#endif  // _QUAD_ENCODER_DATA_FRAME_H_