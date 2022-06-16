#ifndef _SDCARD_H_
#define _SDCARD_H_

#include <NextWheel.h>
#include "FS.h"
#include "SD_MMC.h"

class SDCard {
    public:
    SDCard();
    void begin();
    void update();

    void listDir(const char * dirname, uint8_t levels);

};

#endif // _SDCARD_H_
