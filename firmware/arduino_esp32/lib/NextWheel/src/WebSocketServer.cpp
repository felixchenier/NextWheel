#include "WebSocketServer.h"
#include <SPIFFS.h>
#include <SD_MMC.h>
#include "SDCard.h"
#include <sys/time.h>
#include <config/GlobalConfig.h>
#include <state/SystemState.h>

WebSocketServer::WebSocketServer() : m_server(80), m_ws("/ws") {}

void WebSocketServer::begin(const GlobalConfig::ConfigData &configData)
{
    //Copy config data
    m_configData = configData;

    // Files are stored in SPIFFS
    // Must be uploaded to the ESP32 before running this code
    SPIFFS.begin();

    WiFi.begin(WIFI_DEFAULT_SSID, WIFI_DEFAULT_PASSWORD);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
    }
    Serial.print("Connected to WiFi IP: ");
    Serial.println(WiFi.localIP());

    // Setup the websocket
    setupWebSocket();

    // Setup static routes
    setupStaticRoutes();

    // Setup post request
    setupPostForm();

    // Setup config post request
    setupConfigPostForm();

    // Setup not found
    setupNotFound();

    m_server.begin();
}

void WebSocketServer::setupWebSocket()
{
    m_ws.onEvent(std::bind(
        &WebSocketServer::onWsEvent,
        this,
        std::placeholders::_1,
        std::placeholders::_2,
        std::placeholders::_3,
        std::placeholders::_4,
        std::placeholders::_5,
        std::placeholders::_6));
    m_server.addHandler(&m_ws);
}

void WebSocketServer::onMessage(WebSocketServerMessageEventHandler handler)
{
    m_messageHandler = handler;
}

void WebSocketServer::setupStaticRoutes()
{
    // Default static route
    m_server.serveStatic("/", SPIFFS, "/").setDefaultFile("index.htm");

    // Main route
    m_server.on(
        "/main",
        HTTP_GET,
        [this](AsyncWebServerRequest* request)
        {
            SDCard sd;
            sd.begin();

            File html_file = SPIFFS.open("/main.htm", "r");
            if (!html_file)
            {
                Serial.println("Failed to open main.htm");
                request->send(404);
                return;
            }
            uint8_t html_buffer[html_file.size()];
            html_file.readBytes((char*)html_buffer, html_file.size());
            request->send_P(
                200,
                PSTR("text/html"),
                html_buffer,
                html_file.size(),
                std::bind(&WebSocketServer::onGlobalProcessor, this, std::placeholders::_1));
            html_file.close();
        });

    // File listing route
    m_server.on(
        "/files",
        HTTP_GET,
        [this](AsyncWebServerRequest* request)
        {
            SDCard sd;
            sd.begin();

            File html_file = SPIFFS.open("/files.htm", "r");
            if (!html_file)
            {
                Serial.println("Failed to open files.htm");
                request->send(404);
                return;
            }
            uint8_t html_buffer[html_file.size()];
            html_file.readBytes((char*)html_buffer, html_file.size());
            request->send_P(
                200,
                PSTR("text/html"),
                html_buffer,
                html_file.size(),
                std::bind(&WebSocketServer::onFileProcessor, this, std::placeholders::_1));
            html_file.close();
        });

    // Configuration route
    m_server.on(
        "/config",
        HTTP_GET,
        [this](AsyncWebServerRequest* request)
        {
            File html_file = SPIFFS.open("/config.htm", "r");
            if (!html_file)
            {
                Serial.println("Failed to open config.htm");
                request->send(404);
                return;
            }
            uint8_t html_buffer[html_file.size()];
            html_file.readBytes((char*)html_buffer, html_file.size());
            request->send_P(
                200,
                PSTR("text/html"),
                html_buffer,
                html_file.size(),
                std::bind(&WebSocketServer::onConfigProcessor, this, std::placeholders::_1));
            html_file.close();
        });

    // Data route
    m_server.on(
        "/live",
        HTTP_GET,
        [this](AsyncWebServerRequest* request)
        {
            File html_file = SPIFFS.open("/live.htm", "r");
            if (!html_file)
            {
                Serial.println("Failed to open live.htm");
                request->send(404);
                return;
            }
            uint8_t html_buffer[html_file.size()];
            html_file.readBytes((char*)html_buffer, html_file.size());
            request->send_P(
                200,
                PSTR("text/html"),
                html_buffer,
                html_file.size(),
                std::bind(&WebSocketServer::onLiveProcessor, this, std::placeholders::_1));
            html_file.close();
        });

    // File deletion route
    m_server.on(
        "/delete_file",
        HTTP_GET,
        [this](AsyncWebServerRequest* request)
        {
            int params = request->params();
            for (auto i = 0; i < params; i++)
            {
                AsyncWebParameter* p = request->getParam(i);
                if (p->name() == "file")
                {
                    String file = "/" + p->value();
                    if (SD_MMC.exists(file))
                    {
                        SD_MMC.remove(file);
                    }
                }
            }
            request->redirect("/files");
        });

    // Mounting SDCARD to /download to facilitate file download
    m_server.serveStatic("/download", SD_MMC, "/");
}

