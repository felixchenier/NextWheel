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

void NextWheelApp::start()
{
    m_sdCardWorkerTask.start(this);
    // m_printWorkerTask.start(nullptr);
    m_webSocketServerTask.start(this);
    m_adcTask.start(this);
    m_imuTask.start(this);
    m_powerTask.start(this);
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

    // WARNING -  Make sure Arduino is initialized before creating an instance of NextWheelApp

    // Load config
    GlobalConfig::instance().begin();

    // Initialize leds
    m_leds.begin();

    // First thing we set the system to current time
    m_rtc.begin();

    // Initialize buttons
    // TODO disable buttons for now, interrupts are randomly generated because of noisy power suply.
    // m_buttons.begin();
}

void NextWheelApp::registerSensorTaskToQueues(SensorTask& task)
{
    // task.registerDataQueue(m_printWorkerTask.getQueue());
    task.registerDataQueue(m_sdCardWorkerTask.getQueue());
    task.registerDataQueue(m_webSocketServerTask.getQueue());
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
