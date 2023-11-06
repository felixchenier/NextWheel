#include "GlobalConfig.h"

#include <algorithm>
#include "IMU.h"

const std::vector<uint32_t> GlobalConfig::m_accel_ranges =
    {IMU::IMU_ACC_RANGE_2G, IMU::IMU_ACC_RANGE_4G, IMU::IMU_ACC_RANGE_8G, IMU::IMU_ACC_RANGE_16G};

const std::vector<uint32_t> GlobalConfig::m_gyro_ranges =
    {IMU::IMU_GYR_RANGE_250DPS, IMU::IMU_GYR_RANGE_500DPS, IMU::IMU_GYR_RANGE_1000DPS, IMU::IMU_GYR_RANGE_2000DPS};

const std::vector<uint32_t> GlobalConfig::m_mag_ranges = {IMU::IMU_MAG_RANGE_2500uGAUSS};

const std::vector<uint32_t> GlobalConfig::m_imu_sampling_rate_ranges = {60, 120, 240};
const std::vector<uint32_t> GlobalConfig::m_adc_sampling_rate_ranges = {120, 240, 480, 960, 1000, 2000};


void GlobalConfig::begin()
{
    EEPROM.begin(sizeof(ConfigData));
    load();
    print();
}

void GlobalConfig::load()
{
    EEPROM.get(0, m_config);
    if (!validate())
    {
        setDefault();
    }
}

void GlobalConfig::print()
{
    Serial.println("GlobalConfig:");
    Serial.print("accel_range: ");
    Serial.println(m_config.accel_range);
    Serial.print("gyro_range: ");
    Serial.println(m_config.gyro_range);
    Serial.print("mag_range: ");
    Serial.println(m_config.mag_range);
    Serial.print("imu_sample_rate: ");
    Serial.println(m_config.imu_sample_rate);
    Serial.print("adc_sample_rate: ");
    Serial.println(m_config.adc_sample_rate);
}

void GlobalConfig::save()
{
    EEPROM.put(0, m_config);
    EEPROM.commit();
}

GlobalConfig::ConfigData GlobalConfig::get() const
{
    return m_config;
}

void GlobalConfig::set(GlobalConfig::ConfigData data)
{
    m_config = data;
    save();
}


void GlobalConfig::set_accel_range(unsigned int range)
{
    m_config.accel_range = range;
    save();
}

uint32_t GlobalConfig::get_accel_range() const
{
    return m_config.accel_range;
}

void GlobalConfig::set_gyro_range(unsigned int range)
{
    m_config.gyro_range = range;
    save();
}

uint32_t GlobalConfig::get_gyro_range() const
{
    return m_config.gyro_range;
}

void GlobalConfig::set_mag_range(unsigned int range)
{
    m_config.mag_range = range;
    save();
}

uint32_t GlobalConfig::get_mag_range() const
{
    return m_config.mag_range;
}

void GlobalConfig::set_imu_sample_rate(unsigned int rate)
{
    m_config.imu_sample_rate = rate;
    save();
}

uint32_t GlobalConfig::get_imu_sample_rate() const
{
    return m_config.imu_sample_rate;
}

void GlobalConfig::set_adc_sample_rate(unsigned int rate)
{
    m_config.adc_sample_rate = rate;
    save();
}

uint32_t GlobalConfig::get_adc_sample_rate() const
{
    return m_config.adc_sample_rate;
}

void GlobalConfig::setDefault()
{
    Serial.println("GlobalConfig : Setting default config");
    m_config.accel_range = m_accel_ranges[0];
    m_config.gyro_range = m_gyro_ranges[0];
    m_config.mag_range = m_mag_ranges[0];
    m_config.imu_sample_rate = m_imu_sampling_rate_ranges[0];
    m_config.adc_sample_rate = m_adc_sampling_rate_ranges[0];
    save();
}

// Singleton instance
GlobalConfig& GlobalConfig::instance()
{
    static GlobalConfig instance;
    return instance;
}


bool GlobalConfig::validate()
{
    if (std::find(m_accel_ranges.begin(), m_accel_ranges.end(), m_config.accel_range) == m_accel_ranges.end())
    {
        return false;
    }

    if (std::find(m_gyro_ranges.begin(), m_gyro_ranges.end(), m_config.gyro_range) == m_gyro_ranges.end())
    {
        return false;
    }

    if (std::find(m_mag_ranges.begin(), m_mag_ranges.end(), m_config.mag_range) == m_mag_ranges.end())
    {
        return false;
    }

    if (std::find(m_imu_sampling_rate_ranges.begin(), m_imu_sampling_rate_ranges.end(), m_config.imu_sample_rate) ==
        m_imu_sampling_rate_ranges.end())
    {
        return false;
    }

    if (std::find(m_adc_sampling_rate_ranges.begin(), m_adc_sampling_rate_ranges.end(), m_config.adc_sample_rate) ==
        m_adc_sampling_rate_ranges.end())
    {
        return false;
    }

    return true;
}
