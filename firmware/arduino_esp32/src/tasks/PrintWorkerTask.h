#ifndef _PRINT_WORKER_TASK_H_
#define _PRINT_WORKER_TASK_H_

#include "tasks/WorkerTask.h"

class PrintWorkerTask : public WorkerTask
{
public:
    PrintWorkerTask();

    virtual void run(void* app) override;
};

#endif  // _PRINT_WORKER_TASK_H_
