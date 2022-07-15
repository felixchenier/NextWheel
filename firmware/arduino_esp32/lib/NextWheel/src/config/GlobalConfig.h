#ifndef _GLOBAL_CONFIG_H_
#define _GLOBAL_CONFIG_H_

#include "NextWheel.h"

#include <Arduino.h>
#include <EEPROM.h>
#include <vector>

class GlobalConfig
{
 public:


    typedef struct {
        uint32_t accel_range;
        uint32_t gyro_range;
        uint32_t mag_range;
        uint32_t imu_sample_rate;
        uint32_t adc_sample_rate;
    } ConfigData;



    void begin() {
        EEPROM.begin(sizeof(ConfigData));
        load();
        print();
    }

    void load() {
        EEPROM.get(0, m_config);
        if (!validate())
        {
            setDefault();
        }
    }

    void print() {
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

    void save() {
        EEPROM.put(0, m_config);
        EEPROM.commit();
    }

    ConfigData get() const {
        return m_config;
    }

    void set(ConfigData data) {
        m_config = data;
        save();
    }

    bool validate();

    void set_accel_range(unsigned int range) {
        m_config.accel_range = range;
        save();
    }

    uint32_t get_accel_range() const {
        return m_config.accel_range;
    }

    void set_gyro_range(unsigned int range) {
        m_config.gyro_range = range;
        save();
    }

    uint32_t get_gyro_range() const {
        return m_config.gyro_range;
    }

    void set_mag_range(unsigned int range) {
        m_config.mag_range = range;
        save();
    }

    uint32_t get_mag_range() const {
        return m_config.mag_range;
    }

    void set_imu_sample_rate(unsigned int rate) {
        m_config.imu_sample_rate = rate;
        save();
    }

    uint32_t get_imu_sample_rate() const {
        return m_config.imu_sample_rate;
    }

    void set_adc_sample_rate(unsigned int rate) {
        m_config.adc_sample_rate = rate;
        save();
    }

    uint32_t get_adc_sample_rate() const {
        return m_config.adc_sample_rate;
    }

    void setDefault() {
        Serial.println("GlobalConfig : Setting default config");
        m_config.accel_range = m_accel_ranges[0];
        m_config.gyro_range = m_gyro_ranges[0];
        m_config.mag_range = m_mag_ranges[0];
        m_config.imu_sample_rate = m_imu_sampling_rate_ranges[0];
        m_config.adc_sample_rate = m_adc_sampling_rate_ranges[0];
        save();
    }

    // Singleton instance
    static GlobalConfig& instance() {
        static GlobalConfig instance;
        return instance;
    }

    private:
        ConfigData m_config;
        GlobalConfig() = default;
        ~GlobalConfig() = default;

        //Vectors containing valid configuration values
        static const std::vector<uint32_t> m_accel_ranges;
        static const std::vector<uint32_t> m_gyro_ranges;
        static const std::vector<uint32_t> m_mag_ranges;
        static const std::vector<uint32_t> m_imu_sampling_rate_ranges;
        static const std::vector<uint32_t> m_adc_sampling_rate_ranges;


};

#endif // _GLOBAL_CONFIG_H_