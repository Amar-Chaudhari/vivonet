# vivonet

## Web APP Deployment

### Local Machine Deploy

#### Download Code

```
git clone https://github.com/Amar-Chaudhari/vivonet.git vivonet
cd vivonet
git pull
```

#### Install Dependencies

```
We require Python 2.7 to be installed
python -V
cd vivonet/vivonet_site
pip install -r requirements.txt
```

#### Run Development Server

```
python manage.py migrate
python manage.py runserver
```

### Admin Panel Access (Create/Delete Entries in Database)

```
http://127.0.0.1:8000/admin/
Username: admin
Password: Super123
```

## Installations (Other)

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