void WebSocketServer::setupConfigPostForm()
{

    m_server.on(
        "/config_set_time",
        HTTP_POST,
        [this](AsyncWebServerRequest* request)
        {
            Serial.println("setupConfigPostForm: /config_set_time");

            int params = request->params();
            for (auto i = 0; i < params; i++)
            {
                AsyncWebParameter* p = request->getParam(i);

                if (p->isPost())
                {
                    if (p->name() == "time")
                    {
                        String time = p->value();
                        sendMessageEvent("set_time", time);
                    }
                }
            }

            request->send(200, "text/plain", "OK");
        });


    m_server.on(
        "/config_update",
        HTTP_POST,
        [this](AsyncWebServerRequest* request)
        {
            Serial.println("setupConfigPostForm: /config_update");

            int params = request->params();
            for (auto i = 0; i < params; i++)
            {
                AsyncWebParameter* p = request->getParam(i);

                if (p->isPost())
                {
                    Serial.printf("_POST[%s]: %s\n", p->name().c_str(), p->value().c_str());

                    if (p->name() == "accelerometer_precision") {
                        GlobalConfig::instance().set_accel_range(p->value().toInt());
                    }
                    else if (p->name() == "gyrometer_precision") {
                        GlobalConfig::instance().set_gyro_range(p->value().toInt());
                    }
                    else if (p->name() == "imu_sampling_rate") {
                        GlobalConfig::instance().set_imu_sample_rate(p->value().toInt());
                    }
                    else if (p->name() == "adc_sampling_rate") {
                        GlobalConfig::instance().set_adc_sample_rate(p->value().toInt());
                    }
                    else {
                        Serial.printf("Unknown parameter: %s\n", p->name().c_str());
                    }
                }
            }
            request->send(200, "text/plain", "OK");
        });
}

void WebSocketServer::setupPostForm()
{
    m_server.on(
        "/recording",
        HTTP_GET,
        [this](AsyncWebServerRequest* request)
        {
            String message;

            if (request->hasParam("recording"))
            {
                message = request->getParam("recording")->value();
                sendMessageEvent(String("recording"), String(message));
                // Serial.print("Recording received :");
                // Serial.println(message);
            }
            else
            {
                message = "No message";
            }

            request->redirect("/main");
        });
}

void WebSocketServer::setupNotFound()
{
    m_server.onNotFound(
        [](AsyncWebServerRequest* request)
        {
            Serial.printf("NOT_FOUND: ");
            if (request->method() == HTTP_GET)
                Serial.printf("GET");
            else if (request->method() == HTTP_POST)
                Serial.printf("POST");
            else if (request->method() == HTTP_DELETE)
                Serial.printf("DELETE");
            else if (request->method() == HTTP_PUT)
                Serial.printf("PUT");
            else if (request->method() == HTTP_PATCH)
                Serial.printf("PATCH");
            else if (request->method() == HTTP_HEAD)
                Serial.printf("HEAD");
            else if (request->method() == HTTP_OPTIONS)
                Serial.printf("OPTIONS");
            else
                Serial.printf("UNKNOWN");

            Serial.printf(" http://%s%s\n", request->host().c_str(), request->url().c_str());

            if (request->contentLength())
            {
                Serial.printf("_CONTENT_TYPE: %s\n", request->contentType().c_str());
                Serial.printf("_CONTENT_LENGTH: %u\n", request->contentLength());
            }

            int headers = request->headers();
            int i;
            for (i = 0; i < headers; i++)
            {
                AsyncWebHeader* h = request->getHeader(i);
                Serial.printf("_HEADER[%s]: %s\n", h->name().c_str(), h->value().c_str());
            }

            int params = request->params();
            for (i = 0; i < params; i++)
            {
                AsyncWebParameter* p = request->getParam(i);
                if (p->isFile())
                {
                    Serial.printf("_FILE[%s]: %s, size: %u\n", p->name().c_str(), p->value().c_str(), p->size());
                }
                else if (p->isPost())
                {
                    Serial.printf("_POST[%s]: %s\n", p->name().c_str(), p->value().c_str());
                }
                else
                {
                    Serial.printf("_GET[%s]: %s\n", p->name().c_str(), p->value().c_str());
                }
            }


            request->send(404);
        });
}

