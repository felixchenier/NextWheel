#include <Arduino.h>

#include <NextWheel.h>
#include <IMU.h>
#include <Power.h>
#include <RTC.h>
#include "NextWheelApp.h"

RTC rtc;
NextWheelApp app;

void setup() {

    // put your setup code here, to run once:
    // Serial must be initialized for prints
    Serial.begin(115200);

    //First thing we set the system to current time
    rtc.begin();


    Serial.print("NextWheel version: ");
    Serial.println(NEXT_WHEEL_VERSION);

    // Setup app
    app.begin();

    // Start tasks
    app.start();
}

void loop() {
    // Note Arduino (loop) runs on core 1
    // WiFi, BLE runs on core 0
    // Default loop priority is TASK_PRIORITY_LOWEST (1)
    Serial.print("Main Loop: priority = ");
    Serial.println(uxTaskPriorityGet(NULL));

    Serial.print("Main Loop: Executing on core ");
    Serial.println(xPortGetCoreID());


    TickType_t lastGeneration = xTaskGetTickCount();
    while(1) {

        struct timeval timeval_now;
        gettimeofday(&timeval_now, NULL);

        // IDLE loop.
        //1000 ms task
        vTaskDelayUntil(&lastGeneration, 1000 / portTICK_RATE_MS);

        //ADC Stats
        // Serial.print("ADC: "); Serial.println(adcTask.getDataSentCounter());
        //Serial.println();
    }
}
