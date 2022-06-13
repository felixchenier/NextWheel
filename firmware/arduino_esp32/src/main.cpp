#include <Arduino.h>
#include <RTC.h>
#include <NextWheel.h>
#include <IMU.h>
#include <Power.h>
//#include <SDCard.h>
#include <ADC.h>
#include <WebSocketServer.h>

IMU imu(IMU_I2C_ADDRESS);
Power power(INA220_I2C_ADDRESS);
RTC rtc;
ADC adc;
//SDCard sdcard;
WebSocketServer server;

void setup() {
    // put your setup code here, to run once:
    Serial.begin(115200);
    Serial.print("NextWheel version: ");
    Serial.println(NEXT_WHEEL_VERSION);

    // IMU
    imu.begin();

    power.begin();

    rtc.begin();

    //sdcard.begin();

    adc.begin();

    server.begin();
}

void loop() {
  // put your main code here, to run repeatedly:

  imu.update();

  power.update();

  rtc.update();

  //sdcard.update();

  adc.update();

  server.update();

  delay(1000);
}