#ifndef _WEBSOCKET_SERVER_H_
#define _WEBSOCKET_SERVER_H_

#include <NextWheel.h>
#include <ESPAsyncWebServer.h>

class WebSocketServer {
    public:
        WebSocketServer();
        void begin();
        void update();
    private:
        AsyncWebServer m_server;
        AsyncWebSocket m_ws;
        void onWsEvent(AsyncWebSocket * server, AsyncWebSocketClient * client, AwsEventType type, void * arg, uint8_t *data, size_t len);
};

#endif // _WEBSOCKET_SERVER_H_
