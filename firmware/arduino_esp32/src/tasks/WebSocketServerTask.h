#ifndef _WEBSOCKET_SERVER_TASK_H_
#define _WEBSOCKET_SERVER_TASK_H_

#include "config/WiFiConfig.h"
#include "tasks/WorkerTask.h"
#include "tasks/SDCardWorkerTask.h"
#include "WebSocketServer.h"
#include <string.h>
#include <list>

class WebSocketServerTask : public WorkerTask
{
    static const size_t WEBSOCKET_SERVER_STACK_SIZE = 16000;

public:
    WebSocketServerTask(SDCardWorkerTask* sdcardTask)
        : WorkerTask("WebSocketServerTask", WEBSOCKET_SERVER_STACK_SIZE),
          m_sdCardWorkerTask(sdcardTask)
    {
    }


    virtual void run(void* app) override
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
                        m_sdCardWorkerTask->sendCommandEvent(
                            SDCardWorkerTask::SDCARD_WORKER_TASK_COMMAND_START_RECORDING);
                    }
                    else if (message == "stop_recording")
                    {
                        m_sdCardWorkerTask->sendCommandEvent(
                            SDCardWorkerTask::SDCARD_WORKER_TASK_COMMAND_STOP_RECORDING);
                    }
                }
            });

        m_server.begin();

        TickType_t lastGeneration = xTaskGetTickCount();

        while (1)
        {
            // 40 ms task
            vTaskDelayUntil(&lastGeneration, 40 / portTICK_RATE_MS);

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

protected:
    void onMessage(String param, String message)
    {
        Serial.println("WebSocketServerTask::onMessage");
        Serial.print("Param: ");
        Serial.print(param);
        Serial.print(" Message: ");
        Serial.println(message);
    }

    WebSocketServer m_server;
    SDCardWorkerTask* m_sdCardWorkerTask;
};

#endif  // _WEBSOCKET_SERVER_TASK_H_
