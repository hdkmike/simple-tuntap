# Overview
Simple tun program to write and read data to a tun adapter

# Interfaces
Assumes the following:
* Local tun adapter address is `192.168.40.1`
* Destination for traffic is `192.168.40.2`

## Bring up Network Interface

```bash
ip link set tun0 up
ip address add 192.168.40.1/32 dev tun0
ip route add 192.168.40.2/32 dev tun0
```

## Bring down Network Interface

```bash
ip route del 192.168.40.2/32 dev tun0
ip link set tun0 down
```

# Routing

## Enable Routing (on Linux)
Run `sysctl -w net.ipv4.ip_forward=1` to temporarily enable routing
Edit `/etc/sysctl.conf` with the line `net.ipv4.ip_forward = 1` to make routing persistant across reboots

## Disable Routing
Run `sysctl -w net.ipv4.ip_forward=0` to temporarily enable routing
Edit `/etc/sysctl.conf` with the line `net.ipv4.ip_forward = 0` to make routing persistant across reboots

# Sample programs

## Echo
Simply echos back the data received by the tun to the sender but swaps the IP src and dst.

* `ping 192.168.40.2` will result in a reply
    * It will keep up with a flood ping (`sudo ping -f 192.168.40.2`) but buffers slightly
    * Ping won't work for non-local pings due to the "dumb" echo handler. It doesn't switch the echo/reply types.
* netcat will work with UDP
    * Set up one terminal running `nc -u -l 1234`
    * Set up another terminal running `nc -u 192.168.40.2 1234`
    * You can watch messages from the second terminal show up in the first
* netcat doesn't _completely_ work with TCP because of the "dumb" echo handler
    * Set up one terminal running `nc -l 1234`
    * Set up another terminal running `nc 192.168.40.2 1234`
    * You can watch messages from the second terminal show up in the first
    * Sending a file does not work becuase of the "dumb" echo handler

## Wireshark

* You can run wireshark on the TUN adapter to see the traffic
* `tcpdump` or `tshark` will also work
