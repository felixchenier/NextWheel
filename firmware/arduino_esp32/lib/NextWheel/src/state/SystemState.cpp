#include "SystemState.h"

SystemState::SystemState()
{

}

// Singleton instance
SystemState& SystemState::instance()
{
    static SystemState state;
    return state;
}


SystemState::State& SystemState::getState()
{
    return m_state;
}