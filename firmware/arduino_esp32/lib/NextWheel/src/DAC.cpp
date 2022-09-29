#include "DAC.h"
//#include "I2S.h"

#include "driver/dac.h"
#include "driver/i2s.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#if 0
void DAC::setup() {

    // Configure the I2S peripheral
    // Use only DAC channel 1
    // Use 16 bit data
    // Use 8kHz sample rate

    //dac_output_enable(DAC_CHANNEL_1);
    //dac_output_voltage(DAC_CHANNEL_1, 0);
    //dac_i2s_enable();

    //I2S.setBufferSize(800); // 100ms buffer, max 1024...

    //ADC MODE WILL USE 2 CHANNELS
    // PIN 25 CONFIGURED AS DAC CH1
    // PIN 26 CONFIGURED AS DAC CH2 (J8, unused)
    // PIN 33 CONFIGURED AS ADC CH1 (J8, unused)
    I2S.setDataInPin(33);
    I2S.setDataOutPin(25);
    I2S.setSckPin(26);
    I2S.setFsPin(27);

    if (!I2S.begin(ADC_DAC_MODE, 16000, 16)) {
        Serial.println("Failed to initialize I2S!");
    }
    else
    {
        Serial.println("I2S initialized!");
    }
    //I2S.setPin(I2S_PIN_DAC1);



    /*

    // Configure the I2S peripheral, right channel is GPIO 25
    i2s_config_t i2s_config;



    i2s_config.mode = (i2s_mode_t) (I2S_MODE_MASTER | I2S_MODE_TX | I2S_MODE_DAC_BUILT_IN);
    i2s_config.sample_rate =  8000;
    i2s_config.bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT;
    i2s_config.communication_format = I2S_COMM_FORMAT_STAND_MSB;
    i2s_config.channel_format = I2S_CHANNEL_FMT_ONLY_RIGHT;
    i2s_config.intr_alloc_flags = 0;
    i2s_config.dma_buf_count = 2;
    i2s_config.dma_buf_len = 1024;
    i2s_config.use_apll = 0;
    //i2s_config.tx_desc_auto_clear = 1;

    // Install and start I2S driver, NUM_0 supports DAC built-in
    if (i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL) != ESP_OK) {
        Serial.println("I2S driver install failed");
    }
    else {
        Serial.println("I2S driver install success");
    }

    // Setup DAC
    if (i2s_set_dac_mode(I2S_DAC_CHANNEL_RIGHT_EN) != ESP_OK) {
        Serial.println("I2S set dac mode failed");
    }
    else
    {
        Serial.println("I2S set dac mode success");
    }
    */


    /*
    dac_output_enable(DAC_CHANNEL_1);
    dac_output_voltage(DAC_CHANNEL_1, 0);

    dac_i2s_enable();

    if (!I2S.begin(ADC_DAC_MODE, 8000, 16))
    {
        Serial.println("I2S failed to start");
    }
    else
    {
        Serial.println("I2S started");
    }
    */

}
#endif

 DAC::DAC() {
    m_sample_rate = 8000;
 }

void DAC::setup() {

    //i2s configuration
    int i2s_num = 0; // i2s port number

    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX | I2S_MODE_DAC_BUILT_IN),
        .sample_rate = m_sample_rate,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT, /* the DAC module will only take the 8bits from MSB */
        .channel_format = I2S_CHANNEL_FMT_ONLY_RIGHT,
        .communication_format = (i2s_comm_format_t)I2S_COMM_FORMAT_STAND_MSB,
        .intr_alloc_flags = 0, // default interrupt priority
        .dma_buf_count = 8,
        .dma_buf_len = 64,
        .use_apll = 1
    };

    //initialize i2s with configurations above
    if (i2s_driver_install((i2s_port_t)i2s_num, &i2s_config, 0, NULL) != ESP_OK) {
        Serial.println("I2S driver install failed");
    }
    else {
        Serial.println("I2S driver install success");
    }



    // Setup DAC
    if (i2s_set_dac_mode(I2S_DAC_CHANNEL_RIGHT_EN) != ESP_OK) {
        Serial.println("I2S set dac mode failed");
    }
    else
    {
        Serial.println("I2S set dac mode success");
    }

/*
    if (i2s_set_pin((i2s_port_t)i2s_num, NULL) != ESP_OK) {
        Serial.println("I2S set pin failed");
    }
    else {
        Serial.println("I2S set pin success");
    }
*/

    //set sample rates of i2s to sample rate of wav file
    if (i2s_set_sample_rates((i2s_port_t)i2s_num, m_sample_rate) != ESP_OK) {
        Serial.println("I2S set sample rates failed");
    }
    else {
        Serial.println("I2S set sample rates success");
    }

}

void DAC::setVoltage(uint8_t voltage)
{
    #if 0
    dac_output_voltage(DAC_CHANNEL_1, voltage); //(VDD * 200 / 255)
    #endif
}

size_t DAC::writeFrame(const void *samples, uint32_t length)
{
    size_t bytesWritten = 0;
    if (i2s_write(I2S_NUM_0, samples, length, &bytesWritten, portMAX_DELAY) != ESP_OK) {
        Serial.println("I2S write failed");
    }
    return bytesWritten;
}