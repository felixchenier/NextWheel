#ifndef _PRINT_WORKER_TASK_H_
#define _PRINT_WORKER_TASK_H_

#include "tasks/WorkerTask.h"

class PrintWorkerTask : public WorkerTask
{
public:
    PrintWorkerTask() : WorkerTask("PrintWorkerTask") {}

    virtual void run(void* app) override
    {
        Serial.printf("PrintWorkerTask::run Priority: %li Core: %li \n", uxTaskPriorityGet(NULL), xPortGetCoreID());
        while (1)
        {
            DataFramePtr dataPtr = dequeue();
            if (dataPtr == nullptr)
            {
                continue;
            }
            dataPtr->print();
            delete dataPtr;
        }
    }
};

#endif  // _PRINT_WORKER_TASK_H_
