#ifndef _DAC_ACTUATOR_TASK_H_
#define _DAC_ACTUATOR_TASK_H_

#include "NextWheel.h"
#include <Arduino.h>
#include <freertos/queue.h>
#include "Task.h"

#ifdef _USE_INTERNAL_DAC_
    #include "DAC.h"
#endif


class DACActuatorTask: public Task {

    public:
        DACActuatorTask(const char* name="DACActuatorTask", uint32_t stackSize=TASK_STACK_SIZE_DEFAULT * 10, uint8_t priority=TASK_PRIORITY_DEFAULT);
        virtual void run(void *);

    private:

#ifdef _USE_INTERNAL_DAC_
    DAC m_dac;
#endif
};

#endif // _DAC_ACTUATOR_TASK_H_
