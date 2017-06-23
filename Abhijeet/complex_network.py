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
import sys
from mininet.term import runX11, makeTerm
import time



def myNetwork():

    net = Mininet( topo=None,
                   build=False)

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    S1 = net.addSwitch('S1', cls=OVSKernelSwitch, failMode='standalone')
    S2 = net.addSwitch('S2', cls=OVSKernelSwitch, failMode='standalone')
    S3 = net.addSwitch('S3', cls=OVSKernelSwitch, failMode='standalone')
    S4 = net.addSwitch('S4', cls=OVSKernelSwitch, failMode='standalone')
    S5 = net.addSwitch('S5', cls=OVSKernelSwitch, failMode='standalone')
    S6 = net.addSwitch('S6', cls=OVSKernelSwitch, failMode='standalone')

    R1 = net.addHost('R1', cls=Node, ip='0.0.0.0')
    R2 = net.addHost('R2', cls=Node, ip='0.0.0.0')
    R3 = net.addHost('R3', cls=Node, ip='0.0.0.0')
    R4 = net.addHost('R4', cls=Node, ip='0.0.0.0')
    R5 = net.addHost('R5', cls=Node, ip='0.0.0.0')

    info( '*** Add hosts\n')
    T1 = net.addHost('T1', cls=Host)
    T2 = net.addHost('T2', cls=Host)

    info( '*** Add links\n')
    delay = 5
    T1S1 = {'bw':1,'delay':str(delay)+'ms','max_queue_size':10000}
    links = [
            [S1, T1],
            [S2, T1],
            [S2, R2],
            [S4, R2],
            [S4, R5],
            [S4, R4],
            [S6, R4],
            [S5, T2],
            [S6, T2],
            [S1, R1],
            [S3, R1],
            [S3, R3],
            [S5, R3],
            [S3, R5]
        ]
    
    for s, t in links:
        #print "\n",s, t,
        net.addLink(s, t, cls=TCLink, **T1S1)



    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('S1').start([])
    net.get('S2').start([])
    net.get('S3').start([])
    net.get('S4').start([])
    net.get('S5').start([])
    net.get('S6').start([])

    info( '*** Post configure switches and hosts\n')
    R1.cmd('sysctl -w net.ipv4.ip_forward=1')
    R2.cmd('sysctl -w net.ipv4.ip_forward=1')
    R3.cmd('sysctl -w net.ipv4.ip_forward=1')
    R4.cmd('sysctl -w net.ipv4.ip_forward=1')
    R5.cmd('sysctl -w net.ipv4.ip_forward=1')
    ips=[
        [T1, "T1-eth0", "10.0.1.2", "10.0.1.1"],
        [T1, "T1-eth1", "10.0.2.2", "10.0.2.1"],

        [R1, "R1-eth0", "10.0.1.1"],
        [R1, "R1-eth1", "10.0.3.1"],

        [R2, "R2-eth0", "10.0.2.1"],
        [R2, "R2-eth1", "10.0.4.1"],

        [R3, "R3-eth0", "10.0.3.2"],
        [R3, "R3-eth1", "10.0.5.1"],

        [R4, "R4-eth0", "10.0.4.2"],
        [R4, "R4-eth1", "10.0.6.1"],

        [R5, "R5-eth0", "10.0.4.3"],
        [R5, "R5-eth1", "10.0.3.3"],

        [T2, "T2-eth0", "10.0.5.2", "10.0.5.1"],
        [T2, "T2-eth1", "10.0.6.2", "10.0.6.1"]
        ]

    for x in ips:
        cmd = "ifconfig "+x[1]+" "+x[2] + " netmask 255.255.255.0"
        # print cmd
        x[0].cmd(cmd)
        if len(x) < 4:
            continue
        cmd = "route add default gw "+x[3]+" dev "+ x[1]
        # print cmd
        x[0].cmd(cmd)

    
    routersRouting= [
        [R1, "10.0.2.0/24", "R1-eth1", "10.0.3.3"],
        [R1, "10.0.4.0/24", "R1-eth1", "10.0.3.3"],
        [R1, "10.0.6.0/24", "R1-eth1", "10.0.3.3"],
        [R1, "10.0.5.0/24", "R1-eth1", "10.0.3.2"],
        #[R1, "10.0.5.0/24", "R1-eth1", "10.0.3.2"],
        
        [R2, "10.0.3.0/24", "R2-eth1", "10.0.4.3"],
        [R2, "10.0.1.0/24", "R2-eth1", "10.0.4.3"],
        [R2, "10.0.5.0/24", "R2-eth1", "10.0.4.3"],
        [R2, "10.0.6.0/24", "R2-eth1", "10.0.4.2"],
        
        [R4, "10.0.2.0/24", "R4-eth0", "10.0.4.1"],
        [R4, "10.0.1.0/24", "R4-eth0", "10.0.4.3"],
        [R4, "10.0.3.0/24", "R4-eth0", "10.0.4.3"],
        [R4, "10.0.5.0/24", "R4-eth0", "10.0.4.3"],
        
        [R3, "10.0.1.0/24", "R3-eth0", "10.0.3.1"],
        [R3, "10.0.2.0/24", "R3-eth0", "10.0.3.3"],
        [R3, "10.0.4.0/24", "R3-eth0", "10.0.3.3"],
        [R3, "10.0.6.0/24", "R3-eth0", "10.0.3.3"],
        
        [R5, "10.0.6.0/24", "R5-eth0", "10.0.4.2"],
        [R5, "10.0.2.0/24", "R5-eth0", "10.0.4.1"],
        [R5, "10.0.5.0/24", "R5-eth1", "10.0.3.2"],
        [R5, "10.0.1.0/24", "R5-eth1", "10.0.3.1"],
        ]

    for x in routersRouting:
        cmd = 'route add -net ' + x[1] + ' gw ' + x[3] + ' dev ' + x[2]
        # print cmd
        x[0].cmd(cmd)


    T1.cmd("ip rule add from 10.0.1.2 table 1")
    T1.cmd("ip rule add from 10.0.2.2 table 2")

    T1.cmd("ip route add 10.0.1.0/24 dev T1-eth0 scope link table 1")
    T1.cmd("ip route add default via 10.0.1.1 dev T1-eth0 table 1")

    T1.cmd("ip route add 10.0.2.0/24 dev T1-eth1 scope link table 2")
    T1.cmd("ip route add default via 10.0.2.1 dev T1-eth1 table 2")

    T2.cmd("ip rule add from 10.0.5.2 table 1")
    T2.cmd("ip rule add from 10.0.6.2 table 2")

    T2.cmd("ip route add 10.0.5.0/24 dev T2-eth0 scope link table 1")
    T2.cmd("ip route add default via 10.0.5.1 dev T2-eth0 table 1")

    T2.cmd("ip route add 10.0.6.0/24 dev T2-eth1 scope link table 2")
    T2.cmd("ip route add default via 10.0.6.1 dev T2-eth1 table 2")

    T2.cmd("ping -c2 10.0.1.2")
    T2.cmd("ping -c2 10.0.2.2")
    T1.cmd("ping -c2 10.0.5.2")
    T1.cmd("ping -c2 10.0.6.2")
    
    cli_cmd = "iperf -c 10.0.5.2"
    srv_cmd = "iperf -s"
    tcpdump_cmd = "tcpdump -i any -nv port 5001 -s0"
    srvNode = T2
    cliNode = T1
    termTc, popenTc = runX11(cliNode, "xterm -e "+tcpdump_cmd)
    time.sleep(2)
    termSr, popenSr = runX11(srvNode, "xterm -e "+srv_cmd)
    time.sleep(1)
    termCl, popenCl = runX11(cliNode, "xterm -e "+cli_cmd)
    # popenSr.
    popenCl.wait()
    time.sleep(1)
    popenSr.terminate()
    time.sleep(4)
    popenTc.terminate()
    # CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

