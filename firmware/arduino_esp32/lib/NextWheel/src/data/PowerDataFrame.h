#ifndef _POWER_DATA_FRAME_H_
#define _POWER_DATA_FRAME_H_

#include "data/DataFrame.h"

class PowerDataFrame : public DataFrame
{
public:
    const static size_t POWER_DATA_FRAME_SIZE = 3 * sizeof(float) + sizeof(uint8_t);

    PowerDataFrame(
        float voltage,
        float current,
        float power,
        uint8_t flags = 0,
        uint64_t timestamp = DataFrame::getCurrentTimeStamp())
        : DataFrame(DataFrame::DATA_FRAME_TYPE_POWER, POWER_DATA_FRAME_SIZE, timestamp),
          m_voltage(voltage),
          m_current(current),
          m_power(power),
          m_flags(flags)
    {
    }

    PowerDataFrame(uint64_t timestamp = DataFrame::getCurrentTimeStamp())
        : DataFrame(DataFrame::DATA_FRAME_TYPE_POWER, POWER_DATA_FRAME_SIZE, timestamp)
    {
    }

    PowerDataFrame(const PowerDataFrame& other)
        : DataFrame(other),
          m_voltage(other.m_voltage),
          m_current(other.m_current),
          m_power(other.m_power),
          m_flags(other.m_flags)
    {
    }

    virtual size_t serializePayload(uint8_t* buffer, size_t buffer_size) const override
    {
        memcpy(buffer, &m_voltage, sizeof(float));
        memcpy(buffer + sizeof(float), &m_current, sizeof(float));
        memcpy(buffer + 2 * sizeof(float), &m_power, sizeof(float));
        buffer[3 * sizeof(float)] = m_flags;
        return POWER_DATA_FRAME_SIZE;
    }

    void setVoltage(float voltage) { m_voltage = voltage; }

    void setCurrent(float current) { m_current = current; }

    void setPower(float power) { m_power = power; }

    void setFlags(uint8_t flags) { m_flags = flags; }

    void setAll(float voltage, float current, float power, uint8_t flags)
    {
        m_voltage = voltage;
        m_current = current;
        m_power = power;
        m_flags = flags;
    }

    float getVoltage() { return m_voltage; }

    float getCurrent() { return m_current; }

    float getPower() { return m_power; }

    uint8_t getFlags() { return m_flags; }

    virtual DataFrame* clone() const override { return new PowerDataFrame(*this); }

protected:
    float m_voltage;
    float m_current;
    float m_power;
    uint8_t m_flags;
};

#endif  // _POWER_DATA_FRAME_H_