#ifndef _ADC_SENSOR_TASK_H_
#define _ADC_SENSR_TASK_H_

#include "tasks/SensorTask.h"
#include "data/ADCDataFrame.h"
#include "ADC.h"

class ADCSensorTask : public SensorTask
{
public:
    ADCSensorTask() : SensorTask("ADCSensorTask") {}

    virtual void run(void* app) override
    {
        Serial.printf("ADCTask::run Priority: %li Core: %li \n", uxTaskPriorityGet(NULL), xPortGetCoreID());

        m_adc.begin();
        TickType_t lastGeneration = xTaskGetTickCount();
        ADCDataFrame frame;

        while (1)
        {
            // 1 ms task
            vTaskDelayUntil(&lastGeneration, 1 / portTICK_RATE_MS);

            // Update values
            m_adc.update(frame);

            // Send data to registered queues
            sendData(frame);
        }
    }

private:
    ADC m_adc;
};
#endif  // _ADC_TASK_H_