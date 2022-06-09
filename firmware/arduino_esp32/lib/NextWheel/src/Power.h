#ifndef _POWER_H_
#define _POWER_H_

#include <NextWheel.h>
#include <INA220.h>

#define INA220_I2C_ADDRESS 0x40

class Power {
    public:
        Power(unsigned char address = INA220_I2C_ADDRESS);
        void begin();
        void update();
        bool isLowPower();

    private:
        unsigned char m_i2c_address;
        INA220 m_ina220;
        const uint8_t NUM_INA = 1; // 1 INA devices
        const uint8_t MAX_CUR = 5; // 5 Amps
        const uint16_t SHUNT_R = 20000; // 20 mOhm
};

#endif // _POWER_H_
