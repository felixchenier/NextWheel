# NEXT WHEEL

Welcome to NextWheel, the SmartWheel PCB/Firmware replacement for existing Smart Wheels, now discontinued from [Out-Front](https://out-front.com). This project uses the [PlatformIO](https://platformio.org/) extension for Visual Studio Code for compilation.

## Authors

* Dominic Létourneau (Firmware)
* Antoine Parrinello (PCB)
* Félix Chenier (Supervision)

## License

* [GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt)

## Coding style

* Use the clang-format Visual Studio Extension to follow coding style defined in the [.clang-format](.clang-format) file.

## Programming

> J14 and J15 jumpers must be removed before programming. This is required for the UART0 to work.
> Put back J14 and J15 jumpers when the firmware is uploaded.

Steps:

1. Go to the PlatformIO menu (left toolbar with alien icon)
2. Click on *Build the Filesystem Image* (static files that are stored in the flash memory)
3. Click on *Upload Filesystem Image*
4. Click on *General/Upload*

## Running

> Make sure J14 and J15 jumpers are installed.
> Make sure J11 jumper is in the 2-3 position.

## Hardware

The following sections will describe the supported hardware / software modules.

### I2C

IMU: SEN0373 (BMX160 9-AXIS SENSOR MODULE)
Default address : 0x68

### SPI

ADS8688  IDBTR

### WiFi

Once a WebSocket connection is established, the client and server exchange data via the WebSocket protocol: application messages are split into one or more frames, each of which adds from 2 to 14 bytes of overhead.
