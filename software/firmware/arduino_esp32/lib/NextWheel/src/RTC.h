#ifndef _RTC_H_
#define _RTC_H_

#include <Wire.h>
#include <NextWheel.h>
#include <MCP7940.h>

class RTC
{
public:
    RTC();
    void begin();
    void update();
    bool setTime(String time);
    void printTime();

private:
    MCP7940_Class m_mcp7940;
};

#endif  // _RTC_H_
