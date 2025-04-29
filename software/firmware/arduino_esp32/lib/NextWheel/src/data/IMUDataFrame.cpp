#include "data/IMUDataFrame.h"

IMUDataFrame::IMUDataFrame(uint64_t timestamp)
    : DataFrame(DataFrame::DATA_FRAME_TYPE_IMU, IMU_DATA_FRAME_SIZE, timestamp)
{
    memset(m_data, 0, IMU_DATA_FRAME_SIZE);
}

IMUDataFrame::IMUDataFrame(const IMUDataFrame& other) : DataFrame(other)
{
    // Copy member data to avoid const problems
    memcpy(m_data, other.m_data, IMU_DATA_FRAME_SIZE);
}

size_t IMUDataFrame::serializePayload(uint8_t* buffer, size_t buffer_size) const
{
    memcpy(buffer, m_data, IMU_DATA_FRAME_SIZE);
    return IMU_DATA_FRAME_SIZE;
}

DataFrame* IMUDataFrame::clone() const
{
    return new IMUDataFrame(*this);
}

void IMUDataFrame::setAccel(int16_t x, int16_t y, int16_t z)
{
    m_accel[0] = x;
    m_accel[1] = y;
    m_accel[2] = z;
}

void IMUDataFrame::setGyro(int16_t x, int16_t y, int16_t z)
{
    m_gyro[0] = x;
    m_gyro[1] = y;
    m_gyro[2] = z;
}

void IMUDataFrame::setMag(int16_t x, int16_t y, int16_t z)
{
    m_mag[0] = x;
    m_mag[1] = y;
    m_mag[2] = z;
}
