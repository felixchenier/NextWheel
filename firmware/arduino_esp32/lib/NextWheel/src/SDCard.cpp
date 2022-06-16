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
        #define PIN_SD_CMD 15
        #define PIN_SD_CLK 14
    */
    gpio_pullup_en(GPIO_NUM_2);
    gpio_pullup_en(GPIO_NUM_4);
    gpio_pullup_en(GPIO_NUM_12);
    gpio_pullup_en(GPIO_NUM_13);
    gpio_pullup_en(GPIO_NUM_15);
    gpio_pullup_en(GPIO_NUM_14);

    //SD_MMC.setPins(PIN_SD_CLK, PIN_SD_CMD, PIN_SD_DAT0, PIN_SD_DAT1, PIN_SD_DAT2, PIN_SD_DAT3); //CLK, CMD, D0, D1, D2, D3
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
    Serial.printf("Total space: %lluMB\n", SD_MMC.totalBytes() / (1024 * 1024));
    Serial.printf("Used space: %lluMB\n", SD_MMC.usedBytes() / (1024 * 1024));

    //listDir("/", 0);
    Serial.println();
}

void SDCard::listDir(const char * dirname, uint8_t levels)
{
    Serial.printf("Listing directory: %s\n", dirname);

    File root = SD_MMC.open(dirname);
    if(!root){
        Serial.println("Failed to open directory");
        return;
    }
    if(!root.isDirectory()){
        Serial.println("Not a directory");
        return;
    }

    File file = root.openNextFile();
    while(file){
        if(file.isDirectory()){
            Serial.print("  DIR : ");
            Serial.println(file.name());
            if(levels){
                listDir(file.path(), levels -1);
            }
        } else {
            Serial.print("  FILE: ");
            Serial.print(file.name());
            Serial.print("  SIZE: ");
            Serial.println(file.size());
        }
        file = root.openNextFile();
    }
}