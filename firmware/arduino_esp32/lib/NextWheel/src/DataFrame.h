#ifndef _DATA_FRAME_H_
#define _DATA_FRAME_H_

#include "NextWheel.h"
#include <Arduino.h>
#include <sys/time.h>
#include <memory>



class DataFrame {

    public:
        const static uint8_t HEADER_SIZE = 10;

        enum DataFrameType {
            DATA_FRAME_TYPE_UNKNOWN = 0,
            DATA_FRAME_TYPE_WIFI_CONFIG = 1,
            DATA_FRAME_TYPE_ADC = 2,
            DATA_FRAME_TYPE_IMU = 3,
            DATA_FRAME_TYPE_POWER = 4,
            DATA_FRAME_TYPE_RTC = 5
        };

        DataFrame(DataFrameType type, uint64_t timestamp = DataFrame::getCurrentTimeStamp())
            : m_type(type), m_timestamp(timestamp) {

        }


        // Copy constructor = default implementation (copy by value)
        DataFrame(const DataFrame& other) = default;

        DataFrameType getType() {
            return m_type;
        }

        String getTypeString() {
            switch (m_type) {
                case DATA_FRAME_TYPE_UNKNOWN:
                    return "UNKNOWN";
                case DATA_FRAME_TYPE_WIFI_CONFIG:
                    return "WIFI_CONFIG";
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

        size_t getTotalSize() {
            return HEADER_SIZE + getDataSize();
        }

        virtual uint8_t* getData() = 0;

        virtual size_t getDataSize() const = 0;

        virtual void setData(uint8_t* data, uint8_t size) = 0;

        virtual DataFrame* clone() const = 0;

        static uint64_t getCurrentTimeStamp() {
            // TODO Get the current time from epoch in microseconds
            struct timeval tv_now;
            gettimeofday(&tv_now, NULL);
            uint64_t time_us = (uint64_t)tv_now.tv_sec * 1000000 + (uint64_t)tv_now.tv_usec;
            return time_us;
        }

        void setTimestamp(uint64_t timestamp = DataFrame::getCurrentTimeStamp()) {
            m_timestamp = timestamp;
        }

        virtual void print() {
            Serial.println();
            Serial.println("DataFrame");
            Serial.print("Type: ");Serial.print(m_type); Serial.print(" "); Serial.println(getTypeString());
            Serial.print("Timestamp: ");Serial.println(m_timestamp);
            Serial.print("Data size: ");Serial.println(getDataSize());

            Serial.print("Data: ");

            Serial.print("Data: 0x");
            for (int i = 0; i < getDataSize(); i++) {
                Serial.print(getData()[i], HEX);
                Serial.print(" ");
            }
            Serial.println();
        }

        virtual size_t serialize(uint8_t* buffer, size_t bufferSize) {
            // bufferSize must be at least MAX_FRAME_DATA_SIZE_BYTES + header size
            if (bufferSize < getDataSize() + HEADER_SIZE) {
                return 0;
            }

            // Copy header data
            memcpy(buffer, m_header_data, HEADER_SIZE);

            // Copy data
            memcpy(buffer + HEADER_SIZE, getData(), getDataSize());

            return HEADER_SIZE + m_dataSize;
        }

    protected:
        union {
            uint8_t m_header_data[HEADER_SIZE];
            struct {
                DataFrameType m_type;
                uint64_t m_timestamp;
                uint8_t m_dataSize;
            };
        };

    private:
        DataFrame() = default;
};

typedef DataFrame* DataFramePtr;

class IMUDataFrame : public DataFrame {
    public:

        const static size_t IMU_DATA_FRAME_SIZE = 9 * sizeof(float);

        IMUDataFrame(float *data, uint8_t size, uint64_t timestamp = DataFrame::getCurrentTimeStamp())
            : DataFrame(DataFrame::DATA_FRAME_TYPE_IMU, timestamp) {
            if (data != nullptr && size > 0) {
               setData((uint8_t*)(data), size * sizeof(float));
            }
        }

        IMUDataFrame(const IMUDataFrame& other)
            : DataFrame(other) {
            //Copy member data to avoid const problems
            memcpy(m_data_raw, other.m_data_raw, IMU_DATA_FRAME_SIZE);
        }

        virtual void setData(uint8_t* data, uint8_t size) override {
            if (data == nullptr || size != IMU_DATA_FRAME_SIZE) {
                return;
            }

            memcpy(m_data_raw, data, IMU_DATA_FRAME_SIZE);
        }

        virtual uint8_t* getData() override {
            return m_data_raw;
        }

        virtual size_t getDataSize() const override {
            return IMU_DATA_FRAME_SIZE;
        }

        virtual DataFrame* clone() const override {
            return new IMUDataFrame(*this);
        }

        void setAccel(float x, float y, float z) {
            m_accel[0] = x;
            m_accel[1] = y;
            m_accel[2] = z;
        }

        void setGyro(float x, float y, float z) {
            m_gyro[0] = x;
            m_gyro[1] = y;
            m_gyro[2] = z;
        }

        void setMag(float x, float y, float z) {
            m_mag[0] = x;
            m_mag[1] = y;
            m_mag[2] = z;
        }

        private:

        //Pre allocated memory for IMU data
        union {
            float m_data[IMU_DATA_FRAME_SIZE];
            struct {
                float m_accel[3];
                float m_gyro[3];
                float m_mag[3];
            };
            uint8_t m_data_raw[IMU_DATA_FRAME_SIZE];
        };
};



class ADCDataFrame : public DataFrame {
    public:
        const static size_t ADC_DATA_FRAME_SIZE = 8 * sizeof(float);

        ADCDataFrame(float *data, uint8_t size, uint64_t timestamp = DataFrame::getCurrentTimeStamp())
            : DataFrame(DataFrame::DATA_FRAME_TYPE_ADC, timestamp) {
            if (data != nullptr && size > 0) {
                setData((uint8_t*)(data), size * sizeof(float));
            }
            else {
                memset(m_data_raw, 0, ADC_DATA_FRAME_SIZE);
            }
        }

        ADCDataFrame(const ADCDataFrame& other)
            : DataFrame(other) {
            memcpy(m_data_raw, other.m_data_raw, ADC_DATA_FRAME_SIZE);
        }

        virtual void setData(uint8_t* data, uint8_t size) override {
            if (data == nullptr || size != ADC_DATA_FRAME_SIZE) {
                return;
            }

            memcpy(m_data_raw, data, ADC_DATA_FRAME_SIZE);
        }

        virtual uint8_t* getData() override {
            return m_data_raw;
        }

        virtual DataFrame* clone() const override {
            return new ADCDataFrame(*this);
        }

        float getChannelValue(uint8_t channel) {
            if (channel >= 0 && channel < 8) {
                return m_data[channel];
            }
            return 0;
        }

        void setChannelValue(uint8_t channel, float value) {
            if (channel >= 0 && channel < 8) {
                m_data[channel] = value;
            }
        }

        virtual size_t getDataSize() const override {
            return ADC_DATA_FRAME_SIZE;
        }

    private:

        //Pre allocated memory for IMU data
        union {
            float m_data[ADC_DATA_FRAME_SIZE / sizeof(float)];
            struct {
                float ch0;
                float ch1;
                float ch2;
                float ch3;
                float ch4;
                float ch5;
                float ch6;
                float ch7;
            };
            uint8_t m_data_raw[ADC_DATA_FRAME_SIZE];
        };


};

class PowerDataFrame : public DataFrame {
    public:

        const static size_t POWER_DATA_FRAME_SIZE = 3 * sizeof(float) + sizeof(uint8_t);

        PowerDataFrame(float voltage, float current, float power, uint8_t flags = 0, uint64_t timestamp = DataFrame::getCurrentTimeStamp())
            : DataFrame(DataFrame::DATA_FRAME_TYPE_POWER, timestamp),
            m_voltage(voltage), m_current(current), m_power(power), m_flags(flags) {

        }

        PowerDataFrame(const PowerDataFrame& other)
            : DataFrame(other),
            m_voltage(other.m_voltage), m_current(other.m_current), m_power(other.m_power), m_flags(other.m_flags) {

        }

        float getVoltage() {
            return m_voltage;
        }

        float getCurrent() {
            return m_current;
        }

        float getPower() {
            return m_power;
        }

        uint8_t getFlags() {
            return m_flags;
        }

        virtual void setData(uint8_t* data, uint8_t size) override {
            if (size != POWER_DATA_FRAME_SIZE) {
                return;
            }

            memcpy(m_data_raw, data, POWER_DATA_FRAME_SIZE);
        }

        virtual uint8_t* getData() override {
            return m_data_raw;
        }

        virtual size_t getDataSize() const override {
            return POWER_DATA_FRAME_SIZE;
        }

        virtual DataFrame* clone() const override {
            return new PowerDataFrame(*this);
        }

    protected:
        union {
            uint8_t m_data_raw[POWER_DATA_FRAME_SIZE];
            struct {
                float m_voltage;
                float m_current;
                float m_power;
                uint8_t m_flags;
            };

        };
};

#endif
