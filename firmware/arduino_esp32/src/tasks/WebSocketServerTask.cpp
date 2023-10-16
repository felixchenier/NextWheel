#if 0

#include "WebSocketServerTask.h"

#include "config/GlobalConfig.h"
#include "NextWheelApp.h"
#include <esp_task_wdt.h>

WebSocketServerTask::WebSocketServerTask() : WorkerTask("WebSocketServerTask", WEBSOCKET_SERVER_STACK_SIZE)
{

}


void WebSocketServerTask::run(void* app)
{
    Serial.printf("WebSocketServerTask::run Priority: %li Core: %li \n", uxTaskPriorityGet(NULL), xPortGetCoreID());

    m_server.registerWebsocketConnectedHandler([this]() { this->onWebsocketConnected(); });
    m_server.registerWebsocketDisconnectedHandler([this]() { this->onWebsocketDisconnected(); });

    // Setup WebSocketServer callbacks
    m_server.onMessage(
        [this](String param, String message)
        {
            Serial.println("WebSocketServerTask::onMessage");
            Serial.print("Param: ");Serial.print(param);Serial.print(" Message: ");Serial.println(message);
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
            else if (param == "set_time")
            {
                NextWheelApp::instance()->setTime(message);

                //Printing current time
                struct timeval current_time;
                gettimeofday(&current_time, NULL);
                struct tm* time_info = localtime(&current_time.tv_sec);
                Serial.print("Current time: ");
                Serial.println(String(asctime(time_info)));
            }
            else if (param == "config")
            {
                if(message == "config_update")
                {
                    //Send config update event, not from ISR
                    NextWheelApp::instance()->sendConfigUpdateEvent(false);
                }
            }
        });

    m_server.begin(GlobalConfig::instance().get());

    TickType_t lastGeneration = xTaskGetTickCount();

    while (1)
    {

        //First empty the command queue (timeout=0, not waiting)
        //Loop while we have BASE_TASK_COMMAND_NONE --> 0
        while(Task::BaseTaskCommand command = dequeueBaseCommand(0))
        {
            switch(command)
            {
                case Task::BASE_TASK_COMMAND_NONE:
                    Serial.println("WebSocketServerTask::run: BASE_TASK_COMMAND_NONE");
                    break;
                case Task::BASE_TASK_CONFIG_UPDATED:
                    Serial.println("WebSocketServerTask::run: BASE_TASK_CONFIG_UPDATED");

                    // If file is not null means we are recording. We should update the configuration info from now.
                    if (m_server.webSocketClientCount() > 0)
                    {
                        ConfigDataFrame configDataFrame(GlobalConfig::instance().get());
                        m_server.sendToAll(configDataFrame);

                        // Empty the queue (with old config!)
                        while (DataFramePtr dataPtr = dequeue(0))
                        {
                            delete dataPtr;
                        }
                    }
                    break;

                default:
                    Serial.print("WebSocketServerTask::run: Unknown command: ");
                    Serial.println(command);
                break;
            }
        }

       // Then dequeue all data frames and send them to the websocket
        size_t total_payload_size = 0;
        std::list<DataFramePtr> dataPtrs;

        // Dequeue all values (one shot,), no timeout
        //Make sure we have maximum payload of approximately 1400 bytes
        //Otherwize the IP stack will have to fragment the packet and we will have a lot of overhead
        while (DataFramePtr dataPtr = dequeue(50 / portTICK_RATE_MS))
        {
            if (m_server.webSocketClientCount() > 0)
            {
                total_payload_size += dataPtr->getTotalSize();
                dataPtrs.push_back(dataPtr);

                // Enough data for one transmission ?
                // Size 1400 is selected to avoid IP fragmentation
                if (total_payload_size > 1400)
                {
                    break;
                }
            }
            else
            {
                delete dataPtr;
            }
        }

        // Any clients ?
        if (m_server.webSocketClientCount() > 0 && dataPtrs.size() > 0)
        {
            // uint8_t* super_frame = new uint8_t[total_payload_size + DataFrame::HEADER_SIZE];
            // Serial.printf("Should allocate %i bytes\n", total_payload_size + DataFrame::HEADER_SIZE);
            uint8_t super_frame[total_payload_size + DataFrame::HEADER_SIZE];  // Allocate on stack
            uint64_t timestamp = DataFrame::getCurrentTimeStamp();

            super_frame[0] = 255;
            memcpy(super_frame + 1, &timestamp, sizeof(uint64_t));
            super_frame[9] = dataPtrs.size();

            size_t offset = DataFrame::HEADER_SIZE;
            for (auto dataPtr : dataPtrs)
            {
                dataPtr->serialize(super_frame + offset, dataPtr->getTotalSize());
                offset += dataPtr->getTotalSize();
                delete dataPtr;
            }

            // Send to all websockets
            m_server.sendToAll(super_frame, total_payload_size + DataFrame::HEADER_SIZE);


            // Quick sleep, will get back to work soon to continue sending remaining frames.
            // vTaskDelayUntil(&lastGeneration, 50 / portTICK_RATE_MS);

        }
        else
        {
            // Sleep for a while
            vTaskDelayUntil(&lastGeneration, 100 / portTICK_RATE_MS);
        }
    } // while(1)
}

void WebSocketServerTask::onMessage(String param, String message)
{
    Serial.println("WebSocketServerTask::onMessage");
    Serial.print("Param: ");
    Serial.print(param);
    Serial.print(" Message: ");
    Serial.println(message);
}

void WebSocketServerTask::onWebsocketConnected()
{
    Serial.println("WebSocketServerTask::onWebsocketConnected");
    NextWheelApp::instance()->registerSensorTasksToWebSocketServer();
}

void WebSocketServerTask::onWebsocketDisconnected()
{
    Serial.println("WebSocketServerTask::onWebsocketDisconnected");
    NextWheelApp::instance()->unregisterSensorTasksFromWebSocketServer();
}

bool WebSocketServerTask::isWebSocketConnected()
{
    return m_server.webSocketClientCount() > 0;
}

#endif
