#include "WebSocketServerTask.h"
#include "config/GlobalConfig.h"
#include "NextWheelApp.h"

WebSocketServerTask::WebSocketServerTask()
    : WorkerTask("WebSocketServerTask", WEBSOCKET_SERVER_STACK_SIZE)
{
}


void WebSocketServerTask::run(void* app)
{
    Serial.printf("WebSocketServerTask::run Priority: %li Core: %li \n", uxTaskPriorityGet(NULL), xPortGetCoreID());

    // Setup WebSocketServer callbacks
    m_server.onMessage(
        [this](String param, String message)
        {
            // Serial.println("WebSocketServerTask::onMessage");
            // Serial.print("Param: ");Serial.print(param);Serial.print(" Message: ");Serial.println(message);
            if (param == "recording")
            {
                if (message == "start_recording")
                {
                    NextWheelApp::instance()->startRecording();
                }
                else if (message == "stop_recording")
                {
                    NextWheelApp::instance()->stopRecording();
                }
            }
            else if (param == "set_time") {
                NextWheelApp::instance()->setTime(message);
            }
        });

    m_server.begin(GlobalConfig::instance().get());

    TickType_t lastGeneration = xTaskGetTickCount();

    while (1)
    {
        // 100 ms task
        vTaskDelayUntil(&lastGeneration, 100 / portTICK_RATE_MS);

        unsigned int count = 0;
        size_t total_payload_size = 0;
        std::list<DataFramePtr> dataPtrs;

        // Dequeue all values (one shot), no timeout
        while (DataFramePtr dataPtr = dequeue(0))
        {
            // m_ws.send(dataPtr->getData(), dataPtr->getSize());
            count++;
            total_payload_size += dataPtr->getTotalSize();
            dataPtrs.push_back(dataPtr);
        }

        // Serial.println();
        // Serial.print("Sent ");Serial.print(count);Serial.println(" frames") ;
        // Serial.print("Total payload size: ");Serial.println(total_payload_size);

        uint8_t* super_frame = new uint8_t[total_payload_size + DataFrame::HEADER_SIZE];

        uint64_t timestamp = DataFrame::getCurrentTimeStamp();

        super_frame[0] = 255;
        memcpy(super_frame + 1, &timestamp, sizeof(uint64_t));
        super_frame[9] = count;

        size_t offset = DataFrame::HEADER_SIZE;
        for (auto dataPtr : dataPtrs)
        {
            dataPtr->serialize(super_frame + offset, dataPtr->getTotalSize());
            offset += dataPtr->getTotalSize();
            delete dataPtr;
        }

        m_server.sendToAll(super_frame, total_payload_size + DataFrame::HEADER_SIZE);
        delete[] super_frame;
    }
}

void WebSocketServerTask::onMessage(String param, String message)
{
    Serial.println("WebSocketServerTask::onMessage");
    Serial.print("Param: ");
    Serial.print(param);
    Serial.print(" Message: ");
    Serial.println(message);
}
