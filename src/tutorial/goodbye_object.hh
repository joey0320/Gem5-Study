#ifndef __TUTORIAL_GEM5_GOODBYE_OBJECT__
#define __TUTORIAL_GEM5_GOODBYE_OBJECT__

#include "params/GoodbyeObject.hh"
#include "sim/sim_object.hh"
#include <string>

class GoodbyeObject : public SimObject {
    private:
        void processEvent();
        void fillBuffer();

        EventWrapper<GoodbyeObject, &GoodbyeObject::processEvent> event;

        float bandwidth;
        int bufferSize;
        char *buffer;
        int bufferUsed;
        std::string message;

    public:
        GoodbyeObject(GoodbyeObjectParams *p);
        ~GoodbyeObject();

        void sayGoodbye(std::string name);

};

#endif
