#ifndef _WORKER_TASK_H_
#define _WORKER_TASK_H_

#include <freertos/queue.h>
#include "DataFrame.h"
#include "Task.h"



class Worker : public Task {
    public:
        Worker(const char* name, uint32_t stackSize=TASK_STACK_SIZE_DEFAULT, uint8_t priority=TASK_PRIORITY_DEFAULT)
            : Task(name, stackSize, priority), m_queue(nullptr) {

            m_queue = xQueueCreate(100, sizeof(DataFramePtr));

        }

        QueueHandle_t getQueue() {
            return m_queue;
        }


        DataFramePtr dequeue() {
            DataFramePtr dataPtr;
            if (xQueueReceive(m_queue, &dataPtr, 0) != pdTRUE) {
                return nullptr;
            }
            return dataPtr;
        }

        virtual void run(void *) = 0;

    protected:

    QueueHandle_t m_queue;

};
#endif  // _WORKER_TASK_H_