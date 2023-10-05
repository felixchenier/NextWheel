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
        //First empty the command queue (timeout=0, not waiting)
        //Loop while we have BASE_TASK_COMMAND_NONE --> 0
        while(Task::BaseTaskCommand command = dequeueBaseCommand(0))
        {
            switch(command)
            {
                case Task::BASE_TASK_COMMAND_NONE:
                    Serial.println("PowerSensorTask::run: BASE_TASK_COMMAND_NONE");
                    break;
                case Task::BASE_TASK_CONFIG_UPDATED:
                    Serial.println("PowerSensorTask::run: BASE_TASK_CONFIG_UPDATED");
                    break;
                default:
                    Serial.print("PowerSensorTask::run: Unknown command: ");
                    Serial.println(command);
                break;
            }
        }

        // 1000 ms task
        vTaskDelayUntil(&lastGeneration, 1000 / portTICK_RATE_MS);

        // Update values
        m_power.update(frame);

        // Send data to registered queues
        sendData(frame);
    }
}
