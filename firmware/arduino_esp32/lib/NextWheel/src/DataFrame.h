#ifndef _DATA_FRAME_H_
#define _DATA_FRAME_H_

#include "NextWheel.h"
#include <Arduino.h>
#include <sys/time.h>

#define MAX_FRAME_DATA_SIZE_BYTES 36
#define HEADER_SIZE 10

enum DataFrameType {
    DATA_FRAME_TYPE_UNKNOWN = 0,
    DATA_FRAME_TYPE_WIFI_CONFIG = 1,
    DATA_FRAME_TYPE_ADC = 2,
    DATA_FRAME_TYPE_IMU = 3,
    DATA_FRAME_TYPE_POWER = 4,
    DATA_FRAME_TYPE_RTC = 5
};


template <typename T>
class DataFrame {
    public:

        DataFrame(DataFrameType type, T *data, uint8_t size, uint64_t timestamp = DataFrame::getCurrentTimeStamp())
            : m_type(type), m_timestamp(timestamp) {
            // Clear the data buffer
            memset(m_uint8_data, 0 , MAX_FRAME_DATA_SIZE_BYTES);
            setData<T>(data, size);

        }

        // Copy constructor = default implementation (copy by value)
        DataFrame(const DataFrame& other) = default;

        DataFrameType getType() {
            return m_type;
        }

        template <typename U>
        U* getData() {
            return (U*)m_uint8_data;
        }

        template <typename U>
        void setData(U* data, uint8_t size) {
            m_dataSize = size * sizeof(U);

            //Avoid buffer overflow
            if (m_dataSize > MAX_FRAME_DATA_SIZE_BYTES) {
                m_dataSize = MAX_FRAME_DATA_SIZE_BYTES;
                Serial.println("DataFrame::setData: Buffer overflow");
            }

            // Copy the data if not null
            if (data) {
                memcpy(m_uint8_data, data, m_dataSize);
            }
        }

        template <typename U>
        void setDataItem(uint8_t index, U data) {
            if (index < m_dataSize / sizeof(U)) {
               m_data[index] = data;
            }
        }

        template <typename U>
        U getDataItem(uint8_t index) {
            if (index < m_dataSize / sizeof(U)) {
                return m_data[index];
            }
            return 0;
        }

        static uint64_t getCurrentTimeStamp() {
            // TODO Get the current time from epoch in microseconds
            struct timeval tv_now;
            gettimeofday(&tv_now, NULL);
            uint64_t time_us = (uint64_t)tv_now.tv_sec * 1000000 + (uint64_t)tv_now.tv_usec;
            return time_us;
        }

        virtual void print() {
            Serial.println();
            Serial.println("DataFrame");
            Serial.print("Type: ");Serial.println(m_type);
            Serial.print("Timestamp: ");Serial.println(m_timestamp);
            Serial.print("Data size: ");Serial.println(m_dataSize);

            Serial.print("Data: ");
            /*
            Serial.print("Data: 0x");
            for (int i = 0; i < m_dataSize; i++) {
                Serial.print(m_uint8_data[i], HEX);
                Serial.print(" ");
            }
            Serial.println();
            */

            for (int i = 0; i < m_dataSize / sizeof(T); i++) {
                Serial.print(m_data[i]);
                Serial.print(" ");
            }


            Serial.println();
        }

        virtual size_t serialize(uint8_t* buffer, size_t bufferSize) {
            // bufferSize must be at least MAX_FRAME_DATA_SIZE_BYTES + header size
            if (bufferSize < MAX_FRAME_DATA_SIZE_BYTES + HEADER_SIZE) {
                return 0;
            }

            // Type = 1 byte
            buffer[0] = m_type;

            // Data size = 1 byte
            buffer[1] = m_dataSize;

            //Timestamp = 8 bytes
            buffer[2] = (m_timestamp >> 56) & 0xFF;
            buffer[3] = (m_timestamp >> 48) & 0xFF;
            buffer[4] = (m_timestamp >> 40) & 0xFF;
            buffer[5] = (m_timestamp >> 32) & 0xFF;
            buffer[6] = (m_timestamp >> 24) & 0xFF;
            buffer[7] = (m_timestamp >> 16) & 0xFF;
            buffer[8] = (m_timestamp >> 8) & 0xFF;
            buffer[9] = m_timestamp & 0xFF;

            // Copy data
            memcpy(buffer + HEADER_SIZE, m_uint8_data, m_dataSize);

            return HEADER_SIZE + m_dataSize;
        }


    protected:
        DataFrameType m_type;
        uint64_t m_timestamp;
        uint8_t m_dataSize;

        // Data is stored in the following format:
        union {
            uint8_t m_uint8_data[MAX_FRAME_DATA_SIZE_BYTES];
            T m_data[MAX_FRAME_DATA_SIZE_BYTES / sizeof(T)];

        };

    private:
        DataFrame() = default;
};

#endif
