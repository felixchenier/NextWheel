#ifndef _WEBSOCKET_SERVER_H_
#define _WEBSOCKET_SERVER_H_

#include "config/WiFiConfig.h"
#include <NextWheel.h>
#include <ESPAsyncWebServer.h>
#include <data/DataFrame.h>
#include <data/ConfigDataFrame.h>

class WebSocketServer
{
public:
    typedef std::function<void(String param, String message)> WebSocketServerMessageEventHandler;
    typedef std::function<void()> WebSocketServerWebsocketConnectedHandler;
    typedef std::function<void()> WebSocketServerWebsocketDisconnectedHandler;


    WebSocketServer();
    void begin(const GlobalConfig::ConfigData &configData);
    void sendToAll(DataFrame& frame);
    void sendToAll(const uint8_t* data, size_t size);
    int webSocketClientCount();
    void onMessage(WebSocketServerMessageEventHandler handler);
    void registerWebsocketConnectedHandler(WebSocketServerWebsocketConnectedHandler handler);
    void registerWebsocketDisconnectedHandler(WebSocketServerWebsocketDisconnectedHandler handler);

private:
    AsyncWebServer m_server;
    AsyncWebSocket m_ws;
    WebSocketServerMessageEventHandler m_messageHandler;
    String m_currentRecordingFileName;

    void setupWebSocket();
    void setupStaticRoutes();
    void setupNotFound();
    void setupPostForm();
    void setupConfigPostForm();
    void setupRESTAPI();

    void sendMessageEvent(String param, String message);
    void onWsEvent(
        AsyncWebSocket* server,
        AsyncWebSocketClient* client,
        AwsEventType type,
        void* arg,
        uint8_t* data,
        size_t len);

    String onGlobalProcessor(const String &var);
    String onFileProcessor(const String& var);
    String onConfigProcessor(const String& var);
    String onLiveProcessor(const String& var);
    GlobalConfig::ConfigData m_configData;

    WebSocketServerWebsocketConnectedHandler m_websocketConnectedHandler;
    WebSocketServerWebsocketConnectedHandler m_websocketDisconnectedHandler;
};

#endif  // _WEBSOCKET_SERVER_H_
