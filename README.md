# dns
DNS is the element of [SONM CDN](https://github.com/telminov/sonm-cdn-node-manager/blob/master/SONM%20CDN.md)

DNS that redirects requests to the appropriate CDN nodes


## Installation
Referens installation descripted in ansible-playbook - https://github.com/telminov/sonm-cdn-dns/blob/master/ansible/install.yml
Install example on Digital Ocean instance with Ubuntu Server 18.04

Need installed packages: 
- python 2.X (for ansible)
- virtualenv 
- pip
- ansible



To use this project, you need two IP_STACK_ACCESS_KEY tokens to use the GEO API and MANAGER_TOKEN from node_manager for the return ip

How to get TOKENS:
- IP_STACK_ACCESS_KEY - Need registration on [ipstack.com](https://ipstack.com/) and copy API KEY
- MANAGER_TOKEN -  In node_manager by the path `/admin/` in the Tokens tab. Create a new token for the required user.

### use command line

install python on host
```
ssh root@INSTANCE_HOST_IP
apt install -y python
```

start install ansible-playbook
```
cd <project_path>/ansible
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
echo "INSTANCE_HOST_IP" > inventory

ansible-playbook -i inventory -u root install.yml -e "DNS_PORT=53 CDN_DOMAIN=cdn-sonm.soft-way.biz. MANAGER_URL=http://node-manager.cdn.sonm.soft-way.biz MANAGER_TOKEN=123 IP_STACK_ACCESS_KEY=123"
```

### use installation script (Ubuntu/MacOS)
run for project directory
```
/bin/sh install.sh -a "INSTANCE_HOST_IP" -d "DOMAIN" -p PORT -u "MANAGER_URL" -t "MANAGER_TOKEN" -k "IP_STACK_ACCESS_KEY"
```

### create dns record

To use, you need to add a DNS record for our host (for example, cdn-sonm.soft-way.biz)
```
cdn-sonm NS INSTANCE_HOST_IP
```

## Check local dns
run dns
```
cd <project_path>
virtualenv -p python3 venv
source venv/bin/activate
python3 dns.py
```

in other terminal
```
dig cdn-sonm.soft-way.biz @127.0.0.1 -p 8053
```


## Check prod
```
dig cdn-sonm.soft-way.biz @dns.sonm.soft-way.biz
```
or
```
dig cdn-sonm.soft-way.biz
```
