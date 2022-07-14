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
#include "tasks/PrintWorkerTask.h"
#include "tasks/WebSocketServerTask.h"
#include "tasks/SDCardWorkerTask.h"

#include "config/GlobalConfig.h"

class NextWheelApp
{
public:


    static NextWheelApp* instance();

    void begin()
    {
        // Sensors must be enabled
        // Must be first
        m_sdCardWorkerTask.setCore(0);
        m_sdCardWorkerTask.setPriority(TASK_PRIORITY_HIGH);

        // m_printWorkerTask.setCore(0);
        // m_printWorkerTask.setPriority(TASK_PRIORITY_IDLE);

        m_webSocketServerTask.setCore(1);
        m_webSocketServerTask.setPriority(TASK_PRIORITY_MEDIUM);

        m_adcTask.setCore(1);
        m_adcTask.setPriority(TASK_PRIORITY_HIGHEST);

        m_imuTask.setCore(1);
        m_imuTask.setPriority(TASK_PRIORITY_HIGHEST);

        m_powerTask.setCore(1);
        m_powerTask.setPriority(TASK_PRIORITY_HIGH);


        // Register to queues
        registerSensorTaskToQueues(m_adcTask);
        registerSensorTaskToQueues(m_imuTask);
        registerSensorTaskToQueues(m_powerTask);
    }

    void start()
    {
        m_sdCardWorkerTask.start(this);
        // m_printWorkerTask.start(nullptr);
        m_webSocketServerTask.start(this);
        m_adcTask.start(this);
        m_imuTask.start(this);
        m_powerTask.start(this);
    }

    bool isRecording() { return m_sdCardWorkerTask.isRecording(); }

    LEDS& getLEDS() { return m_leds; }

    RTC& getRTC() { return m_rtc; }

    bool startRecording(bool from_isr = false) {
        return m_sdCardWorkerTask.sendCommandEvent(SDCardWorkerTask::SDCARD_WORKER_TASK_COMMAND_START_RECORDING, from_isr);
    }

    bool stopRecording(bool from_isr = false) {
        return m_sdCardWorkerTask.sendCommandEvent(SDCardWorkerTask::SDCARD_WORKER_TASK_COMMAND_STOP_RECORDING, from_isr);
    }

    GlobalConfig getConfig() const { return m_config; }


private:

    NextWheelApp() : m_webSocketServerTask(&m_sdCardWorkerTask)
    {
        Serial.print("NextWheel version: ");
        Serial.println(NEXT_WHEEL_VERSION);

        // WARNING -  Make sure Arduino is initialized before creating an instance of NextWheelApp

        //Load config
        m_config.begin();

        // Initialize leds
        m_leds.begin();

        // First thing we set the system to current time
        m_rtc.begin();

        // Initialize buttons
        // TODO disable buttons for now, interrupts are randomly generated because of noisy power suply.
        // m_buttons.begin();
    }

    void registerSensorTaskToQueues(SensorTask& task)
    {
        // task.registerDataQueue(m_printWorkerTask.getQueue());
        task.registerDataQueue(m_sdCardWorkerTask.getQueue());
        task.registerDataQueue(m_webSocketServerTask.getQueue());
    }

    // Singleton instance
    static NextWheelApp* m_instance;


    // Drivers
    RTC m_rtc;
    LEDS m_leds;
    Buttons m_buttons;

    // Sensors
    ADCSensorTask m_adcTask;
    IMUSensorTask m_imuTask;
    PowerSensorTask m_powerTask;

    // Workers
    // PrintWorkerTask m_printWorkerTask;
    SDCardWorkerTask m_sdCardWorkerTask;
    WebSocketServerTask m_webSocketServerTask;

    //Config
    GlobalConfig m_config;
};
#endif
