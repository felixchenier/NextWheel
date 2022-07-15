#ifndef _IMU_H_
#define _IMU_H_

#include <NextWheel.h>
#include <drivers/DPEng_BMX160.h>
#include "data/IMUDataFrame.h"

#define IMU_I2C_ADDRESS 0x68

class IMU
{
public:

    typedef enum {
        IMU_ACC_RANGE_2G = 2,
        IMU_ACC_RANGE_4G = 4,
        IMU_ACC_RANGE_8G = 8,
        IMU_ACC_RANGE_16G = 16,
    } IMU_ACCEL_RANGE;

    typedef enum {
        IMU_GYR_RANGE_250DPS = 250,
        IMU_GYR_RANGE_500DPS = 500,
        IMU_GYR_RANGE_1000DPS = 1000,
        IMU_GYR_RANGE_2000DPS = 2000,
    } IMU_GYRO_RANGE;

    typedef enum {
        IMU_MAG_RANGE_2500uGAUSS = 2500,
    } IMU_MAG_RANGE;


    IMU(unsigned char address = IMU_I2C_ADDRESS);
    void begin(IMU_ACCEL_RANGE acc_range, IMU_GYRO_RANGE gyr_range);
    void update(IMUDataFrame& frame);
    void displaySensorDetails();

private:
    void displaySensorDetails(const sensor_t &sensor);
    DPEng::bmx160AccelRange_t convert_acc_range(IMU_ACCEL_RANGE acc_range);
    DPEng::bmx160GyroRange_t convert_gyr_range(IMU_GYRO_RANGE gyr_range);
    unsigned char m_i2c_address;
    DPEng::DPEng_BMX160 m_dpeng_bmx160;
};

#endif  // _IMU_H_
