#include "SDCard.h"


SDCard::SDCard()
{

}

void SDCard::begin()
{


    /*
        #define PIN_SD_DAT0 2
        #define PIN_SD_DAT1 4
        #define PIN_SD_DAT2 12
        #define PIN_SD_DAT3 13
        #define PIN_SD_CMD 25 //Not on default pin, should be 15
        #define PIN_SD_CLK 14
    */
    SD_MMC.setPins(PIN_SD_CLK, PIN_SD_CMD, PIN_SD_DAT0, PIN_SD_DAT1, PIN_SD_DAT2, PIN_SD_DAT3); //CLK, CMD, D0, D1, D2, D3
    if (!SD_MMC.begin()) {
        Serial.println("SD_MMC.begin() failed");
        delay(10000);
        return;
    }
}

void SDCard::update()
{
    Serial.println();
    Serial.print("SDCard type: "); Serial.println(SD_MMC.cardType());
    Serial.print("SDCard size: "); Serial.println(SD_MMC.cardSize());
    Serial.println();
}