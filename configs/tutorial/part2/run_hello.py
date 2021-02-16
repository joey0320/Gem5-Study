import m5
from m5.objects import *

root = Root(full_system=False)

# time_to_wait does not have a default value
# needs to be specified
root.hello = HelloObject(time_to_wait='2us')

# or we can just specify the time_to_wait as a member variable
# root.hello.time_to_wait = '2us'

root.hello.number_of_fires = 10
root.hello.goodbye_object = GoodbyeObject(buffer_size='30B')

m5.instantiate()

print("Beginning simulation")
exit_event = m5.simulate()
print("Exiting @ tick {} because {}".format(m5.curTick(), exit_event.getCause()))
