#include "PrintWorkerTask.h"

PrintWorkerTask::PrintWorkerTask() : WorkerTask("PrintWorkerTask") {}


void PrintWorkerTask::run(void* app)
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