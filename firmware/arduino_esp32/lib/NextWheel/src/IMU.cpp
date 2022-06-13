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

void IMU::update() {
    sensors_event_t aevent, gevent, mevent;
    DataFrame<float> frame(DATA_FRAME_TYPE_IMU, nullptr, 9);

    /* Get a new sensor event */
    m_dpeng_bmx160.getEvent(&aevent, &gevent, &mevent);
    frame.setDataItem(0, aevent.acceleration.x);
    frame.setDataItem(1, aevent.acceleration.y);
    frame.setDataItem(2, aevent.acceleration.z);
    frame.setDataItem(3, gevent.gyro.x);
    frame.setDataItem(4, gevent.gyro.y);
    frame.setDataItem(5, gevent.gyro.z);
    frame.setDataItem(6, mevent.magnetic.x);
    frame.setDataItem(7, mevent.magnetic.y);
    frame.setDataItem(8, mevent.magnetic.z);





    /* Display the accel results (acceleration is measured in m/s^2) */
    Serial.print("A ");
    Serial.print("X: "); Serial.print(aevent.acceleration.x, 4); Serial.print("  ");
    Serial.print("Y: "); Serial.print(aevent.acceleration.y, 4); Serial.print("  ");
    Serial.print("Z: "); Serial.print(aevent.acceleration.z, 4); Serial.print("  ");
    Serial.println("m/s^2");

    /* Display the gyro results (gyro data is in g) */
    Serial.print("G ");
    Serial.print("X: "); Serial.print(gevent.gyro.x, 1); Serial.print("  ");
    Serial.print("Y: "); Serial.print(gevent.gyro.y, 1); Serial.print("  ");
    Serial.print("Z: "); Serial.print(gevent.gyro.z, 1); Serial.print("  ");
    Serial.println("g");

    /* Display the mag results (mag data is in uTesla) */
    Serial.print("M ");
    Serial.print("X: "); Serial.print(mevent.magnetic.x, 1); Serial.print("  ");
    Serial.print("Y: "); Serial.print(mevent.magnetic.y, 1); Serial.print("  ");
    Serial.print("Z: "); Serial.print(mevent.magnetic.z, 1); Serial.print("  ");
    Serial.println("uT");

    Serial.println("");
    frame.print();
}
