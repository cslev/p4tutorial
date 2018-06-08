# Implementing Layer-2 Forwarding

## Introduction

The objective of this exercise is to write a P4 program that
implements basic Layer-2 forwarding accorirding to the destination MAC address found in the header.
For simplicity, the P4 program is also aware of the hosts MAC addresses, so once a host is sending an ARP request, the first hop switch can craft the corresponding ARP reply message implementing and ARP responder purely in the dataplane

With Layer-2 forwarding, the switch must perform the following actions
for every packet: 
 1) Check etherType to filter ARP messages
 2) If packet is and ARP REQUEST, by means of the data stored in the flow table, the switch must tinker the ARP RESPONSE packet
 3) When normal L2/L3 packets are sent from any of the hosts (e.g., ping, iperf), the forwarding should be done by the destination MAC addresses.

 
Your switch will have two single tables: the first one is for the ARP-related data, while the second is for the particular forwarding.
The control plane will populate each table with static rules. 
Each rule in the ARP-related table will map an IP address to the corresponding MAC address,
while each rule in the forwarding table will map each destination MAC address to the port towards the particular destination.

> **Spoiler alert:** There is a reference solution in the `solution`
> sub-directory. Feel free to compare your implementation to the
> reference.

## Step 1: Run the (incomplete) starter code

The directory with this README also contains a skeleton P4 program,
`l2_switch.p4`, which initially drops all packets. Your job will be to
extend this skeleton program to properly implement the Layer-2 forwarding use case.

Before that, let's compile the incomplete `l2_switch.p4` and bring
up a switch in Mininet to test its behavior.

1. In your shell, run:
   ```bash
   make run
   ```
   This will:
   * compile `l2_switch.p4`, and
   * start a Mininet instance with three switches (`s1`, `s2`, `s3`)
     configured in a triangle, each connected to one host (`h1`, `h2`,
     and `h3`).
   * The hosts are assigned IPs of `10.0.0.1/24`, `10.0.0.2/24`, and `10.0.0.3/24`.

2. You should now see a Mininet command prompt. Open two terminals
for `h1` and `h2`, respectively:
   ```bash
   mininet> xterm h1 h2
   ```
3. At each host, one can check that none of them knows the others' MAC address
   ```bash
   arp -n
   ```
4. In `h1`'s xterm, ping `h2`:
   ```bash
   ping 10.0.0.2
   ```
   The message will not be received.
5. Type `exit` to leave each xterm and the Mininet command line.
   Then, to stop mininet:
   ```bash
   make stop
   ```
   And to delete all pcaps, build files, and logs:
   ```bash
   make clean
   ```

The message was not received because each switch is programmed
according to `l2_switch.p4`, which does not handle the packets well.

### A note about the control plane

A P4 program defines a packet-processing pipeline, but the rules
within each table are inserted by the control plane. When a rule
matches a packet, its action is invoked with parameters supplied by
the control plane as part of the rule.

In this exercise, we have already implemented the the control plane
logic for you. As part of bringing up the Mininet instance, the
`make run` command will install packet-processing rules in the tables of
each switch. These are defined in the `sX-commands.txt` files, where
`X` corresponds to the switch number.

**Important:** A P4 program also defines the interface between the
switch pipeline and control plane. The commands in the files
`sX-commands.txt` refer to specific tables, keys, and actions by name,
and any changes in the P4 program that add or rename tables, keys, or
actions will need to be reflected in these command files.

## Step 2: Implement the ARP responder and the Layer-2 forwarding

The `l2_switch.p4` file contains a skeleton P4 program with key pieces of
logic replaced by `TODO` comments. Your implementation should follow
the structure given in this file---replace each `TODO` with logic
implementing the missing piece.

A complete `basic.p4` will contain the following components:

1. Header type definitions for Ethernet (`ethernet_t`) and IPv4 (`ipv4_t`).
2. On top of the source, there is some hints and predefined variables to specify each field of an ARP header
3. **TODO** According to the ARP header define header type `arp_t`
4. **TODO** Add arp_t header type to struct headers
5. **TODO** add deparser logic:
	- hints/steps: filter ethertype
        - filter arp operation code to catch requests
6. **TODO** Handle ARP requests and craft response according to the match-action table, i.e., fill out the `arp_reply` action's body
7. Now, you are basically ready with the ARP responder part, now let's take into consideration the practical packet forwarding 
8. **TODO** Fill out code in the l2_foward action body, where packets need to sent out on the ports set by the control plane
9. **TODO** Fix ingress control logic, i.e., apply the different tables according to the header type and their validity.
10. **TODO** Add deparser logic, i.e., craft the packet header to be sent out


## Step 3: Run your solution

Follow the instructions from Step 1. This time, ping from
`h1` should be working  to `h2`.

### Troubleshooting

There are several problems that might manifest as you develop your program:

1. `l2_switch.p4` might fail to compile. In this case, `make run` will
report the error emitted from the compiler and halt.

2. `l2_switch.p4` might compile but fail to support the control plane
rules in the `s1-commands.txt` through `s3-command.txt` files that
`make run` tries to install using the Bmv2 CLI. In this case, `make run`
will log the CLI tool output in the `logs` directory. Use these error 
messages to fix your `l2_switch.p4` implementation.

3. `l2_switch.p4` might compile, and the control plane rules might be
installed, but the switch might not process packets in the desired
way. The `/tmp/p4s.<switch-name>.log` files contain detailed logs
that describing how each switch processes each packet. The output is
detailed and can help pinpoint logic errors in your implementation.

#### Cleaning up Mininet

In the latter two cases above, `make run` may leave a Mininet instance
running in the background. Use the following command to clean up
these instances:

```bash
make stop && make clean
```

## Next Steps

Congratulations, your implementation works! 

