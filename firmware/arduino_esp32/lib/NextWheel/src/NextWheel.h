#ifndef _NEXT_WHEEL_H_
#define _NEXT_WHEEL_H_

#include "WiFiConfig.h"

/*
    NextWheel  - Global definitions and macros
*/
#define NEXT_WHEEL_VERSION "0.1.0"
#define NEXT_WHEEL_DEBUG_LEVEL 0


// PIN DEFINITIONS
// REFER TO https://docs.espressif.com/projects/esp-idf/en/latest/esp32/hw-reference/esp32/get-started-devkitc.html


// I2C on default pins
#define PIN_I2C_SDA 21
#define PIN_I2C_SCL 22

// SPI on default pins
#define PIN_SPI_MOSI 23
#define PIN_SPI_MISO 19
#define PIN_SPI_CLK 18
#define PIN_SPI_CS1 5
#define PIN_SPI_CS2 15 //WARNING - this should be 25

// SD Card 4 bits not on all default pins, SDMMC (SLOT1)
// https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/sdmmc_host.html
#define PIN_SD_DAT0 2
#define PIN_SD_DAT1 4
#define PIN_SD_DAT2 12
#define PIN_SD_DAT3 13
#define PIN_SD_CMD 25 //Not on default pin, should be 15
#define PIN_SD_CLK 14


// WARNING: Jumper must be removed to use the IMU's interrupt pins.
// WARNING: If jumper is removed, programming will be disabled.
#define PIN_IMU_INT1 1 //TXD0
#define PIN_IMU_INT2 3 //RXD0


// BUTTONS
#define PIN_BUTTON_1 36
#define PIN_BUTTON_2 39

// LEDS
#define PIN_LED_1 17
#define PIN_LED_2 16

// ENCODERS
#define PIN_QUAD_ENCODER_A 35
#define PIN_QUAD_ENCODER_B 0

// I2S
#define PIN_I2S_SDATA 33
#define PIN_I2S_SCLK 26
#define PIN_I2S_LRCLK_WS 27

// EMERGENCY STOP / LOW POWER
#define PIN_EMERGENCY_STOP_LOW_POWER_N 34

// ENABLE SENSORS POWER
#define PIN_ENABLE_SENSOR_POWER 32


// TASKS
#define TASK_PRIORITY_LOWEST 0
#define TASK_PRIORITY_LOW 1
#define TASK_PRIORITY_MEDIUM 2
#define TASK_PRIORITY_HIGH 3
#define TASK_PRIORITY_HIGHEST 4
#define TASK_PRIORITY_IDLE 5
#define TASK_PRIORITY_DEFAULT TASK_PRIORITY_MEDIUM
#define TASK_STACK_SIZE_DEFAULT 2048



#endif
