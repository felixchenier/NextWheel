#ifndef _IMU_SENSOR_TASK_H_
#define _IMU_SENSOR_TASK_H_

#include "tasks/SensorTask.h"

#include "IMU.h"

class IMUSensorTask : public SensorTask
{
public:
    IMUSensorTask() : SensorTask("IMUSensorTask") {}

    virtual void run(void* app) override
    {
        Serial.printf("IMUSensorTask::run Priority: %li Core: %li \n", uxTaskPriorityGet(NULL), xPortGetCoreID());

        IMU imu;

        imu.begin();
        TickType_t lastGeneration = xTaskGetTickCount();
        IMUDataFrame frame;

        while (1)
        {
            // 10 ms task
            vTaskDelayUntil(&lastGeneration, 10 / portTICK_RATE_MS);

            // Update values
            imu.update(frame);

            // Send data to registered queues
            sendData(frame);
        }
    }
};

#endif  // _IMU_SENSOR_TASK_H_
