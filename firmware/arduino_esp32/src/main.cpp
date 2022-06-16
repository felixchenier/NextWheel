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

// IMU imu(IMU_I2C_ADDRESS);
// Power power(INA220_I2C_ADDRESS);
// RTC rtc;
// ADC adc;
SDCard sdcard;
// WebSocketServer server;

ADCTask adcTask;
PrintWorkerTask printWorkerTask;
WebSocketServerTask webSocketServerTask;

void setup() {
    // put your setup code here, to run once:
    Serial.begin(115200);
    Serial.print("NextWheel version: ");
    Serial.println(NEXT_WHEEL_VERSION);

    printWorkerTask.setCore(1);
    printWorkerTask.setPriority(TASK_PRIORITY_LOW);

    webSocketServerTask.setCore(1);
    webSocketServerTask.setPriority(TASK_PRIORITY_MEDIUM);

    adcTask.setCore(0);
    adcTask.setPriority(TASK_PRIORITY_HIGH);

    // adcTask.registerDataQueue(printWorkerTask.getQueue());
    adcTask.registerDataQueue(webSocketServerTask.getQueue());

    printWorkerTask.start(nullptr);
    webSocketServerTask.start(nullptr);
    adcTask.start(nullptr);

    // // IMU
    // imu.begin();

    // power.begin();

    // rtc.begin();

    sdcard.begin();

    // adc.begin();

    // server.begin();
}

void loop() {
  // put your main code here, to run repeatedly:

//   imu.update();

//   power.update();

//   rtc.update();



//   adc.update();

//   server.update();

//   delay(1000);

    TickType_t lastGeneration = xTaskGetTickCount();
    while(1) {

        //sdcard.update();

        // IDLE loop.
        //1000 ms task
        vTaskDelayUntil(&lastGeneration, 1000 / portTICK_RATE_MS);


        //ADC Stats
        Serial.print("ADC: "); Serial.println(adcTask.getDataSentCounter());
        Serial.println();
    }
}
