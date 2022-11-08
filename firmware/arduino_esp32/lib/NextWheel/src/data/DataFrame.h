#ifndef _DATA_FRAME_H_
#define _DATA_FRAME_H_

#include "NextWheel.h"
#include <Arduino.h>
#include <sys/time.h>
#include <memory>


class DataFrame
{
public:
    const static uint8_t HEADER_SIZE = 10;

    enum DataFrameType
    {
        DATA_FRAME_TYPE_UNKNOWN = 0,
        DATA_FRAME_TYPE_CONFIG = 1,
        DATA_FRAME_TYPE_ADC = 2,
        DATA_FRAME_TYPE_IMU = 3,
        DATA_FRAME_TYPE_POWER = 4,
        DATA_FRAME_TYPE_RTC = 5,
        DATA_FRAME_TYPE_AUDIO = 6,
        DATA_FRAME_TYPE_QUAD_ENCODER = 7,
        DATA_FRAME_TYPE_SUPERFRAME = 255
    };

    DataFrame(DataFrameType type, uint16_t data_size, uint64_t timestamp = DataFrame::getCurrentTimeStamp());

    // Copy constructor = default implementation (copy by value)
    DataFrame(const DataFrame& other) = default;

    DataFrameType getType();

    String getTypeString();

    size_t getHeaderSize();

    size_t getTotalSize() const;

    size_t getDataSize() const;

    virtual size_t serializePayload(uint8_t* buffer, size_t buffer_size) const = 0;

    virtual DataFrame* clone() const = 0;

    static uint64_t getCurrentTimeStamp();

    void setTimestamp(uint64_t timestamp = DataFrame::getCurrentTimeStamp());

    virtual void print();

    virtual size_t serialize(uint8_t* buffer, size_t bufferSize) const;

protected:
    DataFrameType m_type;
    uint64_t m_timestamp;
    uint8_t m_dataSize;

private:
    DataFrame() = default;
};

typedef DataFrame* DataFramePtr;

#endif
