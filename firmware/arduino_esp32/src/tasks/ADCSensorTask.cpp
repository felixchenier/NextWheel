#include "ADCSensorTask.h"
#include "config/GlobalConfig.h"

ADCSensorTask::ADCSensorTask() : SensorTask("ADCSensorTask") {}


void ADCSensorTask::run(void* app)
{
    Serial.printf("ADCTask::run Priority: %li Core: %li \n", uxTaskPriorityGet(NULL), xPortGetCoreID());
    m_adc.begin();
    TickType_t lastGeneration = xTaskGetTickCount();
    ADCDataFrame frame;

    uint32_t tick_increment = 1000 / (portTICK_RATE_MS * GlobalConfig::instance().get_adc_sample_rate());

    Serial.print("ADCSensorTask sample_rate: ");
    Serial.println(GlobalConfig::instance().get_imu_sample_rate());
    Serial.print("ADCSensorTask tick_increment: ");
    Serial.println(tick_increment);

    while (1)
    {
        // 1 ms task
        vTaskDelayUntil(&lastGeneration, tick_increment);

        // Update values
        m_adc.update(frame);

        // Send data to registered queues
        sendData(frame);
    }
}