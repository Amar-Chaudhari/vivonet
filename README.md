# vivonet


## Installations

### Create Loopback Interfaces CentOS ###
```
vim /etc/sysconfig/network-scripts/ifcfg-lo:1

DEVICE=lo:1
BOOTPROTO=static
IPADDR=192.168.1.10
NETMASK=255.255.255.0
GATEWAY=192.168.1.1
ONBOOT=yes
```

### Disable IPv6

```
echo "
net.ipv6.conf.all.disable_ipv6 = 1
net.ipv6.conf.default.disable_ipv6 = 1" >> /etc/sysctl.conf && sysctl -p
```