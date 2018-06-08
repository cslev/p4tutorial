#!/usr/bin/env python2
import argparse
import os
from time import sleep

import p4runtime_lib.bmv2
import p4runtime_lib.helper

def writeArpRules(p4info_helper, sw, arp_request_ip, arp_reply_mac):
    '''
    Install ARP responding rules:
    :param p4info_helper: the P4Info helper
    :param sw: the first hop switch to install the rules
    :param arp_request_ip: the IP address the host will look the MAC address for
    :param arp_reply_mac: the MAC address of the arp_request_ip holder
    '''
    table_entry = p4info_helper.buildTableEntry(
            table_name="MyIngress.arp_exact",
            match_fields={
                "hdr.arp.dst_ip":arp_request_ip
            },
            action_name="MyIngress.arp_reply",
            action_params={
                "request_mac":arp_reply_mac,
            })
    sw.WriteTableEntry(table_entry)
    print "Install ARP rule into switch %s" % sw.name

def writeForwardingRules(p4info_helper, sw, dst_eth_addr, outport):
    '''
    Installs basic IPv4 address based flow rules

    :param p4info_helper: the P4Info helper
    :param sw: the switch to install the flow rules
    :param dst_eth_addr: the destination Ethernet address 
    :param outport: the output port the packets need to be sent to
    '''    
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.l2forward_exact",
        match_fields={
            "hdr.ethernet.dstAddr": dst_eth_addr
        },
        action_name="MyIngress.l2_forward",
        action_params={
            "port": outport
        })
    sw.WriteTableEntry(table_entry)
    print "Installed forwarding rule on %s" % sw.name

  

def readTableRules(p4info_helper, sw):
    '''
    Reads the table entries from all tables on the switch.

    :param p4info_helper: the P4Info helper
    :param sw: the switch connection
    '''
    print '\n----- Reading tables rules for %s -----' % sw.name
    for response in sw.ReadTableEntries():
        for entity in response.entities:
            entry = entity.table_entry
            # TODO For extra credit, you can use the p4info_helper to translate
            #      the IDs the entry to names
            print entry
            print '-----'

def printCounter(p4info_helper, sw, counter_name, index):
    '''
    Reads the specified counter at the specified index from the switch. In our
    program, the index is the tunnel ID. If the index is 0, it will return all
    values from the counter.

    :param p4info_helper: the P4Info helper
    :param sw:  the switch connection
    :param counter_name: the name of the counter from the P4 program
    :param index: the counter index (in our case, the tunnel ID)
    '''
    for response in sw.ReadCounters(p4info_helper.get_counters_id(counter_name), index):
        for entity in response.entities:
            counter = entity.counter_entry
            print "%s %s %d: %d packets (%d bytes)" % (
                sw.name, counter_name, index,
                counter.data.packet_count, counter.data.byte_count
            )


def main(p4info_file_path, bmv2_file_path):
    # Instantiate a P4 Runtime helper from the p4info file
    p4info_helper = p4runtime_lib.helper.P4InfoHelper(p4info_file_path)

    # Hardwired topology info for the controller
    hosts_mac = {'10.0.0.1':'00:00:00:00:00:01',
                 '10.0.0.2':'00:00:00:00:00:02',
                 '10.0.0.3':'00:00:00:00:00:03'
                }
    switch_port = {
                    's1': {'00:00:00:00:00:01':1,
                           '00:00:00:00:00:02':2,
                           '00:00:00:00:00:03':3},
                    's2': {'00:00:00:00:00:01':2,
                           '00:00:00:00:00:02':1,
                           '00:00:00:00:00:03':3},
                    's3': {'00:00:00:00:00:01':2,
                           '00:00:00:00:00:02':3,
                           '00:00:00:00:00:03':1}
                    }

    # create connection to each switch
    for i in range(1,4):
        s = p4runtime_lib.bmv2.Bmv2SwitchConnection('s'+str(i),
                                                 address='127.0.0.1:5005'+str(i), 
                                                 device_id=(i-1))
        # Install the P4 program on the switches
        s.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                      bmv2_json_file_path=bmv2_file_path)
        print "Installed P4 Program using SetForwardingPipelineConfig on %s" % s.name
        # Write the ARP rules into the switches
        for ip in hosts_mac:
            writeArpRules(p4info_helper, sw=s,arp_request_ip=ip, arp_reply_mac=hosts_mac[ip])


        # install forwarding rules
        port_series = switch_port[s.name]
        for mac in port_series:
            writeForwardingRules(p4info_helper,sw=s,dst_eth_addr=mac,outport=port_series[mac])
        readTableRules(p4info_helper,s)
   



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='P4Runtime Controller')
    parser.add_argument('--p4info', help='p4info proto in text format from p4c',
                        type=str, action="store", required=False,
                        default='./build/l2_switch.p4info')
    parser.add_argument('--bmv2-json', help='BMv2 JSON file from p4c',
                        type=str, action="store", required=False,
                        default='./build/l2_switch.json')
    args = parser.parse_args()

    if not os.path.exists(args.p4info):
        parser.print_help()
        print "\np4info file not found: %s\nHave you run 'make'?" % args.p4info
        parser.exit(1)
    if not os.path.exists(args.bmv2_json):
        parser.print_help()
        print "\nBMv2 JSON file not found: %s\nHave you run 'make'?" % args.bmv2_json
        parser.exit(1)

    main(args.p4info, args.bmv2_json)
