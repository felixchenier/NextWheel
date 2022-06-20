#include "IMU.h"
#include "DataFrame.h"

IMU::IMU(unsigned char address)
:   m_i2c_address(address), m_dpeng_bmx160(0x160A, 0x160B, 0x160C)
{

}

void IMU::begin() {
    // Initialize the IMU
    if(!m_dpeng_bmx160.begin(DPEng::BMX160_ACCELRANGE_4G, DPEng::GYRO_RANGE_250DPS))
    {
        /* There was a problem detecting the BMX160 ... check your connections */
        Serial.println("Ooops, no BMX160 detected ... Check your wiring!");
        while(1);
    }

    displaySensorDetails();
}

void IMU::displaySensorDetails()
{
    sensor_t accel, gyro, mag;
    m_dpeng_bmx160.getSensor(&accel, &gyro, &mag);
    Serial.println("------------------------------------");
    Serial.println("ACCELEROMETER");
    Serial.println("------------------------------------");
    Serial.print  ("Sensor:       "); Serial.println(accel.name);
    Serial.print  ("Driver Ver:   "); Serial.println(accel.version);
    Serial.print  ("Unique ID:    0x"); Serial.println(accel.sensor_id, HEX);
    Serial.print  ("Min Delay:    "); Serial.print(accel.min_delay); Serial.println(" s");
    Serial.print  ("Max Value:    "); Serial.print(accel.max_value, 4); Serial.println(" m/s^2");
    Serial.print  ("Min Value:    "); Serial.print(accel.min_value, 4); Serial.println(" m/s^2");
    Serial.print  ("Resolution:   "); Serial.print(accel.resolution, 8); Serial.println(" m/s^2");
    Serial.println("------------------------------------");
    Serial.println("");
    Serial.println("------------------------------------");
    Serial.println("GYROSCOPE");
    Serial.println("------------------------------------");
    Serial.print  ("Sensor:       "); Serial.println(gyro.name);
    Serial.print  ("Driver Ver:   "); Serial.println(gyro.version);
    Serial.print  ("Unique ID:    0x"); Serial.println(gyro.sensor_id, HEX);
    Serial.print  ("Min Delay:    "); Serial.print(accel.min_delay); Serial.println(" s");
    Serial.print  ("Max Value:    "); Serial.print(gyro.max_value); Serial.println(" g");
    Serial.print  ("Min Value:    "); Serial.print(gyro.min_value); Serial.println(" g");
    Serial.print  ("Resolution:   "); Serial.print(gyro.resolution); Serial.println(" g");
    Serial.println("------------------------------------");
    Serial.println("");
    Serial.println("------------------------------------");
    Serial.println("MAGNETOMETER");
    Serial.println("------------------------------------");
    Serial.print  ("Sensor:       "); Serial.println(mag.name);
    Serial.print  ("Driver Ver:   "); Serial.println(mag.version);
    Serial.print  ("Unique ID:    0x"); Serial.println(mag.sensor_id, HEX);
    Serial.print  ("Min Delay:    "); Serial.print(accel.min_delay); Serial.println(" s");
    Serial.print  ("Max Value:    "); Serial.print(mag.max_value); Serial.println(" uTesla");
    Serial.print  ("Min Value:    "); Serial.print(mag.min_value); Serial.println(" uTesla");
    Serial.print  ("Resolution:   "); Serial.print(mag.resolution); Serial.println(" uTesla");
    Serial.println("------------------------------------");
    Serial.println("");
    delay(500);
}

void IMU::update(IMUDataFrame &frame) {
    sensors_event_t aevent, gevent, mevent;

    /* Get a new sensor event */
    m_dpeng_bmx160.getEvent(&aevent, &gevent, &mevent);
    frame.setAccel(aevent.acceleration.x, aevent.acceleration.y, aevent.acceleration.z);
    frame.setGyro(gevent.gyro.x, gevent.gyro.y, gevent.gyro.z);
    frame.setMag(mevent.magnetic.x, mevent.magnetic.y, mevent.magnetic.z);
}
