#ifndef _IMU_H_
#define _IMU_H_

#include <NextWheel.h>
#include <DFRobot_BMX160.h>

#define IMU_I2C_ADDRESS 0x68

class IMU {
    public:
        IMU(unsigned char address = IMU_I2C_ADDRESS);
        void begin();
        void update();

    private:
        unsigned char m_i2c_address;
        DFRobot_BMX160 m_bmx160;
};

#endif // _IMU_H_
