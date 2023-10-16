#include "RTC.h"

#define SPRINTF_BUFFER_SIZE 32

RTC::RTC() {}

void RTC::begin()
{
    // Initialize the RTC
    m_mcp7940.begin(I2C_FAST_MODE);

    // Set the system timezone
    // TODO Hardcoded for now...
    setenv("TZ", "EST+5EDT,M3.2.0/2,M11.1.0/2", 1);
    tzset();

    DateTime now = m_mcp7940.now();  // get the current time from RTC
    struct timeval my_time = { (time_t) now.unixtime(), 0 };
    settimeofday(&my_time, NULL);
}

void RTC::update()
{
    // Update the RTC
    // m_rtc.update();
    char inputBuffer[SPRINTF_BUFFER_SIZE];  // Buffer for sprintf()/sscanf()
    DateTime now = m_mcp7940.now();  // get the current time

    sprintf(
        inputBuffer,
        "%04d-%02d-%02d %02d:%02d:%02d",
        now.year(),  // Use sprintf() to pretty print
        now.month(),
        now.day(),
        now.hour(),
        now.minute(),
        now.second());  // date/time with leading zeros
    Serial.print(inputBuffer);  // Display the current date/time
}

void RTC::printTime()
{
    char inputBuffer[SPRINTF_BUFFER_SIZE];  // Buffer for sprintf()/sscanf()
    DateTime now = m_mcp7940.now();  // get the current time

    sprintf(
        inputBuffer,
        "%04d-%02d-%02d %02d:%02d:%02d",
        now.year(),  // Use sprintf() to pretty print
        now.month(),
        now.day(),
        now.hour(),
        now.minute(),
        now.second());  // date/time with leading zeros
    Serial.printf("Current time: %s \n", inputBuffer);  // Display the current date/time
}

bool RTC::setTime(String time)
{
    Serial.print("RTC::setTime : "); Serial.println(time);
    uint32_t unix_time = strtoul(time.c_str(), NULL, 10);
    Serial.println(unix_time);
    m_mcp7940.adjust(DateTime(unix_time));
    m_mcp7940.setBattery(true);  // enable battery

    struct timeval my_time;
    my_time.tv_sec = unix_time;
    my_time.tv_usec = 0;
    settimeofday(&my_time, NULL);
    return true;
}
