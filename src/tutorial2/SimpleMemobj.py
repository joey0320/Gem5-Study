import m5
from m5.params import *
from m5.proxy import *
from m5.SimObject import *

class SimpleMemobj(SimObject):
    type='SimpleMemobj'
    cxx_header='tutorial2/simple_memobj.hh'

    inst_port = SlavePort("CPU side port for instructions")
    data_port = SlavePort("CPU side port for data")
    mem_side = MasterPort("Mem side port")
