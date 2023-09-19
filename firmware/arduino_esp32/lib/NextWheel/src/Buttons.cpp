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
    // Hardware bug on the ESP32, not recommended to use interrupts on GPIN 36 and 39
    //attachInterrupt(PIN_BUTTON_1, NextWheelInterrupts::button1_interrupt, RISING);
    pinMode(PIN_BUTTON_2, INPUT);
    //attachInterrupt(PIN_BUTTON_2, NextWheelInterrupts::button2_interrupt, RISING);
}

bool Buttons::button1Pressed()
{
    return digitalRead(PIN_BUTTON_1) == HIGH;
}

bool Buttons::button2Pressed()
{
    return digitalRead(PIN_BUTTON_2) == HIGH;
}
