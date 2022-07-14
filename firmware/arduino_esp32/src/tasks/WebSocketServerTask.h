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

   virtual void run(void* app) override;


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
