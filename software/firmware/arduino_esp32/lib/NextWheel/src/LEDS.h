#ifndef _LEDS_H_
#define _LEDS_H_

#include <Arduino.h>
#include "NextWheel.h"

class LEDS
{
public:
    const static int LED_COUNT = 2;

    LEDS() = default;

    void begin();

    void setLED1(bool state);

    void setLED2(bool state);

    void toggleLED1();

    void toggleLED2();
};
#endif  // _LEDS_H_
