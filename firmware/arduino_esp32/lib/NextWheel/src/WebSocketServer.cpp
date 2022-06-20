#include "WebSocketServer.h"
#include <SPIFFS.h>
#include <SD_MMC.h>
#include "SDCard.h"
#include "download.h"


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


    m_server.on("/files", HTTP_GET, [this](AsyncWebServerRequest * request) {
        request->send_P(200, PSTR("text/html"), DOWNLOAD_HTML_TEMPLATE, std::bind(&WebSocketServer::onFileDownloadProcessor, this, std::placeholders::_1));
    });

    m_server.on("/download", HTTP_GET, [this](AsyncWebServerRequest * request) {

        SDCard sdCard;

        sdCard.begin();

        //Get the file name from the full url

        String originalUrl = request->urlDecode(request->url());
        String fileName = request->urlDecode(request->url());

        //Remove the leading /download from the file name
        fileName.replace("/download", "");

        Serial.printf("Downloading file: %s\n", fileName.c_str());

        //Get the file
        File file = SD_MMC.open(fileName, "r");

        //Send the file
        if (file) {
            //void AsyncWebServerRequest::send(File content, const String& path, const String& contentType, bool download, AwsTemplateProcessor callback)
            request->send(file, originalUrl, "application/octet-stream", false, nullptr);
            file.close();
        } else {
            request->send(404, "text/plain", "File not found");
        }

        sdCard.end();
    });
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
    if (size > 0 && data != nullptr && m_ws.availableForWriteAll()) {
        if (m_ws.count() > 0) {
            m_ws.binaryAll((const char*) data, size);
        }
    }
    else {
        Serial.println("WebSocketServer::sendToAll: No available websocket for writing");
    }
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


 String WebSocketServer::onFileDownloadProcessor(const String& var)
 {

    //index2.h
    SDCard sd;

    sd.begin();

    String str;

    File root = SD_MMC.open("/");

    root.rewindDirectory();
    File file = root.openNextFile();

    while (file) {
        std::string filename(file.name());
        if (filename.find(".dat") < filename.size() ) {
            str += "<a href=\"/download/";
            str += file.name();
            str += "\">";
            str += file.name();
            str += "</a>";
            str += "    ";
            str += file.size();
            str += "<br>\r\n";
        }

        file = root.openNextFile();
    }

    root.close();

    root.rewindDirectory();

    if (var == F("URLLINK"))
        return  str;

    if (var == F("LINK"))
        return "";

    if (var == F("FILENAME"))
        return  file.name();

    sd.end();

    return String();



 }