#ifndef _IMU_DATA_FRAME_H_
#define _IMU_DATA_FRAME_H_

#include "data/DataFrame.h"

class IMUDataFrame : public DataFrame
{
public:
    const static size_t IMU_AXIS_COUNT = 9;
    const static size_t IMU_DATA_FRAME_SIZE = IMU_AXIS_COUNT * sizeof(int16_t);

    IMUDataFrame(uint64_t timestamp = DataFrame::getCurrentTimeStamp());

    IMUDataFrame(const IMUDataFrame& other);

    virtual size_t serializePayload(uint8_t* buffer, size_t buffer_size) const override;

    virtual DataFrame* clone() const override;

    void setAccel(int16_t x, int16_t y, int16_t z);

    void setGyro(int16_t x, int16_t y, int16_t z);

    void setMag(int16_t x, int16_t y, int16_t z);

private:
    // Pre allocated memory for IMU data
    union
    {
        int16_t m_data[IMU_AXIS_COUNT];
        struct
        {
            int16_t m_accel[3];
            int16_t m_gyro[3];
            int16_t m_mag[3];
        };
    };
};

#endif  // _IMU_DATA_FRAME_H_
