#include <Arduino.h>
#include <SPI.h>
#include <WiFiNINA.h>
#include <PDM.h>

// default number of output channels
static const char channels = 1;

// default PCM output frequency
static const int frequency = 8000;

// Buffer to read samples into, each sample is 16-bits
short sampleBuffer[512] = { 0 };

// Number of audio samples read
volatile int samplesRead = 0;
volatile int sampleFlushed = 0;


bool LED_SWITCH = false;

/* WIRING
  In order to use the Adafruit lsm6dsox sensor with a ST nucleo board,
  plug Nucleo "+3.3V" to AdafruitLSM6DOX "VIN",
  plug Nucleo "GND" to AdafruitLSM6DOX "GND",
  plug Nucleo "SCL"(D15) to AdafruitLSM6DOX "SCL",
  plug Nucleo "SDA"(D14) to AdafruitLSM6DOX "SDA".*/

#include "LSM6DSOXSensor.h"

#define SR 833 // Sample rate. Options are: 12.5, 26, 52, 104, 208, 417, 833, 1667, 3333 and 6667 Hz.
#define WTM_LV 2 // Watermark threshold level. Max samples in this FIFO configuration is 512 (accel and gyro only).

/** LSM6DSOX i2c address:
 * LSM6DSOX_I2C_ADD_L: 0x6A (default)
 * LSM6DSOX_I2C_ADD_H: 0x6B 
 **/
LSM6DSOXSensor lsm6dsoxSensor = LSM6DSOXSensor(&Wire, LSM6DSOX_I2C_ADD_L);


/**
   Callback function to process the data from the PDM microphone.
   NOTE: This callback is executed as part of an ISR.
   Therefore using `Serial` to print messages inside this function isn't supported.
 * */
void onPDMdata() {
  // Query the number of available bytes
  int bytesAvailable = PDM.available();

  // Read into the sample buffer
  PDM.read(sampleBuffer, bytesAvailable);

  if (samplesRead != 0) {
    sampleFlushed += samplesRead;
  }
  else {
    sampleFlushed = 0;
  }

  // 16-bit, 2 bytes per sample
  samplesRead = bytesAvailable / 2;


}


void setup() {

  Serial.begin(115200);
  
  //pinMode(LEDB, OUTPUT);
  
  // Comment this line to skip waiting for serial:
  while(!Serial) delay(10);
  

  // Configure the data receive callback
  PDM.onReceive(onPDMdata);
  PDM.setBufferSize(512);

  // Optionally set the gain
  // Defaults to 20 on the BLE Sense and -10 on the Portenta Vision Shield
  // PDM.setGain(30);

  // Initialize PDM with:
  // - one channel (mono mode)
  // - a 16 kHz sample rate for the Arduino Nano 33 BLE Sense
  // - a 32 kHz or 64 kHz sample rate for the Arduino Portenta Vision Shield
  if (!PDM.begin(channels, frequency)) {
    Serial.println("Failed to start PDM!");
    while (1);
  }

  // i2c, fast mode plus
  Wire.begin();
  Wire.setClock(1000000);

  // Initialize sensors
  lsm6dsoxSensor.begin();
  if (lsm6dsoxSensor.Enable_G() == LSM6DSOX_OK && lsm6dsoxSensor.Enable_X() == LSM6DSOX_OK) {
    Serial.println("Success enabling accelero and gyro");
  } else {
    Serial.println("Error enabling accelero and gyro");
    abort();
  }

  // Check device id
  uint8_t id;
  lsm6dsoxSensor.ReadID(&id);
  if (id != LSM6DSOX_ID) {
    Serial.println("Wrong id for LSM6DSOX sensor. Check that device is plugged");
    abort();
  } else {
    Serial.println("Success checking id for LSM6DSOX sensor");
  }

  // Set accelerometer scale. Available values are: 2, 4, 8, 16 G
  lsm6dsoxSensor.Set_X_FS(16);
  // Set gyroscope scale. Available values are: 125, 250, 500, 1000, 2000 dps
  lsm6dsoxSensor.Set_G_FS(2000);
  
  // Set accelerometer Output Data Rate. Available values are: 1.6, 12.5, 26, 52, 104, 208, 417, 833, 1667, 3333, 6667 Hz
  lsm6dsoxSensor.Set_X_ODR(SR);
  // Set gyroscope Output Data Rate. Available values are 12.5, 26, 52, 104, 208, 417, 833, 1667, 3333, 6667 Hz
  lsm6dsoxSensor.Set_G_ODR(SR);
  
  // Set FIFO Batch Data Rate for accelerometer and gyroscope. Available values are: 0, 12.5, 26, 52, 104, 208, 417, 833, 1667, 3333, 6667 Hz
  lsm6dsoxSensor.Set_FIFO_X_BDR(SR);
  lsm6dsoxSensor.Set_FIFO_G_BDR(SR);

  /** Set FIFO operation mode. Available values are:
   * LSM6DSOX_BYPASS_MODE: FIFO is not used, the buffer content is cleared
   * LSM6DSOX_FIFO_MODE: bufer continues filling until it becomes full. Then it stops collecting data.
   * LSM6DSOX_STREAM_MODE: continuous mode. Older data are replaced by the new data.
   * LSM6DSOX_STREAM_TO_FIFO_MODE: FIFO buffer starts operating in Continuous mode and switches to FIFO mode when an event condition occurs.
   * LSM6DSOX_BYPASS_TO_STREAM_MODE: FIFO buffer starts operating in Bypass mode and switches to Continuous mode when an event condition occurs.
   * */
  lsm6dsoxSensor.Set_FIFO_Mode(LSM6DSOX_BYPASS_MODE); // flush any previous value in FIFO before start
  lsm6dsoxSensor.Set_FIFO_Mode(LSM6DSOX_STREAM_MODE); // start batching in continous mode
  
  // Set FIFO watermark level. Can be used to check when the number of samples in buffer reaches this defined threshold level.
  lsm6dsoxSensor.Set_FIFO_Watermark_Level(WTM_LV);
  
  // FIFO size can be limited to the watermark level by setting the STOP_ON_WTM flag to 1
  //lsm6dsoxSensor.Set_FIFO_Stop_On_Fth(1);

  Serial.println("Starting...");
}

