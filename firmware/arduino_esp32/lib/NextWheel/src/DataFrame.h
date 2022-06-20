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
            DATA_FRAME_TYPE_RTC = 5,
            DATA_FRAME_TYPE_AUDIO = 6
        };

        DataFrame(DataFrameType type, uint16_t data_size, uint64_t timestamp = DataFrame::getCurrentTimeStamp())
            : m_type(type), m_dataSize(data_size), m_timestamp(timestamp) {

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

        size_t getHeaderSize() {
            return HEADER_SIZE;
        }

        size_t getTotalSize() const {
            return HEADER_SIZE + getDataSize();
        }

        size_t getDataSize() const {
            return m_dataSize;
        }

        virtual size_t serializePayload(uint8_t *buffer, size_t buffer_size) const = 0;


        virtual DataFrame* clone() const = 0;

        static uint64_t getCurrentTimeStamp() {
            // TODO Get the current time from epoch in microseconds
            struct timeval tv_now;
            gettimeofday(&tv_now, NULL);
            uint64_t time_us = (uint64_t)tv_now.tv_sec * 1000000L + (uint64_t)tv_now.tv_usec;
            return time_us;
        }

        void setTimestamp(uint64_t timestamp = DataFrame::getCurrentTimeStamp()) {
            m_timestamp = timestamp;
        }

        virtual void print() {

            uint8_t buffer[getTotalSize()];
            serialize(buffer, getTotalSize());


            Serial.println();
            Serial.println("DataFrame");
            Serial.print("Type: ");Serial.print(m_type); Serial.print(" "); Serial.println(getTypeString());
            Serial.print("Timestamp: ");Serial.println(m_timestamp);
            Serial.print("Data size: ");Serial.println(getDataSize());

            Serial.print("Header: 0x");
            for (int i = 0; i < getHeaderSize(); i++) {
                Serial.printf("%2.2x", buffer[i]);
                Serial.print(" ");
            }

            Serial.print("Data: 0x");
            for (int i = getHeaderSize(); i < getTotalSize(); i++) {
                Serial.printf("%2.2x", buffer[i]);
                Serial.print(" ");
            }
            Serial.println();
        }

        virtual size_t serialize(uint8_t* buffer, size_t bufferSize) const {
            // bufferSize must be at least MAX_FRAME_DATA_SIZE_BYTES + header size
            if (bufferSize < getTotalSize()) {
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

class IMUDataFrame : public DataFrame {
    public:

        const static size_t IMU_AXIS_COUNT = 9;
        const static size_t IMU_DATA_FRAME_SIZE = IMU_AXIS_COUNT * sizeof(float);

        IMUDataFrame(uint64_t timestamp = DataFrame::getCurrentTimeStamp())
            : DataFrame(DataFrame::DATA_FRAME_TYPE_IMU, IMU_DATA_FRAME_SIZE, timestamp) {

            memset(m_data,0, IMU_DATA_FRAME_SIZE);
        }

        IMUDataFrame(const IMUDataFrame& other)
            : DataFrame(other) {
            //Copy member data to avoid const problems
            memcpy(m_data, other.m_data, IMU_DATA_FRAME_SIZE);
        }

        virtual size_t serializePayload(uint8_t *buffer, size_t buffer_size) const override {

            memcpy(buffer, m_data, IMU_DATA_FRAME_SIZE);
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
            float m_data[IMU_AXIS_COUNT];
            struct {
                float m_accel[3];
                float m_gyro[3];
                float m_mag[3];
            };
        };
};



class ADCDataFrame : public DataFrame {
    public:
        const static size_t NUM_ADC_CHANNELS = 8;
        const static size_t ADC_DATA_FRAME_SIZE = NUM_ADC_CHANNELS * sizeof(float);

        ADCDataFrame(uint64_t timestamp = DataFrame::getCurrentTimeStamp())
            : DataFrame(DataFrame::DATA_FRAME_TYPE_ADC, ADC_DATA_FRAME_SIZE, timestamp) {

            memset(m_data, 0, ADC_DATA_FRAME_SIZE);
        }

        ADCDataFrame(const ADCDataFrame& other)
            : DataFrame(other) {
            memcpy(m_data, other.m_data, ADC_DATA_FRAME_SIZE);
        }

        virtual size_t serializePayload(uint8_t *buffer, size_t buffer_size) const override {

            memcpy(buffer, m_data, ADC_DATA_FRAME_SIZE);
            return ADC_DATA_FRAME_SIZE;
        }

        virtual DataFrame* clone() const override {
            return new ADCDataFrame(*this);
        }

        float getChannelValue(uint8_t channel) {
            if (channel >= 0 && channel < NUM_ADC_CHANNELS) {
                return m_data[channel];
            }
            return 0;
        }

        void setChannelValue(uint8_t channel, float value) {
            if (channel >= 0 && channel < NUM_ADC_CHANNELS) {
                m_data[channel] = value;
            }
        }

        virtual void print() override {
            DataFrame::print();
            Serial.print("ADC Data: ");
            for (int i = 0; i < NUM_ADC_CHANNELS; i++) {
                Serial.print(m_data[i]);
                Serial.print(" ");
            }
            Serial.println();
        }

    private:

        float m_data[NUM_ADC_CHANNELS];
};

class PowerDataFrame : public DataFrame {
    public:

        const static size_t POWER_DATA_FRAME_SIZE = 3 * sizeof(float) + sizeof(uint8_t);

        PowerDataFrame(float voltage, float current, float power, uint8_t flags = 0, uint64_t timestamp = DataFrame::getCurrentTimeStamp())
            : DataFrame(DataFrame::DATA_FRAME_TYPE_POWER, POWER_DATA_FRAME_SIZE, timestamp),
            m_voltage(voltage), m_current(current), m_power(power), m_flags(flags) {

        }

        PowerDataFrame(uint64_t timestamp = DataFrame::getCurrentTimeStamp())
        : DataFrame(DataFrame::DATA_FRAME_TYPE_POWER, POWER_DATA_FRAME_SIZE, timestamp) {

        }

        PowerDataFrame(const PowerDataFrame& other)
            : DataFrame(other),
            m_voltage(other.m_voltage), m_current(other.m_current), m_power(other.m_power), m_flags(other.m_flags) {

        }

        virtual size_t serializePayload(uint8_t *buffer, size_t buffer_size) const override {

            memcpy(buffer, &m_voltage, sizeof(float));
            memcpy(buffer + sizeof(float), &m_current, sizeof(float));
            memcpy(buffer + 2 * sizeof(float), &m_power, sizeof(float));
            buffer[3 * sizeof(float)] = m_flags;
            return POWER_DATA_FRAME_SIZE;
        }

        void setVoltage(float voltage) {
            m_voltage = voltage;
        }

        void setCurrent(float current) {
            m_current = current;
        }

        void setPower(float power) {
            m_power = power;
        }

        void setFlags(uint8_t flags) {
            m_flags = flags;
        }

        void setAll(float voltage, float current, float power, uint8_t flags) {
            m_voltage = voltage;
            m_current = current;
            m_power = power;
            m_flags = flags;
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

        virtual DataFrame* clone() const override {
            return new PowerDataFrame(*this);
        }

    protected:

        float m_voltage;
        float m_current;
        float m_power;
        uint8_t m_flags;
};

#endif
