#include "tutorial/goodbye_object.hh"

#include "base/logging.hh"
#include "base/trace.hh"
#include "debug/Hello.hh"
#include "sim/sim_exit.hh"

#include <assert.h>

using namespace std;

GoodbyeObject::GoodbyeObject(GoodbyeObjectParams *params):
    SimObject(params),
    event(*this),
    bandwidth(params->bandwidth),
    bufferSize(params->buffer_size),
    buffer(NULL),
    bufferUsed(0) 
{
        buffer = new char[bufferSize];
        DPRINTF(Hello, "Created GoodbyeObject\n");
}

GoodbyeObject::~GoodbyeObject() {
    delete[] buffer;
}

void GoodbyeObject::processEvent() {
    DPRINTF(Hello, "Processing Event\n");
    fillBuffer();
}

void GoodbyeObject::sayGoodbye(std::string other_name) {
    DPRINTF(Hello, "Saying goodbye to %s\n", other_name);
    message = "Goodbye " + other_name;
    fillBuffer();
}

void GoodbyeObject::fillBuffer() {
    assert((int)message.length() > 0);

    int bytes_copied = 0;
    
    for (auto it = message.begin() ; 
            it != message.end() && 
            bufferUsed < bufferSize - 1 ; //char has null
            it++, bufferUsed++, bytes_copied++) {
        buffer[bufferUsed] = *it;
    }  

   if ( bufferUsed < bufferSize - 1 ) { // buffer left
       DPRINTF(Hello, "Scheduling another filBuffer in %d ticks\n", bytes_copied * bandwidth);
       schedule(event, curTick() + bytes_copied * bandwidth);
   } else { //buffer full
       DPRINTF(Hello, "Buffer is full!!!! bye bye\n");
       exitSimLoop(buffer, 0, curTick() + bandwidth * bytes_copied);
   }
}

GoodbyeObject* GoodbyeObjectParams::create() {
    return new GoodbyeObject(this);
}

