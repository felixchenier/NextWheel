#include "ADC.h"
#include "DataFrame.h"

ADC::ADC()
: m_ads8688(PIN_SPI_CS1)  {

}

void ADC::begin()
{
    m_ads8688.setChannelSPD(0b11111111);
    m_ads8688.setGlobalRange(R1);              // set range for all channels
    m_ads8688.autoRst();                       // reset auto sequence
}

void ADC::update() {

    Serial.println("ADC values: ");             // print label
    DataFrame<float> frame(DATA_FRAME_TYPE_ADC, nullptr, 8);
    for (byte i=0;i<8;i++) {

        uint16_t val = m_ads8688.noOp();         // trigger samples
        frame.setDataItem(i, m_ads8688.I2V(val,R1));

        //Serial.print(m_ads8688.I2V(val,R1));     // print value in Volts
        //Serial.println(i!=7?" V | ":" V");  // print Volt label
    }



    frame.print();
}