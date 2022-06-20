#include "RTC.h"

#define SPRINTF_BUFFER_SIZE 32

RTC::RTC() {

}

void RTC::begin() {
    // Initialize the RTC
    m_mcp7940.begin(I2C_FAST_MODE);

    DateTime now = m_mcp7940.now();  // get the current time

    if (now.year() < 2022) {
        Serial.print("RTC has not been set yet. Doing so now.");
        // RTC has not been set yet, so use the current time
        m_mcp7940.adjust(DateTime(2022, 6, 20, 8, 50, 0));
        m_mcp7940.setBattery(true); //enable battery
   }

    // Re-Update time
    now = m_mcp7940.now();

    // Set the system time
    setenv("TZ", "EST+5EDT,M3.2.0/2,M11.1.0/2", 1);
    tzset();

    struct tm tm;
    tm.tm_year = now.year() - 1900;
    tm.tm_mon = now.month() - 1;
    tm.tm_mday = now.day();
    tm.tm_hour = now.hour();
    tm.tm_min = now.minute();
    tm.tm_sec = now.second();
    time_t t = mktime(&tm);

    Serial.printf("Setting system time: %s \n", asctime(&tm));
    struct timeval my_time;
    my_time.tv_sec = t;
    my_time.tv_usec = 0;
    settimeofday(&my_time, NULL);

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
