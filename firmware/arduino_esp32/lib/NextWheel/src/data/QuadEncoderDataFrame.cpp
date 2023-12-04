#include "data/QuadEncoderDataFrame.h"

QuadEncoderDataFrame::QuadEncoderDataFrame(int64_t count, uint64_t timestamp)
    : DataFrame(DataFrame::DATA_FRAME_TYPE_QUAD_ENCODER, QUAD_ENCODER_DATA_FRAME_SIZE, timestamp),
      m_count(count)
{
}

QuadEncoderDataFrame::QuadEncoderDataFrame(uint64_t timestamp)
    : DataFrame(DataFrame::DATA_FRAME_TYPE_QUAD_ENCODER, QUAD_ENCODER_DATA_FRAME_SIZE, timestamp),
      m_count(0)
{
}

QuadEncoderDataFrame::QuadEncoderDataFrame(const QuadEncoderDataFrame& other) : DataFrame(other), m_count(other.m_count)
{
}

size_t QuadEncoderDataFrame::serializePayload(uint8_t* buffer, size_t buffer_size) const
{
    memcpy(buffer, &m_count, sizeof(int64_t));
    return QUAD_ENCODER_DATA_FRAME_SIZE;
}


DataFrame* QuadEncoderDataFrame::clone() const
{
    return new QuadEncoderDataFrame(*this);
}

int64_t QuadEncoderDataFrame::getCount() const
{
    return m_count;
}

void QuadEncoderDataFrame::setCount(int64_t count)
{
    m_count = count;
}
