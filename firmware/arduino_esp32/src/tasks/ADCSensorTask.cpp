#include "ADCSensorTask.h"
#include "config/GlobalConfig.h"


namespace NextWheelInterrupts {
    SemaphoreHandle_t g_adc_semaphore;
    void IRAM_ATTR adc_sensor_task_timer_interrupt(){
         xSemaphoreGiveFromISR(NextWheelInterrupts::g_adc_semaphore, NULL);
    }
}// namespace NextWheel

ADCSensorTask::ADCSensorTask() : SensorTask("ADCSensorTask") {
    NextWheelInterrupts::g_adc_semaphore = xSemaphoreCreateCounting(1,0);
}


void ADCSensorTask::run(void* app)
{
    Serial.printf("ADCTask::run Priority: %li Core: %li \n", uxTaskPriorityGet(NULL), xPortGetCoreID());
    Serial.print("ADCSensorTask sample_rate: ");
    Serial.println(GlobalConfig::instance().get_imu_sample_rate());

    m_adc.begin();
    ADCDataFrame frame;

    auto adc_timer = timerBegin(0, 80, true); //count up. 80 prescaler = 1us resolution
    timerAttachInterrupt(adc_timer, &NextWheelInterrupts::adc_sensor_task_timer_interrupt, false); // Attach interrupt function
    timerAlarmWrite(adc_timer, 1000000 / GlobalConfig::instance().get_adc_sample_rate(), true); // us timer calculation
    timerAlarmEnable(adc_timer);

    while (1)
    {
        // ADC update will be triggered by timer interrupt
        xSemaphoreTake(NextWheelInterrupts::g_adc_semaphore, portMAX_DELAY);

        // Update values
        m_adc.update(frame);

        // Send data to registered queues
        sendData(frame);


    }

    timerAlarmDisable(adc_timer);
    timerEnd(adc_timer);
}