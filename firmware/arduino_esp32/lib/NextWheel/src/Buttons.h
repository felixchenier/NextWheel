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

    void begin()
    {
        Serial.println("Buttons::begin()");
        setup_buttons_interrupt();
    }

    void setup_buttons_interrupt()
    {
        // Setup interrupt arduino
        pinMode(PIN_BUTTON_1, INPUT_PULLDOWN);
        attachInterrupt(PIN_BUTTON_1, NextWheelInterrupts::button1_interrupt, RISING);
        pinMode(PIN_BUTTON_2, INPUT_PULLDOWN);
        attachInterrupt(PIN_BUTTON_2, NextWheelInterrupts::button2_interrupt, RISING);
    }
};

#endif  // _BUTTONS_H_
