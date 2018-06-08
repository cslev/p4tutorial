# Implementing Layer-2 Forwarding

## Introduction

The objective of this exercise is to extend the previous `l2_switch` P4 application with P4Runtime support, i.e., the control plane will not populate the flow tables via the CLI (e.g., `sX-commands.txt`), but rather implement the logic in a P4Runtime controller.
If you have not completed the pure **l2_switch** example, please do it first and refer to its step when doing this tutorial, as the same functioning will be realized.

> **Spoiler alert:** There is a reference solution in the `solution`
> sub-directory. Feel free to compare your implementation to the
> reference.

## First steps

As it was in case of our previous `l2_switch` example, if the mininet system and the switch code is compiled, the forwarding will not work, as the flow tables of the switches are empty.

To test, do the following steps:
1. In your shell, run:
   ```bash
   make run
   ```
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


## Step 2: Implement the ARP responder and the Layer-2 forwarding

The `l2_switch.p4` file contains the working P4 implementation of the switch.
This time, we only write the controller, which a skeleton implementation in Python is provided for.
Open `l2_switch_controller.py` and replace the `TODO` comments with the control logic.

A complete `l2_switch_controller.py` will contain the following components:

1. `writeArpRules` function showing how a specific `table_entry` should be assembled to push down to a P4 switch.
2. **TODO:** similarly to writeArpRules(), create a `table_entry `for the `l2forward_exact` and fill out the corresponding fields set as params
3. The control plane logic is found in the main function. The logic is just a couple of dictionaries containing the fundamental topology information needed for the ARP RESPONSE packet crafint and the practical Layer-2 forwarding.
4. First, a connection is needed to be established to each switch. An example of connecting to a switch can be defined like this:
`p4runtime_lib.bmv2.Bmv2SwitchConnection('s1', address='127.0.0.1:50051', device_id=0)`
5. **TODO** Iterate through all switches and establish the connection (switch `sX` is under 127.0.0.1:5005`X` and its device id is `X-1`)
6. **TODO** Install P4 program into each switch by using the p4info files. An example of this can be found below:
`switch_connection_reference.SetForwardingPipelineConfig(p4info=p4info_helper.p4info, bmv2_json_file_path=bmv2_file_path)`
7. **TODO** Write ARP rules according to hosts_mac dict()
8. **TODO** Write L2 forwarding rules according to switch_port dict(dict())
9. **Optional TODO** Use function `readTablesRules()` to print out the table rules for debugging

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

Congratulations, your implementation works! In the next exercise we
will build on top of this and add support for a basic tunneling
protocol: [basic_tunnel](../basic_tunnel)!

