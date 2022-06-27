#ifndef _IMU_H_
#define _IMU_H_

#include <NextWheel.h>
#include <DPEng_BMX160.h>
#include "DataFrame.h"

#define IMU_I2C_ADDRESS 0x68

class IMU
{
public:
    IMU(unsigned char address = IMU_I2C_ADDRESS);
    void begin();
    void update(IMUDataFrame& frame);
    void displaySensorDetails();

private:
    unsigned char m_i2c_address;
    DPEng::DPEng_BMX160 m_dpeng_bmx160;
};

#endif  // _IMU_H_
