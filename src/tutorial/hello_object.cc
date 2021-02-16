#include "tutorial/hello_object.hh"

#include "base/logging.hh"
#include "base/trace.hh"
#include "debug/Hello.hh"


using namespace std;

// constructor : pass the parameter object to SimObject
HelloObject::HelloObject(HelloObjectParams *params):
    SimObject(params),
    event([this]{processEvent();}, name()),
    goodbye(params->goodbye_object),
    // each params instantiation has a name
    // which comes from the python config file
    myName(params->name), 
    latency(params->time_to_wait),
    timesLeft(params->number_of_fires)
{
    DPRINTF(Hello, "[info] : created the Hello object\n");
    panic_if(!goodbye, "HelloObject must have a non-null GoodbyeObject\n");
}

void HelloObject::processEvent() {
    if (--timesLeft > 0) {
        DPRINTF(Hello, "[info] : processing Event : %d times left\n", timesLeft);
        schedule(event, curTick() + latency);
    } else {
        goodbye->sayGoodbye(myName);
        DPRINTF(Hello, "[info] : Done processing!!\n");
    }
}

void HelloObject::startup() {
    schedule(event, latency);
}



// implement for the parameter type
// implicitly created from the SimObject Python declaration, namely, the create function
// returns a new instantiation of the SimObject
HelloObject* HelloObjectParams::create() {
    return new HelloObject(this);
}

