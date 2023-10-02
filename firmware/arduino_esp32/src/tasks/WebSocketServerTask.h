#ifndef _WEBSOCKET_SERVER_TASK_H_
#define _WEBSOCKET_SERVER_TASK_H_

#include "config/WiFiConfig.h"
#include "tasks/WorkerTask.h"
#include "WebSocketServer.h"
#include <string.h>
#include <list>

class WebSocketServerTask : public WorkerTask
{
    static const size_t WEBSOCKET_SERVER_STACK_SIZE = 12000;

public:
    WebSocketServerTask();
    virtual void run(void* app) override;


protected:
    void onMessage(String param, String message);
    void onWebsocketConnected();
    void onWebsocketDisconnected();

    WebSocketServer m_server;

};

#endif  // _WEBSOCKET_SERVER_TASK_H_
