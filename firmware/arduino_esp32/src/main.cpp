#include <Arduino.h>
#include <RTC.h>
#include <NextWheel.h>
#include <IMU.h>
#include <Power.h>
#include <SDCard.h>
#include <ADC.h>
#include <WebSocketServer.h>
#include "tasks/ADCTask.h"
#include "tasks/PrintWorkerTask.h"
#include "tasks/WebSocketServerTask.h"
#include "tasks/SDCardWorkerTask.h"

// IMU imu(IMU_I2C_ADDRESS);
// Power power(INA220_I2C_ADDRESS);
// RTC rtc;
// ADC adc;
// SDCard sdcard;
// WebSocketServer server;

ADCTask adcTask;
PrintWorkerTask printWorkerTask;
SDCardWorkerTask sdCardWorkerTask;
WebSocketServerTask webSocketServerTask(&sdCardWorkerTask);


void registerSensorTaskToQueues(SensorTask &task) {
    //task.registerDataQueue(printWorkerTask.getQueue());
    task.registerDataQueue(sdCardWorkerTask.getQueue());
    task.registerDataQueue(webSocketServerTask.getQueue());
}


void setup() {
    // put your setup code here, to run once:
    Serial.begin(115200);
    Serial.print("NextWheel version: ");
    Serial.println(NEXT_WHEEL_VERSION);

    //Note Arduino (loop) runs on core 1
    //WiFi, BLE runs on core 0


    // Must be first
    sdCardWorkerTask.setCore(1);
    sdCardWorkerTask.setPriority(TASK_PRIORITY_HIGH);

    printWorkerTask.setCore(0);
    printWorkerTask.setPriority(TASK_PRIORITY_IDLE);

    webSocketServerTask.setCore(0);
    webSocketServerTask.setPriority(TASK_PRIORITY_MEDIUM);

    adcTask.setCore(1);
    adcTask.setPriority(TASK_PRIORITY_HIGHEST);

    //Register to queues
    registerSensorTaskToQueues(adcTask);

    sdCardWorkerTask.start(nullptr);
    printWorkerTask.start(nullptr);
    webSocketServerTask.start(nullptr);
    adcTask.start(nullptr);

    // // IMU
    // imu.begin();

    // power.begin();

    // rtc.begin();

    //sdcard.begin();

    // adc.begin();

    // server.begin();
}

void loop() {

    //Default loop priority is TASK_PRIORITY_LOWEST (1)
    Serial.print("Main Loop: priority = ");
    Serial.println(uxTaskPriorityGet(NULL));

    Serial.print("Main Loop: Executing on core ");
    Serial.println(xPortGetCoreID());
  // put your main code here, to run repeatedly:

//   imu.update();

//   power.update();

//   rtc.update();

//   adc.update();

//   server.update();

//   delay(1000);

    TickType_t lastGeneration = xTaskGetTickCount();
    while(1) {


        // IDLE loop.
        //1000 ms task
        vTaskDelayUntil(&lastGeneration, 1000 / portTICK_RATE_MS);


        //ADC Stats
        // Serial.print("ADC: "); Serial.println(adcTask.getDataSentCounter());
        //Serial.println();
    }
}
