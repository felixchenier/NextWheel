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
        DATA_FRAME_TYPE_SUPERFRAME = 255
    };

    DataFrame(DataFrameType type, uint16_t data_size, uint64_t timestamp = DataFrame::getCurrentTimeStamp())
        : m_type(type),
          m_dataSize(data_size),
          m_timestamp(timestamp)
    {
    }

    // Copy constructor = default implementation (copy by value)
    DataFrame(const DataFrame& other) = default;

    DataFrameType getType() { return m_type; }

    String getTypeString()
    {
        switch (m_type)
        {
            case DATA_FRAME_TYPE_UNKNOWN:
                return "UNKNOWN";
            case DATA_FRAME_TYPE_CONFIG:
                return "CONFIG";
            case DATA_FRAME_TYPE_ADC:
                return "ADC";
            case DATA_FRAME_TYPE_IMU:
                return "IMU";
            case DATA_FRAME_TYPE_POWER:
                return "POWER";
            case DATA_FRAME_TYPE_RTC:
                return "RTC";
            default:
                return "UNKNOWN";
        };
    }

    size_t getHeaderSize() { return HEADER_SIZE; }

    size_t getTotalSize() const { return HEADER_SIZE + getDataSize(); }

    size_t getDataSize() const { return m_dataSize; }

    virtual size_t serializePayload(uint8_t* buffer, size_t buffer_size) const = 0;


    virtual DataFrame* clone() const = 0;

    static uint64_t getCurrentTimeStamp()
    {
        // TODO Get the current time from epoch in microseconds
        struct timeval tv_now;
        gettimeofday(&tv_now, NULL);
        uint64_t time_us = (uint64_t)tv_now.tv_sec * 1000000L + (uint64_t)tv_now.tv_usec;
        return time_us;
    }

    void setTimestamp(uint64_t timestamp = DataFrame::getCurrentTimeStamp()) { m_timestamp = timestamp; }

    virtual void print()
    {
        uint8_t buffer[getTotalSize()];
        serialize(buffer, getTotalSize());


        Serial.println();
        Serial.println("DataFrame");
        Serial.print("Type: ");
        Serial.print(m_type);
        Serial.print(" ");
        Serial.println(getTypeString());
        Serial.print("Timestamp: ");
        Serial.println(m_timestamp);
        Serial.print("Data size: ");
        Serial.println(getDataSize());

        Serial.print("Header: 0x");
        for (int i = 0; i < getHeaderSize(); i++)
        {
            Serial.printf("%2.2x", buffer[i]);
            Serial.print(" ");
        }

        Serial.print("Data: 0x");
        for (int i = getHeaderSize(); i < getTotalSize(); i++)
        {
            Serial.printf("%2.2x", buffer[i]);
            Serial.print(" ");
        }
        Serial.println();
    }

    virtual size_t serialize(uint8_t* buffer, size_t bufferSize) const
    {
        // bufferSize must be at least MAX_FRAME_DATA_SIZE_BYTES + header size
        if (bufferSize < getTotalSize())
        {
            return 0;
        }
        size_t size = HEADER_SIZE;
        // Safety, set everything to 0
        memset(buffer, 0, getTotalSize());

        // Set header data (make sure it is only one byte)
        buffer[0] = (uint8_t)m_type;
        // Copy timestamp
        memcpy(buffer + 1, &m_timestamp, sizeof(m_timestamp));
        // Set data size (make sure it is only one byte)
        buffer[9] = m_dataSize & 0xFF;

        // Copy payload data
        size += serializePayload(buffer + HEADER_SIZE, getDataSize());

        return size;
    }

protected:
    DataFrameType m_type;
    uint64_t m_timestamp;
    uint8_t m_dataSize;

private:
    DataFrame() = default;
};

typedef DataFrame* DataFramePtr;

#endif
