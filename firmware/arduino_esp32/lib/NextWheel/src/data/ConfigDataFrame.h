#ifndef _CONFIG_DATA_FRAME_H_
#define _CONFIG_DATA_FRAME_H_

#include <data/DataFrame.h>
#include <config/GlobalConfig.h>

class ConfigDataFrame : public DataFrame
{
public:
    const static size_t CONFIG_DATA_FRAME_SIZE = sizeof(GlobalConfig::ConfigData);

    ConfigDataFrame(
        const GlobalConfig& config,
        uint64_t timestamp = DataFrame::getCurrentTimeStamp())
        : DataFrame(DataFrame::DATA_FRAME_TYPE_CONFIG, CONFIG_DATA_FRAME_SIZE, timestamp), m_configData(config.get())
    {
    }

    ConfigDataFrame(
        const GlobalConfig::ConfigData& configData,
        uint64_t timestamp = DataFrame::getCurrentTimeStamp())
        : DataFrame(DataFrame::DATA_FRAME_TYPE_CONFIG, CONFIG_DATA_FRAME_SIZE, timestamp), m_configData(configData)
    {
    }

    ConfigDataFrame(const ConfigDataFrame& other)
        : DataFrame(other), m_configData(other.m_configData)
    {
    }

    virtual size_t serializePayload(uint8_t* buffer, size_t buffer_size) const override
    {
        if (buffer_size < CONFIG_DATA_FRAME_SIZE)
        {
            return 0;
        }
        memcpy(buffer, &m_configData, CONFIG_DATA_FRAME_SIZE);
        return CONFIG_DATA_FRAME_SIZE;
    }


    virtual DataFrame* clone() const override { return new ConfigDataFrame(*this); }

protected:

    GlobalConfig::ConfigData m_configData;
};

#endif // _CONFIG_DATA_FRAME_H_
