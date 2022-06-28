#ifndef _POWER_SENSOR_TASK_H_
#define _POWER_SENSOR_TASK_H_


#include "tasks/SensorTask.h"
#include "data/PowerDataFrame.h"
#include "Power.h"


class PowerSensorTask : public SensorTask
{
public:
    PowerSensorTask() : SensorTask("PowerSensorTask") {}

    virtual void run(void* app) override
    {
        Serial.printf("PowerSensorTask::run Priority: %li Core: %li \n", uxTaskPriorityGet(NULL), xPortGetCoreID());

        m_power.begin();
        TickType_t lastGeneration = xTaskGetTickCount();
        PowerDataFrame frame;

        while (1)
        {
            // 1000 ms task
            vTaskDelayUntil(&lastGeneration, 1000 / portTICK_RATE_MS);

            // Update values
            m_power.update(frame);

            // Send data to registered queues
            sendData(frame);
        }
    }

private:
    Power m_power;
};

#endif  // _POWER_SENSOR_TASK_H_
