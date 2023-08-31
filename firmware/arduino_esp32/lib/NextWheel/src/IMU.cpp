#include "IMU.h"

IMU::IMU(unsigned char address) : m_i2c_address(address), m_dpeng_bmx160(0x160A, 0x160B, 0x160C) {}

void IMU::begin(IMU_ACCEL_RANGE acc_range, IMU_GYRO_RANGE gyr_range)
{
    // Initialize the IMU
    if (!m_dpeng_bmx160.begin(convert_acc_range(acc_range), convert_gyr_range(gyr_range)))
    {
        /* There was a problem detecting the BMX160 ... check your connections */
        Serial.println("Ooops, no BMX160 detected ... Check your wiring!");
        while (1)
            ;
    }

    displaySensorDetails();
}

void IMU::displaySensorDetails()
{
    sensor_t accel, gyro, mag;
    m_dpeng_bmx160.getSensor(&accel, &gyro, &mag);
    displaySensorDetails(accel);
    displaySensorDetails(gyro);
    displaySensorDetails(mag);
}

void IMU::displaySensorDetails(const sensor_t& sensor)
{
    // This is a copy of the printSensorDetails() function in the Adafruit Sensor library
    Serial.println(F("------------------------------------"));
    Serial.print(F("Sensor:       "));
    Serial.println(sensor.name);
    Serial.print(F("Type:         "));
    switch ((sensors_type_t)sensor.type)
    {
        case SENSOR_TYPE_ACCELEROMETER:
            Serial.print(F("Acceleration (m/s2)"));
            break;
        case SENSOR_TYPE_MAGNETIC_FIELD:
            Serial.print(F("Magnetic (uT)"));
            break;
        case SENSOR_TYPE_ORIENTATION:
            Serial.print(F("Orientation (degrees)"));
            break;
        case SENSOR_TYPE_GYROSCOPE:
            Serial.print(F("Gyroscopic (deg/s)"));
            break;
        case SENSOR_TYPE_LIGHT:
            Serial.print(F("Light (lux)"));
            break;
        case SENSOR_TYPE_PRESSURE:
            Serial.print(F("Pressure (hPa)"));
            break;
        case SENSOR_TYPE_PROXIMITY:
            Serial.print(F("Distance (cm)"));
            break;
        case SENSOR_TYPE_GRAVITY:
            Serial.print(F("Gravity (m/s2)"));
            break;
        case SENSOR_TYPE_LINEAR_ACCELERATION:
            Serial.print(F("Linear Acceleration (m/s2)"));
            break;
        case SENSOR_TYPE_ROTATION_VECTOR:
            Serial.print(F("Rotation vector"));
            break;
        case SENSOR_TYPE_RELATIVE_HUMIDITY:
            Serial.print(F("Relative Humidity (%)"));
            break;
        case SENSOR_TYPE_AMBIENT_TEMPERATURE:
            Serial.print(F("Ambient Temp (C)"));
            break;
        case SENSOR_TYPE_OBJECT_TEMPERATURE:
            Serial.print(F("Object Temp (C)"));
            break;
        case SENSOR_TYPE_VOLTAGE:
            Serial.print(F("Voltage (V)"));
            break;
        case SENSOR_TYPE_CURRENT:
            Serial.print(F("Current (mA)"));
            break;
        case SENSOR_TYPE_COLOR:
            Serial.print(F("Color (RGBA)"));
            break;
    }

    Serial.println();
    Serial.print(F("Driver Ver:   "));
    Serial.println(sensor.version);
    Serial.print(F("Unique ID:    "));
    Serial.println(sensor.sensor_id);
    Serial.print(F("Min Value:    "));
    Serial.println(sensor.min_value);
    Serial.print(F("Max Value:    "));
    Serial.println(sensor.max_value);
    Serial.print(F("Resolution:   "));
    Serial.println(sensor.resolution);
    Serial.println(F("------------------------------------\n"));
}

void IMU::update(IMUDataFrame& frame)
{
    sensors_event_t aevent, gevent, mevent;

    /* Get a new sensor event */
    m_dpeng_bmx160.getEvent(&aevent, &gevent, &mevent);

    // Raw data is stored in the m_dpeng_bmx160 object
    frame.setAccel(m_dpeng_bmx160.accel_raw.x, m_dpeng_bmx160.accel_raw.y, m_dpeng_bmx160.accel_raw.z);
    frame.setGyro(m_dpeng_bmx160.gyro_raw.x, m_dpeng_bmx160.gyro_raw.y, m_dpeng_bmx160.gyro_raw.z);
    frame.setMag(m_dpeng_bmx160.mag_raw.x, m_dpeng_bmx160.mag_raw.y, m_dpeng_bmx160.mag_raw.z);

    // Converted data is stored in the aevent, gevent, and mevent objects
    //frame.setAccel(aevent.acceleration.x, aevent.acceleration.y, aevent.acceleration.z);
    //frame.setGyro(gevent.gyro.x, gevent.gyro.y, gevent.gyro.z);
    //frame.setMag(mevent.magnetic.x, mevent.magnetic.y, mevent.magnetic.z);

    // Update timestamp to now
    frame.setTimestamp(DataFrame::getCurrentTimeStamp());
}


DPEng::bmx160AccelRange_t IMU::convert_acc_range(IMU_ACCEL_RANGE acc_range)
{
    switch (acc_range)
    {
        case IMU::IMU_ACC_RANGE_2G:
            return DPEng::BMX160_ACCELRANGE_2G;
            break;
        case IMU::IMU_ACC_RANGE_4G:
            return DPEng::BMX160_ACCELRANGE_4G;
            break;
        case IMU::IMU_ACC_RANGE_8G:
            return DPEng::BMX160_ACCELRANGE_8G;
            break;
        case IMU::IMU_ACC_RANGE_16G:
            return DPEng::BMX160_ACCELRANGE_16G;
            break;
    }
    // Default value
    return DPEng::BMX160_ACCELRANGE_2G;
}

DPEng::bmx160GyroRange_t IMU::convert_gyr_range(IMU_GYRO_RANGE gyr_range)
{
    switch (gyr_range)
    {
        case IMU_GYR_RANGE_250DPS:
            return DPEng::GYRO_RANGE_250DPS;
            break;
        case IMU_GYR_RANGE_500DPS:
            return DPEng::GYRO_RANGE_500DPS;
            break;
        case IMU_GYR_RANGE_1000DPS:
            return DPEng::GYRO_RANGE_1000DPS;
            break;
        case IMU_GYR_RANGE_2000DPS:
            return DPEng::GYRO_RANGE_2000DPS;
            break;
    }
    // Default value
    return DPEng::GYRO_RANGE_250DPS;
}
