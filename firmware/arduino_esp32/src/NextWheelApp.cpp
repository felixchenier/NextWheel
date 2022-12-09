#include "NextWheelApp.h"

NextWheelApp* NextWheelApp::m_instance = nullptr;

// Singleton pattern
NextWheelApp* NextWheelApp::instance()
{
    if (m_instance == nullptr)
    {
        m_instance = new NextWheelApp();
    }
    return m_instance;
}

void NextWheelApp::begin()
{
    // Sensors must be enabled
    // Must be first
    m_sdCardWorkerTask.setCore(1);
    m_sdCardWorkerTask.setPriority(TASK_PRIORITY_HIGH);

    // m_printWorkerTask.setCore(0);
    // m_printWorkerTask.setPriority(TASK_PRIORITY_IDLE);

    m_webSocketServerTask.setCore(0);
    m_webSocketServerTask.setPriority(TASK_PRIORITY_MEDIUM);

    m_adcTask.setCore(1);
    m_adcTask.setPriority(TASK_PRIORITY_HIGHEST);

    m_imuTask.setCore(1);
    m_imuTask.setPriority(TASK_PRIORITY_HIGH);

    m_quadEncoderTask.setCore(1);
    m_quadEncoderTask.setPriority(TASK_PRIORITY_MEDIUM);

    m_powerTask.setCore(1);
    m_powerTask.setPriority(TASK_PRIORITY_MEDIUM);

    m_dacTask.setCore(1);
    m_dacTask.setPriority(TASK_PRIORITY_LOW);
}

void NextWheelApp::start()
{
    Serial.println("Starting worker tasks");
    m_sdCardWorkerTask.start(this);
    // m_printWorkerTask.start(nullptr);

#ifndef NEXTWHEEL_DISABLE_WIFI
    m_webSocketServerTask.start(this);
#else
    Serial.println("WiFi + WebSocketServerTask disabled");
#endif


    Serial.println("Starting sensor tasks");
    m_adcTask.start(this);
    m_imuTask.start(this);
    m_powerTask.start(this);
    m_dacTask.start(this);
    m_quadEncoderTask.start(this);
}

bool NextWheelApp::isRecording()
{
    return m_sdCardWorkerTask.isRecording();
}

LEDS& NextWheelApp::getLEDS()
{
    return m_leds;
}

RTC& NextWheelApp::getRTC()
{
    return m_rtc;
}

bool NextWheelApp::startRecording(bool from_isr)
{
    return m_sdCardWorkerTask.sendCommandEvent(SDCardWorkerTask::SDCARD_WORKER_TASK_COMMAND_START_RECORDING, from_isr);
}

bool NextWheelApp::stopRecording(bool from_isr)
{
    return m_sdCardWorkerTask.sendCommandEvent(SDCardWorkerTask::SDCARD_WORKER_TASK_COMMAND_STOP_RECORDING, from_isr);
}

NextWheelApp::NextWheelApp()
{
    Serial.print("NextWheel version: ");
    Serial.println(NEXT_WHEEL_VERSION);

    m_queueMutex = xSemaphoreCreateMutex();

    // WARNING -  Make sure Arduino is initialized before creating an instance of NextWheelApp

    // Load config
    GlobalConfig::instance().begin();

    // Initialize leds
    m_leds.begin();

    // First thing we set the system to current time
    m_rtc.begin();

    // Initialize buttons
    // TODO disable buttons for now, interrupts are randomly generated because of noisy power suply.
    m_buttons.begin();
}

void NextWheelApp::registerSensorTasksToSDCardWorker()
{
    Serial.println("Registering sensor tasks to SDCardWorkerTask");
    xSemaphoreTake(m_queueMutex, portMAX_DELAY);
    m_adcTask.registerDataQueue(m_sdCardWorkerTask.getQueue());
    m_imuTask.registerDataQueue(m_sdCardWorkerTask.getQueue());
    m_powerTask.registerDataQueue(m_sdCardWorkerTask.getQueue());
    m_quadEncoderTask.registerDataQueue(m_sdCardWorkerTask.getQueue());
    xSemaphoreGive(m_queueMutex);
}

void NextWheelApp::unregisterSensorTasksFromSDCardWorker()
{
    Serial.println("Unregistering sensor tasks from SDCardWorkerTask");
    xSemaphoreTake(m_queueMutex, portMAX_DELAY);
    m_adcTask.unregisterDataQueue(m_sdCardWorkerTask.getQueue());
    m_imuTask.unregisterDataQueue(m_sdCardWorkerTask.getQueue());
    m_powerTask.unregisterDataQueue(m_sdCardWorkerTask.getQueue());
    m_quadEncoderTask.unregisterDataQueue(m_sdCardWorkerTask.getQueue());
    xSemaphoreGive(m_queueMutex);
}

void NextWheelApp::registerSensorTasksToWebSocketServer()
{
    Serial.println("Registering sensor tasks to WebSocketServerTask");
    xSemaphoreTake(m_queueMutex, portMAX_DELAY);
    m_adcTask.registerDataQueue(m_webSocketServerTask.getQueue());
    m_imuTask.registerDataQueue(m_webSocketServerTask.getQueue());
    m_powerTask.registerDataQueue(m_webSocketServerTask.getQueue());
    m_quadEncoderTask.registerDataQueue(m_webSocketServerTask.getQueue());
    xSemaphoreGive(m_queueMutex);
}

void NextWheelApp::unregisterSensorTasksFromWebSocketServer()
{
    Serial.println("Unregistering sensor tasks from WebSocketServerTask");
    xSemaphoreTake(m_queueMutex, portMAX_DELAY);
    m_adcTask.unregisterDataQueue(m_webSocketServerTask.getQueue());
    m_imuTask.unregisterDataQueue(m_webSocketServerTask.getQueue());
    m_powerTask.unregisterDataQueue(m_webSocketServerTask.getQueue());
    m_quadEncoderTask.unregisterDataQueue(m_webSocketServerTask.getQueue());
    xSemaphoreGive(m_queueMutex);
}


bool NextWheelApp::setTime(String time)
{
    return m_rtc.setTime(time);
}

namespace NextWheelInterrupts
{
    // interrupts
    // WARNING No Serial.print allowed in interrupts

    void IRAM_ATTR button1_interrupt()
    {
        // Get the state of the button
        // Start recording from ISR
        bool state = digitalRead(PIN_BUTTON_1);
        if (state)
        {
            NextWheelApp::instance()->startRecording(true);
        }
    }

    void IRAM_ATTR button2_interrupt()
    {
        // Get the state of the button
        // Stop recording from ISR
        bool state = digitalRead(PIN_BUTTON_2);
        if (state)
        {
            NextWheelApp::instance()->stopRecording(true);
        }
    }
}