void WebSocketServer::sendToAll(DataFrame& frame)
{
    // Must write binary data to websocket
    uint8_t buffer[frame.getTotalSize()];
    frame.serialize(buffer, frame.getTotalSize());
    m_ws.binaryAll(buffer, frame.getTotalSize());
}

void WebSocketServer::sendToAll(const uint8_t* data, size_t size)
{
    if (size > 0 && data != nullptr && m_ws.availableForWriteAll())
    {
        if (m_ws.count() > 0)
        {
            m_ws.binaryAll((const char*)data, size);
        }
    }
    else
    {
        Serial.println("WebSocketServer::sendToAll: Buffer full, not available for write");
    }
}

void WebSocketServer::sendMessageEvent(String param, String message)
{
    if (m_messageHandler)
    {
        m_messageHandler(param, message);
    }
}

void WebSocketServer::onWsEvent(
    AsyncWebSocket* server,
    AsyncWebSocketClient* client,
    AwsEventType type,
    void* arg,
    uint8_t* data,
    size_t len)
{
    if (type == WS_EVT_CONNECT)
    {
        Serial.println("Client connected");
        SystemState::instance().getState().streaming = true;
        //Send config
        ConfigDataFrame frame(m_configData);
        sendToAll(frame);
    }
    else if (type == WS_EVT_DISCONNECT)
    {
        Serial.println("Client disconnected");
        SystemState::instance().getState().streaming = false;
    }
    else if (type == WS_EVT_DATA)
    {
        Serial.printf("Client message: %s\n", (char*)arg);
    }
}

String WebSocketServer::onGlobalProcessor(const String &var)
{
    if (var == F("SYSTEMTIME"))
    {
        struct timeval current_time;
        gettimeofday(&current_time, NULL);
        struct tm* time_info = localtime(&current_time.tv_sec);
        return String(asctime(time_info));
    }
    else if (var == F("SYSTEM_STATE_RECORDING"))
    {
        return String(SystemState::instance().getState().recording);
    }
    else if (var == F("SYSTEM_STATE_RECORDING_FILE"))
    {
        return String(SystemState::instance().getState().filename);
    }
    else if (var == F("SYSTEM_STATE_STREAMING"))
    {
        return String(SystemState::instance().getState().streaming);
    }
    else if (var == F("IMU_ACC_PRECISION"))
    {
        return String(GlobalConfig::instance().get_accel_range());
    }
    else if (var == F("IMU_GYR_PRECISION"))
    {
        return String(GlobalConfig::instance().get_gyro_range());
    }
    else if (var == F("IMU_SAMPLING_RATE"))
    {
        return String(GlobalConfig::instance().get_imu_sample_rate());
    }
    else if (var == F("ADC_SAMPLING_RATE")) {
        return String(GlobalConfig::instance().get_adc_sample_rate());
    }

    return String();
}

String WebSocketServer::onFileProcessor(const String& var)
{
    if (var == F("URLLINK"))
    {
        String str;
        File root = SD_MMC.open("/");
        root.rewindDirectory();
        File file = root.openNextFile();

        while (file)
        {
            std::string filename(file.name());
            if (filename.find(".dat") < filename.size())
            {
                // Begin row
                str += "<tr>";

                // Filename
                str += "<td>";
                str += "<a href=\"/download/";
                str += file.name();
                str += "\">";
                str += file.name();
                str += "</a>";
                str += "</td>";
                // Size
                str += "<td>";
                str += file.size();
                str += "</td>";
                // Delete
                str += "<td>";
                str += "<a href=\"/delete_file?file=";
                str += file.name();
                str += "\">";
                str += "DELETE";
                str += "</a>";
                str += "</td>";

                // End row
                str += "</tr>\n";
            }

            file = root.openNextFile();
        }

        root.close();
        root.rewindDirectory();
        return str;
    }

    return onGlobalProcessor(var);
}

String WebSocketServer::onConfigProcessor(const String& var)
{
    return onGlobalProcessor(var);
}

String WebSocketServer::onLiveProcessor(const String& var)
{
    return onGlobalProcessor(var);
}

int WebSocketServer::webSocketClientCount()
{
    return m_ws.count();
}