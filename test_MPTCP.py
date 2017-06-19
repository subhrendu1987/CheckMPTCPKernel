#!/usr/bin/python
"""
CHECK IF THIS KERNEL SUPPORTS MPTCP OR NOT
Sample output
	Final Bandwidth= [  3]  0.0-100.2 sec   224 MBytes  18.8 Mbits/sec
	Path stats{'Path':[BW,DELAY,LOSS_RATE]}= {'h2-s2-s1-h1': [10, 17.0, 0], 'h2-s3-s4-h1': [10, 17.0, 0]}

Here bandwidth test result gives "18.8 Mbits/sec" which complies with sum of path bandwidth i.e (10+10=20Mbps)
"""

import os, sys, argparse, random, re, netifaces
from subprocess import Popen, PIPE, call
from time import sleep
import termcolor as T
from itertools import chain
import json

from mininet.net import Mininet
from mininet.log import lg
from mininet.node import UserSwitch as Switch
from mininet.link import Link, TCLink, Intf
from mininet.util import makeNumeric, custom
from mininet.cli import CLI
from functools import partial
from mininet.node import Controller, RemoteController,OVSController
from mininet.topo import Topo

import Switch4_part3 as sw_net
import framework
#############################################################################
def main():
    framework.preconfigure()
    args = framework.parse_args()
    lg.setLogLevel('info')
    net = sw_net.myNetwork()
    A=framework.mininet_to_networkx(net)
    node_graph=A[0]
    ###########################################
    print "-----Start PING test"
    hIpDict=framework.getAllIP(net)
    lg.info("Before configuring routing table\n")
    framework.pingAllIP(hIpDict,1)
    ###########################################
    if(len(net.controllers)>1):
	framework.run_configure(args,net)
    else:
        framework.run_configure_single_nw(args,net)
    ###########################################
    hIpDict=framework.getAllIP(net)
    lg.info("After configuring routing table\n")
    framework.pingAllIP(hIpDict,3)
    ###########################################
    pathA=None
    pathA=False
    os.system("/etc/init.d/networking restart")
    path='10.0.0.1'
    src="h2"
    dest="h1"
    path_stat=framework.get_path_stats(node_graph,src,dest)
    ###########################################
    net.getNodeByName(dest).cmdPrint("iperf -s&")#h1
    test_result=net.getNodeByName(src).cmdPrint("sleep 5; iperf -c %s -i 2 -t 30 -m"%(path))#h2
    test_result=test_result.split("\n")
    Final=test_result[len(test_result)-3]
    T.cprint("------------------------------------------------------------","green", attrs=['bold'])
    T.cprint("SEE FILE HEADER FOR EXPLAINATION ON THE OUTPUT\n\n\n","red", attrs=['bold'])
    T.cprint("Final Bandwidth= %s"%(Final),"green")
    T.cprint("Path stats{\'Path\':[BW,DELAY,LOSS_RATE]}="+str(path_stat),"green")
    print "\n\n"
    net.stop()
    framework.end(args)
#############################################################################
if __name__ == '__main__':
    main()
#############################################################################
