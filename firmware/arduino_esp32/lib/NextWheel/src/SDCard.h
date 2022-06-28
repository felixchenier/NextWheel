#ifndef _SDCARD_H_
#define _SDCARD_H_

#include <NextWheel.h>
#include "FS.h"
#include "SD_MMC.h"
#include "data/DataFrame.h"

class SDCard
{
public:
    SDCard();
    void begin();
    void update();
    void end();
    void listFiles();
    void listDir(const char* dirname, uint8_t levels);
    File openNewLogFile(const char* filename);
    size_t writeToLogFile(File file, const DataFrame& frame);
};

#endif  // _SDCARD_H_
