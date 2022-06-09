#include "RTC.h"

#define SPRINTF_BUFFER_SIZE 32

RTC::RTC() {

}

void RTC::begin() {
    // Initialize the RTC
    m_mcp7940.begin();

    DateTime now = m_mcp7940.now();  // get the current time

    if (now.year() < 2022) {
        // RTC has not been set yet, so use the current time
        m_mcp7940.adjust(DateTime(2022, 1, 1, 0, 0, 0));
    }

}

void RTC::update() {
    // Update the RTC
    //m_rtc.update();
    char inputBuffer[SPRINTF_BUFFER_SIZE];  // Buffer for sprintf()/sscanf()
    DateTime now = m_mcp7940.now();  // get the current time

    sprintf(inputBuffer, "%04d-%02d-%02d %02d:%02d:%02d",
            now.year(),  // Use sprintf() to pretty print
            now.month(), now.day(), now.hour(), now.minute(),
            now.second());                         // date/time with leading zeros
    Serial.print(inputBuffer);                     // Display the current date/time

}
