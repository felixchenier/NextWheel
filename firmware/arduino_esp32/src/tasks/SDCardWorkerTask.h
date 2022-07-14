#ifndef _SDCARD_WORKER_TASK_H_
#define _SDCARD_WORKER_TASK_H_

#include "tasks/WorkerTask.h"
#include "SDCard.h"


class SDCardWorkerTask : public WorkerTask
{
    static const size_t SDCARD_WORKER_TASK_STACK_SIZE = 8000;

public:
    enum SDCardWorkerTaskCommand
    {
        SDCARD_WORKER_TASK_COMMAND_NONE = 0,
        SDCARD_WORKER_TASK_COMMAND_START_RECORDING = 1,
        SDCARD_WORKER_TASK_COMMAND_STOP_RECORDING = 2
    };


    SDCardWorkerTask()
        : WorkerTask("SDCardWorkerTask", SDCARD_WORKER_TASK_STACK_SIZE),
          m_file(nullptr),
          m_bytesWritten(0)
    {
        m_commandQueue = xQueueCreate(100, sizeof(SDCardWorkerTaskCommand));
    }

    bool sendCommandEvent(SDCardWorkerTaskCommand command, bool from_isr = false)
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


    String currentFileName() { return m_filename; }

    bool isRecording()
    {
        if (m_file)
        {
            return true;
        }

        return false;
    }

    virtual void run(void* app) override;

private:
    SDCard m_sdCard;
    File m_file;
    String m_filename;
    size_t m_bytesWritten;
    QueueHandle_t m_commandQueue;

    SDCardWorkerTaskCommand dequeueCommand(unsigned long timeout = 10)
    {
        SDCardWorkerTaskCommand command = SDCARD_WORKER_TASK_COMMAND_NONE;
        if (xQueueReceive(m_commandQueue, &command, timeout) != pdTRUE)
        {
            return SDCARD_WORKER_TASK_COMMAND_NONE;
        }
        return command;
    }

    String generateFileName()
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

    void resetLog()
    {
        if (m_file)
        {
            m_file.close();
        }
        m_file = File(nullptr);
        m_filename = String();
        m_bytesWritten = 0;
    }
};

#endif  // _SDCARD_WORKER_TASK_H_
