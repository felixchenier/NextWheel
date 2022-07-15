#include "LEDS.h"

void LEDS::begin()
{
    pinMode(PIN_LED_1, OUTPUT);
    digitalWrite(PIN_LED_1, HIGH);

    pinMode(PIN_LED_2, OUTPUT);
    digitalWrite(PIN_LED_2, HIGH);
}

void LEDS::setLED1(bool state)
{
    digitalWrite(PIN_LED_1, state);
}

void LEDS::setLED2(bool state)
{
    digitalWrite(PIN_LED_2, state);
}

void LEDS::toggleLED1()
{
    digitalWrite(PIN_LED_1, !digitalRead(PIN_LED_1));
}

void LEDS::toggleLED2()
{
    digitalWrite(PIN_LED_2, !digitalRead(PIN_LED_2));
}