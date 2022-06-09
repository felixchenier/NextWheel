# NEXT WHEEL

Welcome to NextWheel, the SmartWheel PCB/Firmware replacement for existing Smart Wheels, now discontinued from [Out-Front](https://out-front.com). This project uses the [PlatformIO](https://platformio.org/) extension for Visual Studio Code for compilation.

## Programming

> J14 and J15 jumpers must be removed before programming. This is required for the UART0 to work.
> Put back J14 and J15 jumpers when the firmware is uploaded.

## Running

> Make sure J14 and J15 jumpers are installed.
> Make sure J11 is in the 2-3 position.

## Hardware

The following sections will describe the supported hardware / software modules.

### I2C

IMU: SEN0373 (BMX160 9-AXIS SENSOR MODULE)
Default address : 0x68

### SPI

ADS8688  IDBTR


