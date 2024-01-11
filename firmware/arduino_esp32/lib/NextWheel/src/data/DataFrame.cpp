#include "data/DataFrame.h"


DataFrame::DataFrame(DataFrameType type, uint16_t data_size, uint64_t timestamp)
    : m_type(type),
      m_dataSize(data_size),
      m_timestamp(timestamp)
{
}


DataFrame::DataFrameType DataFrame::getType()
{
    return m_type;
}

String DataFrame::getTypeString()
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

size_t DataFrame::getHeaderSize()
{
    return HEADER_SIZE;
}

size_t DataFrame::getTotalSize() const
{
    return HEADER_SIZE + getDataSize();
}

size_t DataFrame::getDataSize() const
{
    return m_dataSize;
}

uint64_t DataFrame::getCurrentTimeStamp()
{
    // TODO Get the current time from epoch in microseconds
    struct timeval tv_now;
    gettimeofday(&tv_now, NULL);
    uint64_t time_us = (uint64_t)tv_now.tv_sec * 1000000L + (uint64_t)tv_now.tv_usec;
    return time_us;
}

void DataFrame::setTimestamp(uint64_t timestamp)
{
    m_timestamp = timestamp;
}

void DataFrame::print()
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

size_t DataFrame::serialize(uint8_t* buffer, size_t bufferSize) const
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
