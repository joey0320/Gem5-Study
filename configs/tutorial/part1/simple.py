import m5
from m5.objects import *


# the system object will be the parent of all other objects
# in the simulated system
# it contains alot of functional information (e.g. physical memory ranges, root clock domain, kernel ...)
system = System()

# set clock domain
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# set memory : memory is usually timing mode
system.mem_mode = 'timing'
system.mem_ranges = [AddrRange('512MB')]

# set cpu
system.cpu = TimingSimpleCPU()

# set systemwide memory bus
system.membus = SystemXBar()

# no cache system
# directly connect caches to the membus
# memobject1.master = memobject1.slave
# master sends requeset
# slave sends the responses
system.cpu.icache_port = system.membus.slave
system.cpu.dcache_port = system.membus.slave

# only required for X86
# create IO controller on the cpu
# and connect it to the mem bus
system.cpu.createInterruptController()
system.cpu.interrupts[0].pio = system.membus.master
system.cpu.interrupts[0].int_master = system.membus.slave
system.cpu.interrupts[0].int_slave = system.membus.master

system.system_port = system.membus.slave

# create a memory controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.master

# in the syscall emulation mode, we just need to pass the application binary
# then give this process to the cpu workload
# and finally create the functional exectuion contexts in the CPU
process = Process()
process.cmd = ['tests/test-progs/hello/bin/x86/linux/hello']
system.cpu.workload = process
system.cpu.createThreads()

# finally we instantiate the system and run the simulation
root = Root(full_system=False, system=system)

m5.instantiate()

print("Beginning simulation")
exit_event = m5.simulate()
print("Exiting @ tick {} because {}".format(m5.curTick(), exit_event.getCause()))


