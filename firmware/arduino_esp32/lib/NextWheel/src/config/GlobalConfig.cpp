#include "GlobalConfig.h"

#include <algorithm>
#include "IMU.h"

const std::vector<uint32_t> GlobalConfig::m_accel_ranges =
    {IMU::IMU_ACC_RANGE_2G, IMU::IMU_ACC_RANGE_4G, IMU::IMU_ACC_RANGE_8G, IMU::IMU_ACC_RANGE_16G};

const std::vector<uint32_t> GlobalConfig::m_gyro_ranges =
    {IMU::IMU_GYR_RANGE_250DPS, IMU::IMU_GYR_RANGE_500DPS, IMU::IMU_GYR_RANGE_1000DPS, IMU::IMU_GYR_RANGE_2000DPS};

const std::vector<uint32_t> GlobalConfig::m_mag_ranges = {IMU::IMU_MAG_RANGE_2500uGAUSS};

const std::vector<uint32_t> GlobalConfig::m_imu_sampling_rate_ranges = {25, 50, 100, 200, 400 /*, 800, 1600*/};
const std::vector<uint32_t> GlobalConfig::m_adc_sampling_rate_ranges = {25, 50, 100, 200, 400, 800, 1000};


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