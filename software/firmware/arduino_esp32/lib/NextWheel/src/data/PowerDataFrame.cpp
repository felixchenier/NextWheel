#include "data/PowerDataFrame.h"

PowerDataFrame::PowerDataFrame(float voltage, float current, float power, uint8_t flags, uint64_t timestamp)
    : DataFrame(DataFrame::DATA_FRAME_TYPE_POWER, POWER_DATA_FRAME_SIZE, timestamp),
      m_voltage(voltage),
      m_current(current),
      m_power(power),
      m_flags(flags)
{
}

PowerDataFrame::PowerDataFrame(uint64_t timestamp)
    : DataFrame(DataFrame::DATA_FRAME_TYPE_POWER, POWER_DATA_FRAME_SIZE, timestamp)
{
}

PowerDataFrame::PowerDataFrame(const PowerDataFrame& other)
    : DataFrame(other),
      m_voltage(other.m_voltage),
      m_current(other.m_current),
      m_power(other.m_power),
      m_flags(other.m_flags)
{
}

size_t PowerDataFrame::serializePayload(uint8_t* buffer, size_t buffer_size) const
{
    memcpy(buffer, &m_voltage, sizeof(float));
    memcpy(buffer + sizeof(float), &m_current, sizeof(float));
    memcpy(buffer + 2 * sizeof(float), &m_power, sizeof(float));
    buffer[3 * sizeof(float)] = m_flags;
    return POWER_DATA_FRAME_SIZE;
}

void PowerDataFrame::setVoltage(float voltage)
{
    m_voltage = voltage;
}

void PowerDataFrame::setCurrent(float current)
{
    m_current = current;
}

void PowerDataFrame::setPower(float power)
{
    m_power = power;
}

void PowerDataFrame::setFlags(uint8_t flags)
{
    m_flags = flags;
}

void PowerDataFrame::setAll(float voltage, float current, float power, uint8_t flags)
{
    m_voltage = voltage;
    m_current = current;
    m_power = power;
    m_flags = flags;
}

float PowerDataFrame::getVoltage()
{
    return m_voltage;
}

float PowerDataFrame::getCurrent()
{
    return m_current;
}

float PowerDataFrame::getPower()
{
    return m_power;
}

uint8_t PowerDataFrame::getFlags()
{
    return m_flags;
}

DataFrame* PowerDataFrame::clone() const
{
    return new PowerDataFrame(*this);
}
