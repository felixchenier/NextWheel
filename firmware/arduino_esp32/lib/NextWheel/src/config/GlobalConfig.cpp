#include "GlobalConfig.h"

#include <algorithm>

const std::vector<unsigned int> GlobalConfig::m_accel_ranges = {2, 4, 8, 16};
const std::vector<unsigned int> GlobalConfig::m_gyro_ranges = {250, 500, 1000, 2000};
const std::vector<unsigned int> GlobalConfig::m_mag_ranges = {2500};
const std::vector<unsigned int> GlobalConfig::m_imu_sampling_rate_ranges = {10, 50, 100, 200};
const std::vector<unsigned int> GlobalConfig::m_adc_sampling_rate_ranges = {10, 50, 100, 200, 400, 800, 1000};


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

    if (std::find(m_imu_sampling_rate_ranges.begin(), m_imu_sampling_rate_ranges.end(), m_config.imu_sample_rate) == m_imu_sampling_rate_ranges.end())
    {
        return false;
    }

    if (std::find(m_adc_sampling_rate_ranges.begin(), m_adc_sampling_rate_ranges.end(), m_config.adc_sample_rate) == m_adc_sampling_rate_ranges.end())
    {
        return false;
    }

    return true;
}