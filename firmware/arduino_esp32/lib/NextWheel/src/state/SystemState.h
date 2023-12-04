#ifndef _SYSTEM_STATE_H_
#define _SYSTEM_STATE_H_


#include "NextWheel.h"
#include <Arduino.h>

class SystemState
{
public:
    struct State
    {
        State()
        {
            streaming = false;
            recording = false;
            filename = "";
        }

        State(const State& state)
        {
            streaming = state.streaming;
            recording = state.recording;
            filename = state.filename;
        }

        State& operator=(const State& other)
        {
            streaming = other.streaming;
            recording = other.recording;
            filename = other.filename;
            return *this;
        }

        bool streaming;
        bool recording;
        String filename;
    };

    SystemState::State& getState();

    // Singleton instance
    static SystemState& instance();

private:
    SystemState::State m_state;
    SystemState();
    ~SystemState() = default;
};


#endif  // _SYSTEM_STATE_H_
