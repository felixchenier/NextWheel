#ifndef _WEBSOCKET_SERVER_TASK_V2_H_
#define _WEBSOCKET_SERVER_TASK_V2_H_

#include "config/WiFiConfig.h"
#include "tasks/WorkerTask.h"
#include <NextWheel.h>
#include <data/DataFrame.h>
#include <data/ConfigDataFrame.h>
#include <string.h>
#include <list>
#include <WebSocketsServer.h>
#include <WebServer.h>



class WebSocketServerTask_v2 : public WorkerTask
{
    static const size_t WEBSOCKET_SERVER_STACK_SIZE = 12000;

public:
    WebSocketServerTask_v2();
    virtual void run(void* app) override;
    bool isWebSocketConnected();


protected:
    void onMessage(String param, String message);
    void onWebsocketConnected();
    void onWebsocketDisconnected();
    void webSocketEvent(uint8_t num, WStype_t type, uint8_t * payload, size_t length);
    void setupRESTAPI();

    WebSocketsServer m_webSocketServer;
    WebServer m_webServer;

};

#endif  // _WEBSOCKET_SERVER_TASK_V2_H_