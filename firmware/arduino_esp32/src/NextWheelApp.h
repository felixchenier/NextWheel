#ifndef _NEXT_WHEEL_APP_H_
#define _NEXT_WHEEL_APP_H_

#include "NextWheel.h"
#include "tasks/SensorTask.h"
#include "tasks/WorkerTask.h"
#include "tasks/ADCSensorTask.h"
#include "tasks/IMUSensorTask.h"
#include "tasks/PowerSensorTask.h"
#include "tasks/PrintWorkerTask.h"
#include "tasks/WebSocketServerTask.h"
#include "tasks/SDCardWorkerTask.h"


class NextWheelApp {
    public:

    NextWheelApp() : m_webSocketServerTask(&m_sdCardWorkerTask)
    {

    }

    void begin() {

        // Sensors must be enabled
        // Must be first
        m_sdCardWorkerTask.setCore(0);
        m_sdCardWorkerTask.setPriority(TASK_PRIORITY_HIGH);

        //m_printWorkerTask.setCore(0);
        //m_printWorkerTask.setPriority(TASK_PRIORITY_IDLE);

        m_webSocketServerTask.setCore(1);
        m_webSocketServerTask.setPriority(TASK_PRIORITY_MEDIUM);

        m_adcTask.setCore(1);
        m_adcTask.setPriority(TASK_PRIORITY_HIGHEST);

        m_imuTask.setCore(1);
        m_imuTask.setPriority(TASK_PRIORITY_HIGHEST);

        m_powerTask.setCore(1);
        m_powerTask.setPriority(TASK_PRIORITY_HIGH);


        //Register to queues
        registerSensorTaskToQueues(m_adcTask);
        registerSensorTaskToQueues(m_imuTask);
        registerSensorTaskToQueues(m_powerTask);

    }

    void start() {
        m_sdCardWorkerTask.start(this);
        //m_printWorkerTask.start(nullptr);
        m_webSocketServerTask.start(this);
        m_adcTask.start(this);
        m_imuTask.start(this);
        m_powerTask.start(this);
    }

    bool isRecording() {
        return m_sdCardWorkerTask.isRecording();
    }

    //Sensors
    ADCSensorTask m_adcTask;
    IMUSensorTask m_imuTask;
    PowerSensorTask m_powerTask;

    //Workers
    //PrintWorkerTask m_printWorkerTask;
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
