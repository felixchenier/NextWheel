#ifndef _SENSOR_TASK_H_
#define _SENSOR_TASK_H_

#include "NextWheel.h"
#include <Arduino.h>
#include <freertos/queue.h>
#include "Task.h"
#include "data/DataFrame.h"
#include <list>
#include <memory>

class SensorTask: public Task {

    public:
        SensorTask(const char* name, uint32_t stackSize=TASK_STACK_SIZE_DEFAULT, uint8_t priority=TASK_PRIORITY_DEFAULT)
            : Task(name, stackSize, priority), m_dataSentCounter(0) {

        }

        bool registerDataQueue(QueueHandle_t* queue) {
            if (queue == nullptr) {
                return false;
            }
            m_dataQueues.push_back(queue);
            return true;
        }

        bool unregisterDataQueue(QueueHandle_t* queue) {
            if (queue == nullptr) {
                return false;
            }
            m_dataQueues.remove(queue);
            return true;
        }

        bool sendData(const DataFrame &dataFrame) {
            if (m_dataQueues.empty()) {
                return false;
            }

            for (auto queue : m_dataQueues) {

                DataFrame* dataPtr = dataFrame.clone();

                if (dataPtr == nullptr) {
                    return false;
                }

                if (xQueueSend(*queue, &dataPtr, 0) != pdTRUE) {
                    Serial.print("Failed to send data to queue: ");
                    Serial.println(dataPtr->getType());
                    delete dataPtr;
                    return false;
                }
            }
            m_dataSentCounter++;
            return true;
        }

        size_t getDataSentCounter() {
            return m_dataSentCounter;
        }

        virtual void run(void *) = 0;

    protected:
        std::list<QueueHandle_t*> m_dataQueues;
        size_t m_dataSentCounter;
};

#endif // _SENSOR_TASK_H_
