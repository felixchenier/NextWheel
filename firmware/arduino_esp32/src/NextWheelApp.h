#ifndef _NEXT_WHEEL_APP_H_
#define _NEXT_WHEEL_APP_H_

#include "NextWheel.h"
#include "tasks/SensorTask.h"
#include "tasks/WorkerTask.h"
#include "tasks/ADCTask.h"
#include "tasks/PrintWorkerTask.h"
#include "tasks/WebSocketServerTask.h"
#include "tasks/SDCardWorkerTask.h"


class NextWheelApp {
    public:

    NextWheelApp() : m_webSocketServerTask(&m_sdCardWorkerTask)
    {

    }

    void begin() {

        // Must be first
        m_sdCardWorkerTask.setCore(0);
        m_sdCardWorkerTask.setPriority(TASK_PRIORITY_HIGH);

        m_printWorkerTask.setCore(0);
        m_printWorkerTask.setPriority(TASK_PRIORITY_IDLE);

        m_webSocketServerTask.setCore(1);
        m_webSocketServerTask.setPriority(TASK_PRIORITY_MEDIUM);

        m_adcTask.setCore(1);
        m_adcTask.setPriority(TASK_PRIORITY_HIGHEST);

        //Register to queues
        registerSensorTaskToQueues(m_adcTask);

    }

    void start() {
        m_sdCardWorkerTask.start(this);
        //m_printWorkerTask.start(nullptr);
        m_webSocketServerTask.start(this);
        m_adcTask.start(this);
    }


    ADCTask m_adcTask;
    PrintWorkerTask m_printWorkerTask;
    SDCardWorkerTask m_sdCardWorkerTask;
    WebSocketServerTask m_webSocketServerTask;

    private:

    void registerSensorTaskToQueues(SensorTask &task) {
        //task.registerDataQueue(m_printWorkerTask.getQueue());
        task.registerDataQueue(m_sdCardWorkerTask.getQueue());
        task.registerDataQueue(m_webSocketServerTask.getQueue());
    }

};
#endif
