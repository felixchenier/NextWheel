/*
 * Task.cpp
 *
 *  Created on: Mar 4, 2017
 *      Author: kolban
 */


#include <esp_log.h>
#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <string>

#include "Task.h"
#include "sdkconfig.h"

static const char* LOG_TAG = "Task";


/**
 * @brief Create an instance of the task class.
 *
 * @param [in] taskName The name of the task to create.
 * @param [in] stackSize The size of the stack.
 * @return N/A.
 */
Task::Task(std::string taskName, uint16_t stackSize, uint8_t priority)
{
    m_taskName = taskName;
    m_stackSize = stackSize;
    m_priority = priority;
    m_taskData = nullptr;
    m_handle = nullptr;
    m_coreId = tskNO_AFFINITY;

    // Create command queue
    m_baseCommandQueue = xQueueCreate(10, sizeof(BaseTaskCommand));
}  // Task

Task::~Task() {}  // ~Task

/**
 * @brief Suspend the task for the specified milliseconds.
 *
 * @param [in] ms The delay time in milliseconds.
 * @return N/A.
 */

/* static */ void Task::delay(int ms)
{
    ::vTaskDelay(ms / portTICK_PERIOD_MS);
}  // delay

/**
 * Static class member that actually runs the target task.
 *
 * The code here will run on the task thread.
 * @param [in] pTaskInstance The task to run.
 */
void Task::runTask(void* pTaskInstance)
{
    Task* pTask = (Task*)pTaskInstance;
    ESP_LOGD(LOG_TAG, ">> runTask: taskName=%s", pTask->m_taskName.c_str());
    pTask->run(pTask->m_taskData);
    ESP_LOGD(LOG_TAG, "<< runTask: taskName=%s", pTask->m_taskName.c_str());
    pTask->stop();
}  // runTask

/**
 * @brief Start an instance of the task.
 *
 * @param [in] taskData Data to be passed into the task.
 * @return N/A.
 */
void Task::start(void* taskData)
{
    if (m_handle != nullptr)
    {
        ESP_LOGW(LOG_TAG, "Task::start - There might be a task already running!");
    }
    m_taskData = taskData;
    // Specify the core to run on
    ::xTaskCreatePinnedToCore(&runTask, m_taskName.c_str(), m_stackSize, this, m_priority, &m_handle, m_coreId);

    // Let the OS decide which core to run the task on
    //::xTaskCreate(&runTask, m_taskName.c_str(), m_stackSize, this, m_priority, &m_handle);
}  // start


/**
 * @brief Stop the task.
 *
 * @return N/A.
 */
void Task::stop()
{
    if (m_handle == nullptr)
        return;
    xTaskHandle temp = m_handle;
    m_handle = nullptr;
    ::vTaskDelete(temp);
}  // stop

/**
 * @brief Set the stack size of the task.
 *
 * @param [in] stackSize The size of the stack for the task.
 * @return N/A.
 */
void Task::setStackSize(uint16_t stackSize)
{
    m_stackSize = stackSize;
}  // setStackSize

/**
 * @brief Set the priority of the task.
 *
 * @param [in] priority The priority for the task.
 * @return N/A.
 */
void Task::setPriority(uint8_t priority)
{
    m_priority = priority;
}  // setPriority

/**
 * @brief Set the name of the task.
 *
 * @param [in] name The name for the task.
 * @return N/A.
 */
void Task::setName(std::string name)
{
    m_taskName = name;
}  // setName

/**
 * @brief Set the core number the task has to be executed on.
 * If the core number is not set, tskNO_AFFINITY will be used
 *
 * @param [in] coreId The id of the core.
 * @return N/A.
 */
void Task::setCore(BaseType_t coreId)
{
    m_coreId = coreId;
}

bool Task::sendBaseCommandEvent(BaseTaskCommand command, bool from_isr)
{
    if (from_isr)
    {
        return xQueueSendFromISR(m_baseCommandQueue, &command, nullptr) == pdTRUE;
    }
    else
    {
        return xQueueSend(m_baseCommandQueue, &command, 0) == pdTRUE;
    }
}

Task::BaseTaskCommand Task::dequeueBaseCommand(unsigned long timeout)
{
    BaseTaskCommand command = BASE_TASK_COMMAND_NONE;
    if (xQueueReceive(m_baseCommandQueue, &command, timeout) != pdTRUE)
    {
        return BASE_TASK_COMMAND_NONE;
    }
    return command;
}
