#ifndef _WEBSOCKET_SERVER_H_
#define _WEBSOCKET_SERVER_H_

#include <NextWheel.h>
#include <ESPAsyncWebServer.h>
#include <DataFrame.h>

class WebSocketServer  {
    public:

        typedef std::function<void(String param, String message)> WebSocketServerMessageEventHandler;

        WebSocketServer();
        void begin();

        void sendToAll(DataFrame &frame);
        void sendToAll(const uint8_t *data, size_t size);
        void onMessage(WebSocketServerMessageEventHandler handler);

    private:
        AsyncWebServer m_server;
        AsyncWebSocket m_ws;
        WebSocketServerMessageEventHandler m_messageHandler;

        void setupWebSocket();
        void setupStaticRoutes();
        void setupNotFound();
        void setupPostForm();
        void sendMessageEvent(String param, String message);
        void onWsEvent(AsyncWebSocket * server, AsyncWebSocketClient * client, AwsEventType type, void * arg, uint8_t *data, size_t len);


};

#endif // _WEBSOCKET_SERVER_H_