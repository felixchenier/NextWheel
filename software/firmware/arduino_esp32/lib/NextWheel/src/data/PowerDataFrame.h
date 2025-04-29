#ifndef _POWER_DATA_FRAME_H_
#define _POWER_DATA_FRAME_H_

#include "data/DataFrame.h"

/**
 * @brief Data frame for power data, units are in Volt, Ampere and Watt.
 */
class PowerDataFrame : public DataFrame
{
public:
    const static size_t POWER_DATA_FRAME_SIZE = 3 * sizeof(float) + sizeof(uint8_t);

    PowerDataFrame(
        float voltage,
        float current,
        float power,
        uint8_t flags = 0,
        uint64_t timestamp = DataFrame::getCurrentTimeStamp());

    PowerDataFrame(uint64_t timestamp = DataFrame::getCurrentTimeStamp());

    PowerDataFrame(const PowerDataFrame& other);

    virtual size_t serializePayload(uint8_t* buffer, size_t buffer_size) const override;

    void setVoltage(float voltage);
    void setCurrent(float current);
    void setPower(float power);
    void setFlags(uint8_t flags);
    void setAll(float voltage, float current, float power, uint8_t flags);

    float getVoltage();
    float getCurrent();
    float getPower();
    uint8_t getFlags();

    virtual DataFrame* clone() const override;

protected:
    float m_voltage;
    float m_current;
    float m_power;
    uint8_t m_flags;
};

#endif  // _POWER_DATA_FRAME_H_
