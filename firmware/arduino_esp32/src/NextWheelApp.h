#ifndef _NEXT_WHEEL_APP_H_
#define _NEXT_WHEEL_APP_H_

#include "NextWheel.h"

#include <RTC.h>
#include <LEDS.h>
#include <Buttons.h>

#include "tasks/SensorTask.h"
#include "tasks/WorkerTask.h"
#include "tasks/ADCSensorTask.h"
#include "tasks/IMUSensorTask.h"
#include "tasks/PowerSensorTask.h"
#include "tasks/WebSocketServerTask.h"
#include "tasks/SDCardWorkerTask.h"
#include "tasks/DACActuatorTask.h"
#include "tasks/QuadEncoderSensorTask.h"

#include "config/GlobalConfig.h"

class NextWheelApp
{
public:
    static NextWheelApp* instance();

    void begin();

    void start();

    bool isRecording();

    bool isStreaming();

    LEDS& getLEDS();

    RTC& getRTC();

    bool startRecording(bool from_isr = false);

    bool stopRecording(bool from_isr = false);

    void sendConfigUpdateEvent(bool from_isr = false);

    bool setTime(String time);

    void registerSensorTasksToSDCardWorker();
    void unregisterSensorTasksFromSDCardWorker();
    void registerSensorTasksToWebSocketServer();
    void unregisterSensorTasksFromWebSocketServer();

    bool button1Pressed();
    bool button2Pressed();

private:
    NextWheelApp();

    // Singleton instance
    static NextWheelApp* m_instance;


    // Drivers
    RTC m_rtc;
    LEDS m_leds;
    Buttons m_buttons;

    // Actuators
    DACActuatorTask m_dacTask;


    // Sensors
    ADCSensorTask m_adcTask;
    IMUSensorTask m_imuTask;
    PowerSensorTask m_powerTask;
    QuadEncoderSensorTask m_quadEncoderTask;

    // Workers
    SDCardWorkerTask m_sdCardWorkerTask;
    //WebSocketServerTask m_webSocketServerTask;
    WebSocketServerTask m_webSocketServerTask;

    SemaphoreHandle_t m_queueMutex;
};
#endif
