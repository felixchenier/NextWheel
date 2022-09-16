#include "DACActuatorTask.h"

DACActuatorTask::DACActuatorTask(const char* name, uint32_t stackSize, uint8_t priority)
    : Task(name, stackSize, priority)
{
    m_dac.setup();
}

void DACActuatorTask::run(void *)
{
    Serial.printf("DACActuatorTask::run Priority: %li Core: %li \n", uxTaskPriorityGet(NULL), xPortGetCoreID());


    TickType_t lastGeneration = xTaskGetTickCount();
    uint32_t tick_increment = portTICK_RATE_MS * 1;
    Serial.print("DACActuatorTask tick_increment: ");
    Serial.println(tick_increment);

    const int frequency = 880; // frequency of square wave in Hz
    const int amplitude = 16000; // amplitude of square wave
    const int sampleRate = 8000; // sample rate in Hz
    const int bps = 16;

    const int halfWavelength = (sampleRate / frequency); // half wavelength of square wave
    short sample = amplitude; // current sample value
    int count = 0;


    while (1)
    {
        // 1 ms task
        vTaskDelayUntil(&lastGeneration, tick_increment);


        /*

        // Writing 8 samples at a time (8khz * 1ms = 8 samples)
        for (auto i = 0; i < 8; i++)
        {
            if (count % halfWavelength == 0 )
            {
                // invert the sample every half wavelength count multiple to generate square wave
                sample = -1 * sample;
            }

            I2S.write(sample);

            // increment the counter for the next sample
            count++;
        }

        */
        if (++count % 2 == 0)
        {
           m_dac.setVoltage(0); //(VDD * 100 / 255)
        }
        else
        {
            m_dac.setVoltage(100); //(VDD * 100 / 255)
        }
    }
}