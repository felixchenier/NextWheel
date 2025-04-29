#ifndef _CONFIG_DATA_FRAME_H_
#define _CONFIG_DATA_FRAME_H_

#include <data/DataFrame.h>
#include <config/GlobalConfig.h>

class ConfigDataFrame : public DataFrame
{
public:
    const static size_t CONFIG_DATA_FRAME_SIZE = sizeof(GlobalConfig::ConfigData);

    ConfigDataFrame(const GlobalConfig::ConfigData& configData, uint64_t timestamp = DataFrame::getCurrentTimeStamp());

    ConfigDataFrame(const ConfigDataFrame& other);

    virtual size_t serializePayload(uint8_t* buffer, size_t buffer_size) const override;

    virtual DataFrame* clone() const override;

protected:
    GlobalConfig::ConfigData m_configData;
};

#endif  // _CONFIG_DATA_FRAME_H_
