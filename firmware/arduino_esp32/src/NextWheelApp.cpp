#include "NextWheelApp.h"

NextWheelApp* NextWheelApp::m_instance = nullptr;

// Singleton pattern
NextWheelApp* NextWheelApp::instance()
{
    if (m_instance == nullptr)
    {
        m_instance = new NextWheelApp();
    }
    return m_instance;
}

namespace NextWheelInterrupts
{
    // interrupts
    // WARNING No Serial.print allowed in interrupts

    void IRAM_ATTR button1_interrupt()
    {
        // Get the state of the button
        // Start recording from ISR
        bool state = digitalRead(PIN_BUTTON_1);
        if (state)
        {
            NextWheelApp::instance()->startRecording(true);
        }
    }

    void IRAM_ATTR button2_interrupt()
    {
        // Get the state of the button
        // Stop recording from ISR
        bool state = digitalRead(PIN_BUTTON_2);
        if (state)
        {
            NextWheelApp::instance()->stopRecording(true);
        }
    }
}