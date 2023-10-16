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
#ifdef _USE_INTERNAL_DAC_
    m_dac.setup();
#else
    //Standard PWM init
    //enable PWM ouput on GPIO25
    ledcSetup(0, 2000, 8);
    ledcAttachPin(PIN_SPI_CS2, 0);
    ledcWrite(0,0); // Ch:0, Duty:0

#endif
}

void DACActuatorTask::run(void *)
{
    Serial.printf("DACActuatorTask::run Priority: %li Core: %li \n", uxTaskPriorityGet(NULL), xPortGetCoreID());

#ifdef _USE_INTERNAL_DAC_
    const uint32_t sampling_rate = m_dac.getSampleRate();
    const uint32_t frequency = 400;
    size_t index = 0;
    uint8_t stereo_buffer[4] = {0,0,0,0}; //Right, left

#else
    //Standard PWM
    TickType_t lastGeneration = xTaskGetTickCount();
#endif

    //Common part, read base commnd

    while (1)
    {
        //First empty the command queue (timeout=0, not waiting)
        //Loop while we have BASE_TASK_COMMAND_NONE --> 0
        while(Task::BaseTaskCommand command = dequeueBaseCommand(0))
        {
            switch(command)
            {
                case Task::BASE_TASK_COMMAND_NONE:
                    Serial.println("DACActuatorTask::run: BASE_TASK_COMMAND_NONE");
                    break;
                case Task::BASE_TASK_CONFIG_UPDATED:
                    Serial.println("DACActuatorTask::run: BASE_TASK_CONFIG_UPDATED");
                    break;
                default:
                    Serial.print("DACActuatorTask::run: Unknown command: ");
                    Serial.println(command);
                break;
            }
        }

#ifdef _USE_INTERNAL_DAC_

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

#else
     // 1000 ms task
    vTaskDelayUntil(&lastGeneration, 1000 / portTICK_RATE_MS);
    ledcWrite(0,128);

#endif

    }// while(1)
} // run
