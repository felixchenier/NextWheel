#include "WebSocketServer.h"


WebSocketServer::WebSocketServer() :
    m_server(80),
    m_ws("/ws"){


}

void WebSocketServer::begin() {
    WiFi.begin(WIFI_DEFAULT_SSID, WIFI_DEFAULT_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }
    Serial.print("Connected to WiFi IP: ");
    Serial.println(WiFi.localIP());
    m_ws.onEvent(std::bind(&WebSocketServer::onWsEvent, this, std::placeholders::_1, std::placeholders::_2, std::placeholders::_3, std::placeholders::_4, std::placeholders::_5, std::placeholders::_6));
    m_server.addHandler(&m_ws);
    m_server.begin();
}

void WebSocketServer::sendToAll(DataFrame &frame)
{
    // Must write binary data to websocket
    uint8_t buffer[frame.getTotalSize()];
    frame.serialize(buffer, frame.getTotalSize());
    m_ws.binaryAll(buffer, frame.getTotalSize());
}

void WebSocketServer::sendToAll(const uint8_t *data, size_t size)
{
    m_ws.binaryAll((const char*) data, size);
}

void WebSocketServer::onWsEvent(AsyncWebSocket * server, AsyncWebSocketClient * client, AwsEventType type, void * arg, uint8_t *data, size_t len) {
    if(type == WS_EVT_CONNECT) {
        Serial.println("Client connected");
    } else if(type == WS_EVT_DISCONNECT) {
        Serial.println("Client disconnected");
    } else if(type == WS_EVT_DATA) {
        Serial.printf("Client message: %s\n", (char*)arg);
    }
}
