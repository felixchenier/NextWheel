#ifndef _WORKER_TASK_H_
#define _WORKER_TASK_H_


#include "data/DataFrame.h"
#include "Task.h"
#include <freertos/queue.h>


class WorkerTask : public Task {
    public:
        WorkerTask(const char* name, uint32_t stackSize=TASK_STACK_SIZE_DEFAULT, uint8_t priority=TASK_PRIORITY_DEFAULT)
            : Task(name, stackSize, priority), m_dataQueue(nullptr) {

            m_dataQueue = xQueueCreate(200, sizeof(DataFramePtr));

        }

        QueueHandle_t* getQueue() {
            return &m_dataQueue;
        }


        DataFramePtr dequeue(unsigned long timeout = 10) {
            DataFramePtr dataPtr;
            if (xQueueReceive(m_dataQueue, &dataPtr, timeout) != pdTRUE) {
                return nullptr;
            }
            return dataPtr;
        }

        virtual void run(void *) = 0;

    protected:

    QueueHandle_t m_dataQueue;

};
#endif  // _WORKER_TASK_H_