void loop() {

  static uint8_t wtmStatus = 0; // FIFO watermark status
  uint8_t fullStatus = 0; // FIFO full status
  uint16_t numSamples = 0; // number of samples in FIFO
  uint8_t Tag; // FIFO data sensor identifier
  int32_t acceleration[3]; // X, Y, Z accelerometer values in mg
  int32_t rotation[3]; // X, Y, Z giroscope values in mdps

  // Get number of samples in buffer
  lsm6dsoxSensor.Get_FIFO_Num_Samples(&numSamples);
  

  // Check if FIFO threshold level was reached.
  lsm6dsoxSensor.Get_FIFO_Watermark_Status(&wtmStatus);

  if (wtmStatus != 0) {
    //Serial.print("Samples in FIFO: "); Serial.println(numSamples);
    //Serial.println("-- FIFO Watermark level reached!, fetching data.");

    // fetch data from FIFO
    for (uint16_t i = 0; i < WTM_LV; i++) {

      lsm6dsoxSensor.Get_FIFO_Tag(&Tag); // get data identifier
      
      // Get gyroscope data
      if (Tag == 1) { 
        lsm6dsoxSensor.Get_FIFO_G_Axes(rotation);
        #if 0 // set to 1 for printing values
        Serial.print("mdps: "); Serial.print(rotation[0]); 
        Serial.print(", "); Serial.print(rotation[1]); 
        Serial.print(", "); Serial.print(rotation[2]); 
        Serial.println();
        #endif
      } 


      
      // Get accelerometer data
      else if (Tag == 2) {
        lsm6dsoxSensor.Get_FIFO_X_Axes(acceleration); 
        #if 0 // set to 1 for printing values
        Serial.print("mG: "); Serial.print(acceleration[0]); 
        Serial.print(", "); Serial.print(acceleration[1]); 
        Serial.print(", "); Serial.print(acceleration[2]); 
        Serial.println();
        #endif
      }
    }
  }

  // Check if FIFO is full.
  lsm6dsoxSensor.Get_FIFO_Full_Status(&fullStatus);

  if (fullStatus != 0) {
    lsm6dsoxSensor.Get_FIFO_Num_Samples(&numSamples);
    Serial.print("Samples in FIFO: "); Serial.println(numSamples);

    Serial.println("-- FIFO is full!, consider reducing Watermark Level or Buffer Data Rate.\nFlushing data from FIFO.");
    lsm6dsoxSensor.Set_FIFO_Mode(LSM6DSOX_BYPASS_MODE); // flush FIFO data
    lsm6dsoxSensor.Set_FIFO_Mode(LSM6DSOX_STREAM_MODE); // continue batching
  }


  // Wait for samples to be read
  if (samplesRead) {
    
    if (sampleFlushed)
    {
      Serial.print("Num audio samples :");
      Serial.println(samplesRead);
      Serial.println(sampleFlushed);
    }
    // Print samples to the serial monitor or plotter
    for (int i = 0; i < samplesRead; i++) {
      //Serial.println(sampleBuffer[i]);
    }

    // Clear the read count
    samplesRead = 0;
  }


  //delay(10); // FIFO continues batching while we sleep 
}