#include "IMUSensorTask.h"
#include "config/GlobalConfig.h"

void IMUSensorTask::run(void* app)
{
    Serial.printf("IMUSensorTask::run Priority: %li Core: %li \n", uxTaskPriorityGet(NULL), xPortGetCoreID());

    IMU imu;

    imu.begin((IMU::IMU_ACCEL_RANGE)GlobalConfig::instance().get_accel_range(), (IMU::IMU_GYRO_RANGE)GlobalConfig::instance().get_gyro_range());

    TickType_t lastGeneration = xTaskGetTickCount();
    IMUDataFrame frame;

    uint32_t tick_increment =  1000 / (portTICK_RATE_MS * GlobalConfig::instance().get_imu_sample_rate());

    Serial.print("IMUSensorTask sample_rate: ");
    Serial.println(GlobalConfig::instance().get_imu_sample_rate());
    Serial.print("IMUSensorTask tick_increment: ");
    Serial.println(tick_increment);

    while (1)
    {
        // 10 ms task 10 / portTICK_RATE_MS
        vTaskDelayUntil(&lastGeneration, tick_increment);

        // Update values
        imu.update(frame);

        // Send data to registered queues
        sendData(frame);
    }
}