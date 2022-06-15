#ifndef _WEBSOCKET_SERVER_TASK_H_
#define _WEBSOCKET_SERVER_TASK_H_

#include "tasks/WorkerTask.h"
#include "WebSocketServer.h"

class WebSocketServerTask : public WorkerTask {

    static const size_t WEBSOCKET_SERVER_STACK_SIZE = 8000;

    public:
        WebSocketServerTask() : WorkerTask("WebSocketServerTask", WEBSOCKET_SERVER_STACK_SIZE) {

        }


        virtual void run(void *) override {

            m_server.begin();

            while (1) {
                DataFramePtr dataPtr = dequeue();
                if (dataPtr == nullptr) {
                    continue;
                }

                //dataPtr->print();

                // Will send to all connected websockets
                m_server.sendToAll(*dataPtr);

                // Mandatory, we need to cleanup the memory
                delete dataPtr;
            }
        }

    protected:

        WebSocketServer m_server;
};

#endif // _WEBSOCKET_SERVER_TASK_H_
