from mininet.topo import Topo
from mininet.util import irange
from mininet.net import Containernet
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel
import os
setLogLevel('info')





"Datacenter topology with 4 hosts per rack, 4 racks, and a root switch"
controllerIP = repr(os.environ.get('CONTROLLER_IP'))
self = Containernet(controller=RemoteController)
info('*** Adding controller at '+ controllerIP + '\n')
self.addController('c0', controller=RemoteController, ip=controllerIP, port=6653)


self.racks = []
rootSwitch = self.addSwitch('s1')
for i in irange(1, 2):
    rack = self.buildRack(i)
    self.racks.append(rack)
    for switch in rack:
        self.addLink(rootSwitch, switch)


"Build a rack of hosts with a top-of-rack switch"

dpid = (loc * 16) + 1
switch = self.addSwitch('s1r%s' % loc, dpid='%x' % dpid)

for n in irange(1, 5):
    #host = self.addHost( 'h%sr%s' % ( n, loc ) )
    #host = self.addHost('h%sr%s' % (n, loc), dimage="ubuntu:trusty")
    host = self.addDocker('h%sr%s', dimage="acksec/dc26", environment={"CONTROLLER_IP": controllerIP}, working_dir="/root")
    self.addLink(switch, host)

# Return list of top-of-rack switches for this rack
info('*** Starting network\n')
net.start()
info('*** Running CLI\n')
CLI(net)
info('*** Stopping network')
net.stop()


# Allows the file to be imported using `mn --custom <filename> --topo dcbasic`
