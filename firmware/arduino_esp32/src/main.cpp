#include <Arduino.h>
#include <NextWheel.h>
#include "NextWheelApp.h"

//Global app object
NextWheelApp app;

void setup() {
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

        if (app.isRecording()) {
            app.getLEDS().toggleLED1();
        }
        else {
            app.getLEDS().setLED1(false);
        }

        // IDLE loop.
        //1000 ms task
        vTaskDelayUntil(&lastGeneration, 1000 / portTICK_RATE_MS);
    }
}
