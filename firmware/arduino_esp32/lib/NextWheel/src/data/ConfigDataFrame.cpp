#include "data/ConfigDataFrame.h"


ConfigDataFrame::ConfigDataFrame(const GlobalConfig::ConfigData& configData, uint64_t timestamp)
    : DataFrame(DataFrame::DATA_FRAME_TYPE_CONFIG, CONFIG_DATA_FRAME_SIZE, timestamp),
      m_configData(configData)
{
}

ConfigDataFrame::ConfigDataFrame(const ConfigDataFrame& other) : DataFrame(other), m_configData(other.m_configData) {}

size_t ConfigDataFrame::serializePayload(uint8_t* buffer, size_t buffer_size) const
{
    if (buffer_size < CONFIG_DATA_FRAME_SIZE)
    {
        return 0;
    }
    memcpy(buffer, &m_configData, CONFIG_DATA_FRAME_SIZE);
    return CONFIG_DATA_FRAME_SIZE;
}

DataFrame* ConfigDataFrame::clone() const
{
    return new ConfigDataFrame(*this);
}
