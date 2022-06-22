#ifndef _LEDS_H_
#define _LEDS_H_

#include <Arduino.h>
#include "NextWheel.h"

class LEDS {
    public:

    const static int LED_COUNT = 2;

    LEDS() = default;

    void begin() {
        pinMode(PIN_LED_1, OUTPUT);
        digitalWrite(PIN_LED_1, HIGH);

        pinMode(PIN_LED_2, OUTPUT);
        digitalWrite(PIN_LED_2, HIGH);
    }

    void setLED1(bool state) {
        digitalWrite(PIN_LED_1, state);
    }

    void setLED2(bool state) {
        digitalWrite(PIN_LED_2, state);
    }

    void toggleLED1() {
        digitalWrite(PIN_LED_1, !digitalRead(PIN_LED_1));
    }

    void toggleLED2() {
        digitalWrite(PIN_LED_2, !digitalRead(PIN_LED_2));
    }
};

#endif // _LEDS_H_
