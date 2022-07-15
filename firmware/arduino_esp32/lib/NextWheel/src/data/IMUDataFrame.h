#ifndef _IMU_DATA_FRAME_H_
#define _IMU_DATA_FRAME_H_

#include "data/DataFrame.h"

class IMUDataFrame : public DataFrame
{
public:
    const static size_t IMU_AXIS_COUNT = 9;
    const static size_t IMU_DATA_FRAME_SIZE = IMU_AXIS_COUNT * sizeof(float);

    IMUDataFrame(uint64_t timestamp = DataFrame::getCurrentTimeStamp());

    IMUDataFrame(const IMUDataFrame& other);

    virtual size_t serializePayload(uint8_t* buffer, size_t buffer_size) const override;

    virtual DataFrame* clone() const override;

    void setAccel(float x, float y, float z);

    void setGyro(float x, float y, float z);

    void setMag(float x, float y, float z);

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