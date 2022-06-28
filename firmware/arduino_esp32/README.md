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

1. Modify [lib/NextWheel/src/config/WiFiConfig.h](lib/NextWheel/src/config/WiFiConfig.h) with your WiFi information.
2. Go to the PlatformIO menu (left toolbar with alien icon)
3. Click on *Build the Filesystem Image* (static files that are stored in the flash memory)
4. Click on *Upload Filesystem Image*
5. Click on *General/Upload*

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

### WiFi / WebSocket Protocol

Once a WebSocket connection is established, the client and server exchange data via the WebSocket protocol in binary format : application messages, using the HTTP protocol, are split into one or more frames, each of which adds from 2 to 14 bytes of overhead.

### WebSocket Binary Message Format

> Note 1: Bytes are ordered little endian (lsb first)

| TYPE (uint8)   | TIMESTAMP (uint64)   | DATA SIZE (uint8)   | DATA (variable byte(s)) |
|----------------|----------------------|---------------------|-------------------------|
| 0=UNKNOWN      | INVALID              | 0 BYTE              | NONE                    |
| 1=CONFIG       | UNIX MICROSECONDS    | NOT IMPLEMENTED YET | NONE                    |
| 2=ADC          | UNIX MICROSECONDS    | 32 BYTES            | 8 CH x FLOAT32          |
| 3=IMU          | UNIX MICROSECONDS    | 36 BYTES            | 9 FLOAT32 (AX,AY,AZ, GX,GY,GZ, MX,MY,MZ) |
| 4=POWER        | UNIX MICROSECONDS    | 13 BYTES            | 3 FLOAT32 (V,I,P) + FLAGS (uint8) |
| 5=RTC          | UNIX MICROSECONDS    | NOT IMPLEMENTED YET | NONE                    |
| 6=AUDIO        | UNIX MICROSECONDS    | NOT IMPLEMENTED YET | NONE                    |
| 255=SUPERFRAME | UNIX MICROSECONDS    | NB INCLUDED FRAMES  | VARIABLE NUMBER OF FULL FRAMES |

> Note 2: To avoid sending small packets with high overhead, the [WebSocketServerTask](src/tasks/WebSocketServerTask.h) sends periodic superframes of type 255 at a rate of 20Hz, wich is the aggregation of all accumulated frames in a 50ms period. This allows to maximize the bandwidth and minimize the TCP/IP embedded stack overhead.
