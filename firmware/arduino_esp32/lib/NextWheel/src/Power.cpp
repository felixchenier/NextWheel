#include "Power.h"

Power::Power(unsigned char address) : m_i2c_address(address)
{
    // SET PIN AS INPUT
    pinMode(PIN_EMERGENCY_STOP_LOW_POWER_N, INPUT);
    pinMode(PIN_ENABLE_SENSOR_POWER, OUTPUT);

    enableSensors(false);
}

void Power::begin()
{
    enableSensors(true);

    // Initialize the INA220
    uint8_t availableDevices = m_ina220.begin(
        MAX_CUR,
        SHUNT_R,
        INA_ADC_MODE_128AVG,
        INA_ADC_MODE_128AVG,
        INA_MODE_CONTINUOUS_BOTH,
        &m_i2c_address,
        NUM_INA);
    Serial.print("Configured ");
    Serial.print(availableDevices);
    Serial.print(" of ");
    Serial.print(NUM_INA);
    Serial.println(" INA220 current sensors");
}


void Power::update(PowerDataFrame& frame)
{
    float voltage = m_ina220.getBusMilliVolts(0) / 1000.0;
    float current = m_ina220.getBusMicroAmps(0) / 1000000.0;
    float power = m_ina220.getBusMicroWatts(0) / 1000000.0;

    uint8_t flags = isLowPower() ? 0b00000001 : 0;
    flags |= isSensorsEnabled() ? 0b00000010 : 0;

    frame.setAll(voltage, current, power, flags);
    frame.setTimestamp(DataFrame::getCurrentTimeStamp());
}

bool Power::isLowPower()
{
    return digitalRead(PIN_EMERGENCY_STOP_LOW_POWER_N) == LOW;
}

bool Power::isSensorsEnabled()
{
    return digitalRead(PIN_ENABLE_SENSOR_POWER) == HIGH;
}

void Power::enableSensors(bool enabled)
{
    Serial.print("Enabling sensors: ");
    Serial.println(enabled);
    digitalWrite(PIN_ENABLE_SENSOR_POWER, enabled ? HIGH : LOW);
}