#include "PowerSensorTask.h"

PowerSensorTask::PowerSensorTask() : SensorTask("PowerSensorTask") {}

void PowerSensorTask::run(void* app)
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