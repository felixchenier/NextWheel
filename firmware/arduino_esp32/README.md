# NEXT WHEEL v0.1.0

Welcome to NextWheel, the SmartWheel PCB/Firmware replacement for existing Smart Wheels, now discontinued from [Out-Front](https://out-front.com). This project uses the [PlatformIO](https://platformio.org/) extension for Visual Studio Code for compilation.

## Authors

* Dominic Létourneau (Firmware)
* Antoine Parrinello (PCB)
* Félix Chenier (Supervision)

## License

* [GPLv3](https://www.gnu.org/licenses/gpl-3.0.txt)

## Requirements for building the firmware

* [Zoom Recording for temporary reference (unlisted link)](https://uqam.ca.panopto.com/Panopto/Pages/Viewer.aspx?id=369eabaa-aeb1-4282-85cf-af47011472e2)

* [Visual Studio Code](https://code.visualstudio.com/download) (latest version)
* [PlatformIO extension](https://platformio.org/)
* In VSCode's new PlatformIO menu (left toolbar with alien icon), got to `PIO Home` > `Platforms` and install Espressif 32 Platform @ 5.x.x

## Coding style

* Use the clang-format Visual Studio Extension to follow coding style defined in the [.clang-format](.clang-format) file.

## Programming

> J14 and J15 jumpers must be removed before programming. This is required for the UART0 to work.
> It is recommended that you leave J14 and J15 jumpers unconnected to get the console output (serial monitor).

Steps:

1. Modify [lib/NextWheel/src/config/WiFiConfig.h](lib/NextWheel/src/config/WiFiConfig.h) with your WiFi information.
2. Go to the PlatformIO menu (left toolbar with alien icon)
3. Click on *Platform/Build the Filesystem Image* (static files that are stored in the flash memory)
4. Click on *Platform/Upload Filesystem Image*
5. Click on *General/Build*
6. Click on *General/Upload*

## Running

> Make sure J11 jumper is in the 2-3 position.

## Hardware

The following sections will describe the supported hardware / software modules.

### I2C

IMU: SEN0373 (BMX160 9-AXIS SENSOR MODULE)
Default address : 0x68

RTC: MCP7940M (Real time clock with battery backup)
Default address : 0xDE

### SPI

ADS8688  IDBTR

### WiFi / WebSocket Protocol

Once a WebSocket connection is established, the client and server exchange data via the WebSocket protocol in binary format : application messages, using the HTTP protocol, are split into one or more frames, adding a little overhead that needs to be considered, especially if we send small amount of data at once.

### WebSocket Binary Message Format

> Note 1: Bytes are ordered little endian (lsb first)
> Note 2: Protocol optimized for more efficiency using raw data instead. Conversions need to occur in client code.

| TYPE (uint8)   | TIMESTAMP (uint64)   | DATA SIZE (uint8)   | DATA (variable byte(s)) |
|----------------|----------------------|---------------------|-------------------------|
| 0=UNKNOWN      | INVALID              | 0 BYTE              | NONE                    |
| 1=CONFIG       | UNIX MICROSECONDS    | 20 BYTES            | 5x UINT32 (See [ConfigData](lib/NextWheel/src/config/GlobalConfig.h)) |
| 2=ADC          | UNIX MICROSECONDS    | 12 BYTES            | 6 CH x UINT16 (See [ADCDataFrame](lib/NextWheel/src/data/ADCDataFrame.h)) |
| 3=IMU          | UNIX MICROSECONDS    | 36 BYTES            | 9 FLOAT32 (AX,AY,AZ, GX,GY,GZ, MX,MY,MZ) (See [IMUDataFrame](lib/NextWheel/src/data/IMUDataFrame.h)) |
| 4=POWER        | UNIX MICROSECONDS    | 13 BYTES            | 3 FLOAT32 (V,I,P) + FLAGS (uint8) (See [PowerDataFrame](lib/NextWheel/src/data/PowerDataFrame.h)) |
| 5=RTC          | UNIX MICROSECONDS    | NOT IMPLEMENTED YET | NONE                    |
| 6=AUDIO        | UNIX MICROSECONDS    | NOT IMPLEMENTED YET | NONE                    |
| 7=QUADENCODER  | UNIX MICROSECONDS    | 8 BYTES             | 1 INT64 (See [QuadEncoderDataFrame](lib/NextWheel/src/data/QuadEncoderDataFrame.h))|
| 255=SUPERFRAME | UNIX MICROSECONDS    | NB INCLUDED FRAMES  | VARIABLE NUMBER OF FULL FRAMES |

> Note 2: To avoid sending small packets with high overhead ratio (data size small vs websocket overhead), the [WebSocketServerTask](src/tasks/WebSocketServerTask.h) sends periodic superframes of type 255 at a rate of 20Hz, wich is the aggregation of all accumulated frames in a 50ms period. This allows to maximize the bandwidth and minimize the TCP/IP embedded stack overhead. Every data frame is timstamped, so we can recover all data chronologically.

### ADC VALUE CONVERSION

VREF = 4.096V
RANGE (R1) = -1.25/+1.25
out_max = 1.25 * VREF
out_min = -1.25 * VREF
CONVERSION = (float)x * (out_max - out_min) / 65535. + out_min;
