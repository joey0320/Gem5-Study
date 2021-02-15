import m5
from m5.objects import *
from caches import *
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument("--l1d_size", help="L1 data cache size")
    parser.add_argument("--l1i_size", help="L1 instruction cache size")
    parser.add_argument("--l2_size", help="L2 cache size")

    args = parser.parse_args()
    return args


if __name__ == "__m5_main__":
    # the system object will be the parent of all other objects
    # in the simulated system
    # it contains alot of functional information (e.g. physical memory ranges, root clock domain, kernel ...)
    args = get_arguments()

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

    # create caches
    system.cpu.icache = L1ICache(args.l1d_size)
    print(system.cpu.icache.size)
    system.cpu.dcache = L1DCache(args.l1i_size)

    # connect caches to cpu ports
    system.cpu.icache.connectCPU(system.cpu)
    system.cpu.dcache.connectCPU(system.cpu)

    # we need to create a L2 bus since the L2 cache only has a single port
    system.l2bus = L2XBar()

    # connect L1 cache to L2 bus
    system.cpu.icache.connectBus(system.l2bus)
    system.cpu.dcache.connectBus(system.l2bus)

    # create L2 caceh
    system.l2cache = L2Cache(args.l2_size)

    # set systemwide memory bus
    system.membus = SystemXBar()

    # connect L2 cache
    system.l2cache.connectCPUSideBus(system.l2bus)
    system.l2cache.connectMemSideBus(system.membus)

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


