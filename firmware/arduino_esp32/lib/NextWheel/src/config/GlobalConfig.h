#ifndef _GLOBAL_CONFIG_H_
#define _GLOBAL_CONFIG_H_

#include "NextWheel.h"

#include <Arduino.h>
#include <EEPROM.h>
#include <vector>

class GlobalConfig
{
 public:

    static const std::vector<unsigned int> m_accel_ranges;
    static const std::vector<unsigned int> m_gyro_ranges;
    static const std::vector<unsigned int> m_mag_ranges;
    static const std::vector<unsigned int> m_imu_sampling_rate_ranges;
    static const std::vector<unsigned int> m_adc_sampling_rate_ranges;

    typedef struct {
        unsigned int accel_range;
        unsigned int gyro_range;
        unsigned int mag_range;
        unsigned int imu_sample_rate;
        unsigned int adc_sample_rate;
    } ConfigData;


    GlobalConfig() = default;
    ~GlobalConfig() = default;

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

    ConfigData get() {
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

    void set_gyro_range(unsigned int range) {
        m_config.gyro_range = range;
        save();
    }

    void set_mag_range(unsigned int range) {
        m_config.mag_range = range;
        save();
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

    private:
        ConfigData m_config;


};

#endif // _GLOBAL_CONFIG_H_