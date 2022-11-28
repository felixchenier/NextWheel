#include "IMUSensorTask.h"
#include "config/GlobalConfig.h"


namespace NextWheelInterrupts {
    SemaphoreHandle_t g_imu_semaphore;
    void IRAM_ATTR imu_sensor_task_timer_interrupt(){
         xSemaphoreGiveFromISR(NextWheelInterrupts::g_imu_semaphore, NULL);
    }
}// namespace NextWheel



IMUSensorTask::IMUSensorTask() : SensorTask("IMUSensorTask") {
     NextWheelInterrupts::g_imu_semaphore = xSemaphoreCreateCounting(1,0);
}

void IMUSensorTask::run(void* app)
{
    Serial.printf("IMUSensorTask::run Priority: %li Core: %li \n", uxTaskPriorityGet(NULL), xPortGetCoreID());
    Serial.print("IMUSensorTask sample_rate: ");
    Serial.println(GlobalConfig::instance().get_imu_sample_rate());

    IMU imu;

    imu.begin(
        (IMU::IMU_ACCEL_RANGE)GlobalConfig::instance().get_accel_range(),
        (IMU::IMU_GYRO_RANGE)GlobalConfig::instance().get_gyro_range());


    IMUDataFrame frame;

    auto imu_timer = timerBegin(1, 80, true); //count up. 80 prescaler = 1us resolution
    timerAttachInterrupt(imu_timer, &NextWheelInterrupts::imu_sensor_task_timer_interrupt, false); // Attach interrupt function
    timerAlarmWrite(imu_timer, 1000000 / GlobalConfig::instance().get_imu_sample_rate(), true); // us timer calculation
    timerAlarmEnable(imu_timer);

    while (1)
    {
        // IMU update will be triggered by timer interrupt
        xSemaphoreTake(NextWheelInterrupts::g_imu_semaphore, portMAX_DELAY);

        // Update values
        imu.update(frame);

        // Send data to registered queues
        sendData(frame);
    }

    timerAlarmDisable(imu_timer);
    timerEnd(imu_timer);
}