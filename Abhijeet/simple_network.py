#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False)

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host)
    h2 = net.addHost('h2', cls=Host)

    info( '*** Add links\n')
    linkProp = {'bw':10,'delay':'100ms'}
    net.addLink(h1, s1, cls=TCLink, **linkProp)
    net.addLink(h1, s2, cls=TCLink, **linkProp)
    net.addLink(h2, s1, cls=TCLink, **linkProp)
    net.addLink(h2, s2, cls=TCLink, **linkProp)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([])
    net.get('s2').start([])

    info( '*** Post configure switches and hosts\n')
    
    h1.cmd("ifconfig h1-eth0 10.0.1.1 netmask 255.255.255.0")
    h1.cmd("ifconfig h1-eth1 192.168.2.1 netmask 255.255.255.0")
    h2.cmd("ifconfig h2-eth0 10.0.1.2 netmask 255.255.255.0")
    h2.cmd("ifconfig h2-eth1 192.168.2.2 netmask 255.255.255.0")

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

