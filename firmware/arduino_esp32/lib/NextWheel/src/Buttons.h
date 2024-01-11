#ifndef _BUTTONS_H_
#define _BUTTONS_H_

#include "NextWheel.h"
#include <Arduino.h>
#include <list>


namespace NextWheelInterrupts
{
    // interrupts handling need to be implemented in the application
    extern void IRAM_ATTR button1_interrupt();
    extern void IRAM_ATTR button2_interrupt();
}

class Buttons
{
public:
    Buttons() = default;

    void begin();

    void setup_buttons_interrupt();

    bool button1Pressed();

    bool button2Pressed();
};

#endif  // _BUTTONS_H_
