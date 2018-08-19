# dns
DNS, который перенапрляет запросы на соответствующие узлы CDN


## Installation
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

ansible-playbook -i inventory -u root install.yml -e "DNS_PORT=8053 CDN_DOMAIN=cdn-sonm.soft-way.biz. MANAGER_URL=http://node-manager.cdn.sonm.soft-way.biz MANAGER_TOKEN=269f9cf80c75881adebd5db8a6782ca7b1c03f1a IP_STACK_ACCESS_KEY=d6b7f0fbe5b6e72d5b534b4989206cda"
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
dig ya.ru @127.0.0.1 -p 8053 +tcp
```


## Check prod
```
dig cdn.sonm.soft-way.biz @dns.sonm.soft-way.biz -p 8053 +tcp
```