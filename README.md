# dns
DNS is the element of [SONM CDN](https://github.com/telminov/sonm-cdn-node-manager/blob/master/SONM%20CDN.md)

DNS that redirects requests to the appropriate CDN nodes


## Installation
Referens installation descripted in ansible-playbook - https://github.com/telminov/sonm-cdn-dns/blob/master/ansible/install.yml

Install example on Digital Ocean instance with Ubuntu Server 18.04

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
