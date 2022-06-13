#ifndef _WEBSOCKET_SERVER_H_
#define _WEBSOCKET_SERVER_H_

#include <NextWheel.h>
#include <ESPAsyncWebServer.h>
#include <Task.h>
#include <freertos/queue.h>

class WebSocketServer : public Task {
    public:
        WebSocketServer();
        void begin();
        void update();
    private:
        virtual void run(void* data);
        AsyncWebServer m_server;
        AsyncWebSocket m_ws;
        void onWsEvent(AsyncWebSocket * server, AsyncWebSocketClient * client, AwsEventType type, void * arg, uint8_t *data, size_t len);
};

#endif // _WEBSOCKET_SERVER_H_
