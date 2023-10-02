#include "DACActuatorTask.h"

//#include "I2S.h"

/**
 * @brief Scale data to 16bit/32bit for I2S DMA output.
 *        DAC can only output 8bit data value.
 *        I2S DMA will still send 16 bit or 32bit data, the highest 8bit contains DAC data.
 */
int example_i2s_dac_data_scale(uint8_t* d_buff, uint8_t* s_buff, uint32_t len)
{
    uint32_t j = 0;
    for (int i = 0; i < len; i++) {
        d_buff[j++] = 0;
        d_buff[j++] = s_buff[i];
    }
    return (len * 2);
}


DACActuatorTask::DACActuatorTask(const char* name, uint32_t stackSize, uint8_t priority)
    : Task(name, stackSize, priority)
{
    m_dac.setup();
}

void DACActuatorTask::run(void *)
{
    Serial.printf("DACActuatorTask::run Priority: %li Core: %li \n", uxTaskPriorityGet(NULL), xPortGetCoreID());
    const uint32_t sampling_rate = m_dac.getSampleRate();
    const uint32_t frequency = 400;
    TickType_t lastGeneration = xTaskGetTickCount();
    uint32_t tick_increment = portTICK_RATE_MS * 1;
    Serial.print("DACActuatorTask tick_increment: ");
    Serial.println(tick_increment);


    size_t index = 0;

    uint8_t stereo_buffer[4] = {0,0,0,0}; //Right, left
    while (1)
    {
        uint16_t sample =  uint16_t(120.0 * sin(2 * M_PI * (double)frequency * (double)index++ / (double)sampling_rate) + 120.0);
        //uint16_t sample = 0;
        //Serial.printf("DACActuatorTask::run sample: i: %i %u \n", index, sample);

        //DAC will only use the MSB
        // Right channel
        stereo_buffer[0] = 0;
        stereo_buffer[1] = (sample) & 0xFF;

        // Left channel
        //stereo_buffer[2] = 0;
        //stereo_buffer[3] = sample & 0xFF;

        //Write to DAC (will wait if buffer is full)
        // Only using right channel
        m_dac.writeFrame(stereo_buffer, sizeof(stereo_buffer) / 2);
    }
}
