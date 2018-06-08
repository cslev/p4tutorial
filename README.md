# p4tutorial
This repository contains some additional tutorials for the main [p4lang/tutorials](https://github.com/p4lang/tutorials) repo derived from my P4-related plays.

## Introduction
This repository contains **two** almost-ready P4 codes (solutions are in the corresponding solution/ directory):
 1) **l2_switch**: a simple L2 switch, i.e., packets are forwared according to their DESTINATION MAC ADDRESS. The application also implements a pure dataplane ARP responder for handling the ARP REQUESTS sent initially by any of the hosts.
In particular, **each switch** is aware of each host's MAC address, and once a switch encounters an ARP REQUEST sent from a host, it immediately replies to it in a well-formed ARP_RESPONSE packet. Once the switches know the MAC addresses of the corresponding IP address, they can ping each other.
 2) **l2_switch_p4runtime**: the same as **l2_switch**, but the control plane is implemented in P4Runtime instead of the text-file based configuration

## Notes
In the [p4lang/tutorials](https://github.com/p4lang/tutorials), the hosts are not in the same L2 domain, so some of the topology files and Makefiles had to be tediously adapted to this use case.
It affects a modified **run_exercise.py** for the hosts' configuration (e.g., IP address setup, delete default gateway from the routing table, disable manually hardwired ARP entries).
Note, however that these do not have any effect to the original repository, as the related files are included into this repositories and will only be used if these solutions are being tested.

## Walkthrough
Obtaining the P4 environment (easiest way is to download the VirtualBox image) is the reader's responsibilty. There is a bunch of howtos on this, please browse the [main P4 site's events page](https://p4.org/events/), for instance, instructions for downloading the VM can be found on the site of [East Coast P4 Developer Day, Spring 2018](https://p4.org/events/2018-03-09-p4-developer-day/).

After booting up the VM, get into the directory of one of the tutorials:...
