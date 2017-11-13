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

# Sample programs

## Echo
Simply echos back the data received by the tun to the sender

* `ping 192.168.40.2` will result in a reply
    * It will keep up with a flood ping (`sudo ping -f 192.168.40.2`) but buffers slightly
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
