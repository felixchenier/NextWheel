#include "QuadEncoderSensorTask.h"
#include "config/GlobalConfig.h"
#include "data/QuadEncoderDataFrame.h"

QuadEncoderSensorTask::QuadEncoderSensorTask() : SensorTask("QuadEncoderSensorTask") {}


void QuadEncoderSensorTask::run(void* app)
{
    Serial.printf("QuadEncoderSensorTask::run Priority: %li Core: %li \n", uxTaskPriorityGet(NULL), xPortGetCoreID());

    TickType_t lastGeneration = xTaskGetTickCount();

    // Setup encoder
    m_encoder.attachFullQuad(PIN_QUAD_ENCODER_A, PIN_QUAD_ENCODER_B);
    m_encoder.clearCount();

    QuadEncoderDataFrame frame;

    while (1)
    {
        // 1000 ms task
        vTaskDelayUntil(&lastGeneration, 1000 / portTICK_RATE_MS);

        // Save encoder value
        int64_t count = m_encoder.getCount();

        // Reset counter
        m_encoder.clearCount();

        // Serial.print("encoder counts: ");
        // Serial.println(count);

        // Update timestamp and value
        frame.setTimestamp(DataFrame::getCurrentTimeStamp());
        frame.setCount(count);
        // Send data to registered queues
        sendData(frame);
    }
}