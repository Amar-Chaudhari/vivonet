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
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

### Admin Panel Access (Create/Delete Entries in Database)

```
http://127.0.0.1:8000/admin/
Username: admin
Password: Super123
```

## Deploy on Server

**ssh to controller:**
```
ssh -l root 198.11.21.36 -p 10000
```
**ssh to web server**
```
ssh 10.0.1.40
```
**Download latest code and deploy**
```
source /opt/virtualenv/vivo_env/bin/activate
cd /opt/projects/vivonet/
git pull
rm -rf /opt/webapp/vivonet_site/
cp -rf vivonet_site /opt/webapp/
cd /opt/webapp/vivonet_site/
python manage.py collectstatic
systemctl restart gunicorn
systemctl restart nginx
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