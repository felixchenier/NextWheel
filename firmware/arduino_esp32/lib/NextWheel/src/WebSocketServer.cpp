#include "WebSocketServer.h"
#include <SPIFFS.h>

WebSocketServer::WebSocketServer() :
    m_server(80),
    m_ws("/ws"){


}

void WebSocketServer::begin() {

    //Files are stored in SPIFFS
    //Must be uploaded to the ESP32 before running this code
    SPIFFS.begin();

    WiFi.begin(WIFI_DEFAULT_SSID, WIFI_DEFAULT_PASSWORD);
    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
    }
    Serial.print("Connected to WiFi IP: ");
    Serial.println(WiFi.localIP());

    //Setup the websocket
    setupWebSocket();

    //Setup static routes
    setupStaticRoutes();

    //Setup post request
    setupPostForm();

    //Setup not found
    setupNotFound();

    m_server.begin();
}

void WebSocketServer::setupWebSocket()
{
    m_ws.onEvent(std::bind(&WebSocketServer::onWsEvent, this, std::placeholders::_1, std::placeholders::_2, std::placeholders::_3, std::placeholders::_4, std::placeholders::_5, std::placeholders::_6));
    m_server.addHandler(&m_ws);

}

void WebSocketServer::onMessage(WebSocketServerMessageEventHandler handler) {
    m_messageHandler = handler;
}

void WebSocketServer::setupStaticRoutes()
{
    m_server.serveStatic("/", SPIFFS, "/").setDefaultFile("index.htm");
}

void WebSocketServer::setupPostForm()
{
    m_server.on("/recording", HTTP_GET, [this](AsyncWebServerRequest *request) {
        String message;

        if (request->hasParam("recording")) {
            message = request->getParam("recording")->value();
            sendMessageEvent(String("recording"), String(message));
            // Serial.print("Recording received :");
            // Serial.println(message);
        }
        else {
            message = "No message";
        }

        request->send(200, "text/plain", "Received " + message);
    });
}

void WebSocketServer::setupNotFound() {
    m_server.onNotFound([](AsyncWebServerRequest *request){
        Serial.printf("NOT_FOUND: ");
        if(request->method() == HTTP_GET)
            Serial.printf("GET");
        else if(request->method() == HTTP_POST)
            Serial.printf("POST");
        else if(request->method() == HTTP_DELETE)
            Serial.printf("DELETE");
        else if(request->method() == HTTP_PUT)
            Serial.printf("PUT");
        else if(request->method() == HTTP_PATCH)
            Serial.printf("PATCH");
        else if(request->method() == HTTP_HEAD)
            Serial.printf("HEAD");
        else if(request->method() == HTTP_OPTIONS)
            Serial.printf("OPTIONS");
        else
            Serial.printf("UNKNOWN");

        Serial.printf(" http://%s%s\n", request->host().c_str(), request->url().c_str());

        if(request->contentLength()) {
            Serial.printf("_CONTENT_TYPE: %s\n", request->contentType().c_str());
            Serial.printf("_CONTENT_LENGTH: %u\n", request->contentLength());
        }

        int headers = request->headers();
        int i;
        for(i=0;i<headers;i++){
            AsyncWebHeader* h = request->getHeader(i);
            Serial.printf("_HEADER[%s]: %s\n", h->name().c_str(), h->value().c_str());
        }

        int params = request->params();
        for(i=0;i<params;i++){
            AsyncWebParameter* p = request->getParam(i);
            if(p->isFile()){
                Serial.printf("_FILE[%s]: %s, size: %u\n", p->name().c_str(), p->value().c_str(), p->size());
            } else if(p->isPost()){
                Serial.printf("_POST[%s]: %s\n", p->name().c_str(), p->value().c_str());
            } else {
                Serial.printf("_GET[%s]: %s\n", p->name().c_str(), p->value().c_str());
            }
        }


        request->send(404);
    });
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

void WebSocketServer::sendMessageEvent(String param, String message) {
    if (m_messageHandler) {
        m_messageHandler(param, message);
    }
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