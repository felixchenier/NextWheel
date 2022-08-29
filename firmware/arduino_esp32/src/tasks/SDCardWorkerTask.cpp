#include "SDCardWorkerTask.h"
#include "NextWheelApp.h"
#include "data/ConfigDataFrame.h"
#include "config/GlobalConfig.h"
#include "state/SystemState.h"


SDCardWorkerTask::SDCardWorkerTask()
    : WorkerTask("SDCardWorkerTask", SDCARD_WORKER_TASK_STACK_SIZE),
      m_file(nullptr),
      m_bytesWritten(0)
{
    m_commandQueue = xQueueCreate(100, sizeof(SDCardWorkerTaskCommand));
}

bool SDCardWorkerTask::sendCommandEvent(SDCardWorkerTaskCommand command, bool from_isr)
{
    if (from_isr)
    {
        return xQueueSendFromISR(m_commandQueue, &command, nullptr) == pdTRUE;
    }
    else
    {
        return xQueueSend(m_commandQueue, &command, 0) == pdTRUE;
    }
}


String SDCardWorkerTask::currentFileName()
{
    return m_filename;
}

bool SDCardWorkerTask::isRecording()
{
    if (m_file)
    {
        return true;
    }

    return false;
}

void SDCardWorkerTask::run(void* app)
{
    Serial.printf("SDCardWorkerTask::run Priority: %li Core: %li \n", uxTaskPriorityGet(NULL), xPortGetCoreID());

    TickType_t lastGeneration = xTaskGetTickCount();

    while (1)
    {
        // 10 ms task
        vTaskDelayUntil(&lastGeneration, 10 / portTICK_RATE_MS);

        // Dequeue all data values (one shot), no timeout
        while (DataFramePtr dataPtr = dequeue(0))
        {
            // Writing to log file if it is open
            if (m_file)
            {
                m_bytesWritten += m_sdCard.writeToLogFile(m_file, *dataPtr);
            }

            // Mandatory to delete, otherwise the memory will be leaked
            delete dataPtr;
        }

        // Make sure write is complete
        if (m_file)
        {
            m_file.flush();
        }

        // Dequeue commands
        while (SDCardWorkerTaskCommand command = dequeueCommand(0))
        {
            switch (command)
            {
                case SDCARD_WORKER_TASK_COMMAND_NONE:
                    Serial.println("SDCardWorkerTask::run: SDCARD_WORKER_TASK_COMMAND_NONE");
                    break;
                case SDCARD_WORKER_TASK_COMMAND_START_RECORDING:

                    Serial.println("SDCardWorkerTask::run: SDCARD_WORKER_TASK_COMMAND_START_RECORDING");
                    m_sdCard.begin();

                    // Make sure we close the file if we were already recording
                    resetLog();

                    m_filename = generateFileName();
                    m_file = m_sdCard.openNewLogFile(m_filename.c_str());
                    if (!m_file)
                    {
                        Serial.print("SDCardWorkerTask::run: Failed to open log file : ");
                        Serial.println(m_filename);
                        resetLog();
                    }
                    else
                    {
                        Serial.print("SDCardWorkerTask::run: File opened: ");
                        Serial.println(m_file.name());

                        SystemState::instance().getState().recording = true;
                        SystemState::instance().getState().filename = m_file.name();

                        // Write config (first data object in the file)
                        ConfigDataFrame configDataFrame(GlobalConfig::instance().get());
                        m_sdCard.writeToLogFile(m_file, configDataFrame);
                    }
                    break;
                case SDCARD_WORKER_TASK_COMMAND_STOP_RECORDING:
                    Serial.println("SDCardWorkerTask::run: SDCARD_WORKER_TASK_COMMAND_STOP_RECORDING");
                    if (m_file)
                    {
                        SystemState::instance().getState().recording = false;
                        SystemState::instance().getState().filename  = String();

                        Serial.print("SDCardWorkerTask::run: File closed: ");
                        Serial.println(m_file.name());
                        Serial.print("SDCardWorkerTask::run: File size: ");
                        Serial.println(m_bytesWritten);
                    }
                    resetLog();
                    break;
                default:
                    Serial.println("SDCardWorkerTask::run: Unknown command");
                    break;
            }
        }  // end while (SDCardWorkerTaskCommand command = dequeueCommand(0))
    }
}

SDCardWorkerTask::SDCardWorkerTaskCommand SDCardWorkerTask::dequeueCommand(unsigned long timeout)
{
    SDCardWorkerTaskCommand command = SDCARD_WORKER_TASK_COMMAND_NONE;
    if (xQueueReceive(m_commandQueue, &command, timeout) != pdTRUE)
    {
        return SDCARD_WORKER_TASK_COMMAND_NONE;
    }
    return command;
}

String SDCardWorkerTask::generateFileName()
{
    time_t now;
    struct tm* timeInfo;
    time(&now);
    timeInfo = localtime(&now);
    char fileName[64];
    sprintf(
        fileName,
        "/log_%04d-%02d-%02d_%02d-%02d-%02d.dat",
        timeInfo->tm_year + 1900,
        timeInfo->tm_mon + 1,
        timeInfo->tm_mday,
        timeInfo->tm_hour,
        timeInfo->tm_min,
        timeInfo->tm_sec);
    return String(fileName);
}

void SDCardWorkerTask::resetLog()
{
    if (m_file)
    {
        m_file.close();
    }
    m_file = File(nullptr);
    m_filename = String();
    m_bytesWritten = 0;
}