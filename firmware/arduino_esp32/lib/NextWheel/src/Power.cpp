#include "Power.h"
#include "DataFrame.h"

Power::Power(unsigned char address)
: m_i2c_address(address) {

    //SET PIN AS INPUT
    pinMode(PIN_EMERGENCY_STOP_LOW_POWER_N, INPUT);
    pinMode(PIN_ENABLE_SENSOR_POWER, OUTPUT);

    enableSensors(true);
}

void Power::begin() {
  // Initialize the INA220
  uint8_t availableDevices = m_ina220.begin(MAX_CUR, SHUNT_R, INA_ADC_MODE_128AVG, INA_ADC_MODE_128AVG, INA_MODE_CONTINUOUS_BOTH, &m_i2c_address, NUM_INA);
  Serial.print("Configured "); Serial.print(availableDevices); Serial.print(" of "); Serial.print(NUM_INA); Serial.println(" INA220 current sensors");

}


void Power::update() {

    float vol = m_ina220.getBusMilliVolts(0) / 1000.0;
    float cur = m_ina220.getBusMicroAmps(0) / 1000.0;
    float power = m_ina220.getBusMicroWatts(0) / 1000.0;

    uint8_t flags = isLowPower() ? 0b00000001 : 0;
    flags |= isSensorsEnabled() ? 0b00000010 : 0;

    PowerDataFrame frame(vol, cur, power, flags);
    frame.print();

}

bool Power::isLowPower() {
  return digitalRead(PIN_EMERGENCY_STOP_LOW_POWER_N) == LOW;
}

bool Power::isSensorsEnabled()
{
    return digitalRead(PIN_ENABLE_SENSOR_POWER) == HIGH;
}

void Power::enableSensors(bool enabled)
{
    digitalWrite(PIN_ENABLE_SENSOR_POWER, enabled ? HIGH : LOW);
}