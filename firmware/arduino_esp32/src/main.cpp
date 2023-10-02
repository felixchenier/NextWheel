#include <Arduino.h>
#include <NextWheel.h>
#include "NextWheelApp.h"
#include <esp_adc_cal.h>
#include <driver/adc.h>
extern "C" {
    #include <esp_wifi.h>
}

void setup()
{
    esp_wifi_set_ps(WIFI_PS_NONE);

    // Serial must be initialized for prints to work
    Serial.begin(115200);

    // Global app object
    // Needs to be initialized after Arduino objects are created and ready.
    // We allocate the app in the setup function to make sure it is initialized.

    // Setup app
    NextWheelApp::instance()->begin();

    // Start tasks
    NextWheelApp::instance()->start();
}

void loop()
{
    // Note Arduino (loop) runs on core 1
    // WiFi, BLE runs on core 0
    // Default loop priority is TASK_PRIORITY_LOWEST (1)
    Serial.print("Main Loop: priority = ");
    Serial.println(uxTaskPriorityGet(NULL));

    Serial.print("Main Loop: Executing on core ");
    Serial.println(xPortGetCoreID());

    String currentIP = WiFi.localIP().toString();

    TickType_t lastGeneration = xTaskGetTickCount();
    while (1)
    {
        struct timeval timeval_now;
        gettimeofday(&timeval_now, NULL);

        // Verify that the IP has changed...
        // Signal IP with LEDS... Not optimal but for works for now.
        if (currentIP != WiFi.localIP().toString())
        {
            // Start of IP address
            NextWheelApp::instance()->getLEDS().setLED1(false);
            NextWheelApp::instance()->getLEDS().setLED2(false);
            vTaskDelayUntil(&lastGeneration, 1000 / portTICK_RATE_MS);
            NextWheelApp::instance()->getLEDS().setLED1(true);
            NextWheelApp::instance()->getLEDS().setLED2(true);
            vTaskDelayUntil(&lastGeneration, 1000 / portTICK_RATE_MS);
            NextWheelApp::instance()->getLEDS().setLED1(false);
            NextWheelApp::instance()->getLEDS().setLED2(false);

            // Store new IP
            currentIP = WiFi.localIP().toString();

            Serial.print("IP address changed: ");
            Serial.println(currentIP);

            for (auto i = 0; i < currentIP.length(); i++)
            {   // '.' separates the IP address

                // Signal changing Digit
                NextWheelApp::instance()->getLEDS().setLED1(true);
                vTaskDelayUntil(&lastGeneration, 500 / portTICK_RATE_MS);
                NextWheelApp::instance()->getLEDS().setLED1(false);
                vTaskDelayUntil(&lastGeneration, 500 / portTICK_RATE_MS);

                if (currentIP[i] != '.')
                {
                    auto val = String(currentIP[i]).toInt();
                    Serial.print("Signaling: "); Serial.println(val);
                    for (auto j = 0; j < val; j++)
                    {
                        //Signal count with LED2
                        NextWheelApp::instance()->getLEDS().setLED2(true);
                        vTaskDelayUntil(&lastGeneration, 250 / portTICK_RATE_MS);
                        NextWheelApp::instance()->getLEDS().setLED2(false);
                        vTaskDelayUntil(&lastGeneration, 250 / portTICK_RATE_MS);
                    }
                }
                else
                {
                    // Signal changing Digit
                    NextWheelApp::instance()->getLEDS().setLED1(true);
                    vTaskDelayUntil(&lastGeneration, 2000 / portTICK_RATE_MS);
                    NextWheelApp::instance()->getLEDS().setLED1(false);
                    vTaskDelayUntil(&lastGeneration, 2000 / portTICK_RATE_MS);
                }

                // Pause for each digit
                //vTaskDelayUntil(&lastGeneration, 1000 / portTICK_RATE_MS);
            }

            // End of IP address
            NextWheelApp::instance()->getLEDS().setLED1(false);
            NextWheelApp::instance()->getLEDS().setLED2(false);
            vTaskDelayUntil(&lastGeneration, 1000 / portTICK_RATE_MS);
            NextWheelApp::instance()->getLEDS().setLED1(true);
            NextWheelApp::instance()->getLEDS().setLED2(true);
            vTaskDelayUntil(&lastGeneration, 1000 / portTICK_RATE_MS);
            NextWheelApp::instance()->getLEDS().setLED1(false);
            NextWheelApp::instance()->getLEDS().setLED2(false);
        }
        else
        {
            // Normal LED handling
            if (NextWheelApp::instance()->isRecording())
            {
                NextWheelApp::instance()->getLEDS().toggleLED1();
            }
            else
            {
                NextWheelApp::instance()->getLEDS().setLED1(false);
            }

            // Blinking led2 for now...
            NextWheelApp::instance()->getLEDS().toggleLED2();

            // IDLE loop.
            // 250 ms task
            vTaskDelayUntil(&lastGeneration, 250 / portTICK_RATE_MS);

            if(NextWheelApp::instance()->button1Pressed())
            {
                Serial.println("Button 1 pressed");
                NextWheelApp::instance()->startRecording();
            }

            if(NextWheelApp::instance()->button2Pressed())
            {
                Serial.println("Button 2 pressed");
                NextWheelApp::instance()->stopRecording();
            }
        }
       Serial.print("Free heap size: "); Serial.println(ESP.getFreeHeap());
    }
}
