#ifndef _ADC_TASK_H_
#define _ADC_TASK_H_

#include "tasks/SensorTask.h"
#include "ADC.h"

class ADCTask : public SensorTask {

    public:

    ADCTask() : SensorTask("ADC") {

    }

    virtual void run(void *) override {
        Serial.printf("ADCTask::run Priority: %li Core: %li \n", uxTaskPriorityGet(NULL), xPortGetCoreID());

        ADC adc;

        adc.begin();
        TickType_t lastGeneration = xTaskGetTickCount();
        ADCDataFrame frame;

        while (1) {
            //10 ms task
            vTaskDelayUntil(&lastGeneration, 1 / portTICK_RATE_MS);

            //Update values
            adc.update(frame);

            //Send data to registered queues
            sendData(frame);
        }
    }
};
#endif  // _ADC_TASK_H_