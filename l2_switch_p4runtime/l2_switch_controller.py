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

    '''
    TODO: similarly to writeArpRules(), create a table_entry for the l2forward_exact
          and fill out the corresponding fields set as params            
    '''
  

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
    # These are the MAC addresses of the hosts to provide the ARP responder feature
    hosts_mac = {'10.0.0.1':'00:00:00:00:00:01',
                 '10.0.0.2':'00:00:00:00:00:02',
                 '10.0.0.3':'00:00:00:00:00:03'
                }
    # Forwarding rules for the switches, i.e., which dst_mac can be reached via which port
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
    '''
    TODO: 
    - Connect to each switch
    hint: p4runtime_lib.bmv2.Bmv2SwitchConnection('s1',
                                                 address='127.0.0.1:50051', 
                                                 device_id=0)
    - install P4 program
    hint: switch_conn.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                      bmv2_json_file_path=bmv2_file_path)
    
    - write ARP rules according to hosts_mac dict()
    - write L2 forwarding rules according to switch_port dict(dict())
    [- use readTablesRules() to print out the table rules for debugging]
    '''
    # create connection to each switch
    for i in range(1,4):
        # TODO connect to switches

        # TODO Install the P4 program on the switches
        
        # TODO Write the ARP rules into the switches


        # TODO install forwarding rules
        
        # [TODO read flow tables]



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
