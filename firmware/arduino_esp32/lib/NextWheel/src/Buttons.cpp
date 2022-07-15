#include "Buttons.h"


void Buttons::begin()
{
    Serial.println("Buttons::begin()");
    setup_buttons_interrupt();
}

void Buttons::setup_buttons_interrupt()
{
    // Setup interrupt arduino
    // No internal pullup or down on those pins
    pinMode(PIN_BUTTON_1, INPUT);
    attachInterrupt(PIN_BUTTON_1, NextWheelInterrupts::button1_interrupt, RISING);
    pinMode(PIN_BUTTON_2, INPUT);
    attachInterrupt(PIN_BUTTON_2, NextWheelInterrupts::button2_interrupt, RISING);
}