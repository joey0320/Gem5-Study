#ifndef __TUTORIAL_GEM5_HELLO_OBJECT__
#define __TUTORIAL_GEM5_HELLO_OBJECT__

#include "params/HelloObject.hh"
#include "sim/sim_object.hh"
#include "tutorial/goodbye_object.hh"
#include <string>

class HelloObject : public SimObject {
    private:
        void processEvent();

        EventFunctionWrapper event;
    
        GoodbyeObject *goodbye;

        const std::string myName;
        const Tick latency;
        int timesLeft;


    public:
        // constructor of a SimObject takes a parameter object
        // which is autmatically created by the build system
        HelloObject(HelloObjectParams *p);

        void startup();
};

#endif
