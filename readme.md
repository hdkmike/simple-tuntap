# Bring up Network Interface

```bash
ip link set tun0 up
ip address add 192.168.40.1/32 dev tun0
ip route add 192.168.40.2/32 dev tun0
```

# Bring down Network Interface

```bash
ip route del 192.168.40.2/32 dev tun0
ip link set tun0 down
```
