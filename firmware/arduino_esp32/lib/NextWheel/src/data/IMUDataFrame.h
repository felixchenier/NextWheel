#ifndef _IMU_DATA_FRAME_H_
#define _IMU_DATA_FRAME_H_

#include "data/DataFrame.h"

class IMUDataFrame : public DataFrame
{
public:
    const static size_t IMU_AXIS_COUNT = 9;
    const static size_t IMU_DATA_FRAME_SIZE = IMU_AXIS_COUNT * sizeof(float);

    IMUDataFrame(uint64_t timestamp = DataFrame::getCurrentTimeStamp())
        : DataFrame(DataFrame::DATA_FRAME_TYPE_IMU, IMU_DATA_FRAME_SIZE, timestamp)
    {
        memset(m_data, 0, IMU_DATA_FRAME_SIZE);
    }

    IMUDataFrame(const IMUDataFrame& other) : DataFrame(other)
    {
        // Copy member data to avoid const problems
        memcpy(m_data, other.m_data, IMU_DATA_FRAME_SIZE);
    }

    virtual size_t serializePayload(uint8_t* buffer, size_t buffer_size) const override
    {
        memcpy(buffer, m_data, IMU_DATA_FRAME_SIZE);
        return IMU_DATA_FRAME_SIZE;
    }

    virtual DataFrame* clone() const override { return new IMUDataFrame(*this); }

    void setAccel(float x, float y, float z)
    {
        m_accel[0] = x;
        m_accel[1] = y;
        m_accel[2] = z;
    }

    void setGyro(float x, float y, float z)
    {
        m_gyro[0] = x;
        m_gyro[1] = y;
        m_gyro[2] = z;
    }

    void setMag(float x, float y, float z)
    {
        m_mag[0] = x;
        m_mag[1] = y;
        m_mag[2] = z;
    }

private:
    // Pre allocated memory for IMU data
    union
    {
        float m_data[IMU_AXIS_COUNT];
        struct
        {
            float m_accel[3];
            float m_gyro[3];
            float m_mag[3];
        };
    };
};

#endif  // _IMU_DATA_FRAME_H_