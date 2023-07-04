#ifndef _DAC_ACTUATOR_TASK_H_
#define _DAC_ACTUATOR_TASK_H_

#include "NextWheel.h"
#include <Arduino.h>
#include <freertos/queue.h>
#include "Task.h"
#include "DAC.h"

class DACActuatorTask: public Task {

    public:
        DACActuatorTask(const char* name="DACActuatorTask", uint32_t stackSize=TASK_STACK_SIZE_DEFAULT * 10, uint8_t priority=TASK_PRIORITY_DEFAULT);
        virtual void run(void *);

    private:

    DAC m_dac;

};

#endif // _DAC_ACTUATOR_TASK_H_
