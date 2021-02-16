from m5.params import *
from m5.SimObject import SimObject

class HelloObject(SimObject):
    # convention to have same name with class
    # type is the C++ class that you are wrapping with this Python SimObject
    type='HelloObject'

    # file that contains the declaration of the class used as the 'type' parameter
    # convention is to use lowercase and underscore with the same name
    cxx_header='tutorial/hello_object.hh'


    # adding parameters
    # they will be passed to the C++ object
    # Param.<TypeName>(default_value, "description")
    # Many other convenience parameters (e.g. Percent, Cycles, MemorySize)
    time_to_wait = Param.Latency("Time before firing the event")
    number_of_fires = Param.Int(1, "Number of times to fire the event before goodbye")

    goodbye_object = Param.GoodbyeObject("A goodbye object")


class GoodbyeObject(SimObject):
    type='GoodbyeObject'
    cxx_header='tutorial/goodbye_object.hh'

    bandwidth = Param.MemoryBandwidth('100MB/s', "BW to fill the buffer")
    buffer_size = Param.MemorySize('1kB', "size of the buffer to fill")

