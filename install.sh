#!/bin/sh
# /bin/sh install.sh -a "INSTANCE_HOST_IP" -d "DOMAIN" -p PORT -u "MANAGER_URL" -t "MANAGER_TOKEN" -k "IP_STACK_ACCESS_KEY"

ERROR='\033[0;31m'
INFO='\033[1;34m'
NC='\033[m'
SUCCESS='\033[0;32m'

INSTANCE_HOST_IP=''
DOMAIN=''
PORT=''
MANAGER_URL=''
MANAGER_TOKEN=''
IP_STACK_ACCESS_KEY=''

function check_error {
    if [ $? -ne 0 ]; then
      echo "${ERROR}ERROR";
        exit 1
      else
        echo "${SUCCESS}SUCCESS";
    fi
}

while getopts ":a:d:p:u:t:k:" opt; do
  case $opt in
    a) INSTANCE_HOST_IP="$OPTARG"
    ;;
    d) DOMAIN="$OPTARG"
    ;;
    p) PORT="$OPTARG"
    ;;
    u) MANAGER_URL="$OPTARG"
    ;;
    t) MANAGER_TOKEN="$OPTARG"
    ;;
    k) IP_STACK_ACCESS_KEY="$OPTARG"
    ;;
    \?) echo "${ERROR}ERROR: ${NC}Invalid option -$OPTARG"; exit 1
    ;;
  esac
done

if [[ $INSTANCE_HOST_IP = "" ]]; then
   echo "${ERROR}ERROR: ${NC}Parameter INSTANCE_HOST_IP \"-a\" has been not empty";
   exit 1
fi

if [[ $DOMAIN = "" ]]; then
   echo "${ERROR}ERROR: ${NC}Parameter DOMAIN \"-d\" has been not empty";
   exit 1
fi

if [[ $PORT = "" ]]; then
   echo "${ERROR}ERROR: ${NC}Parameter PORT \"-p\" has been not empty";
   exit 1
fi

if [[ $MANAGER_URL = "" ]]; then
   echo "${ERROR}ERROR: ${NC}Parameter MANAGER_URL \"-u\" has been not empty";
   exit 1
fi

if [[ $IP_STACK_ACCESS_KEY = "" ]]; then
   echo "${ERROR}ERROR: ${NC}Parameter IP_STACK_ACCESS_KEY \"-k\" has been not empty";
   exit 1
fi


echo "== INSTALATION SONM CDN DNS =="
echo "INSTANCE_HOST_IP:    " $INSTANCE_HOST_IP
echo "DOMAIN:              " $DOMAIN
echo "PORT:                " $PORT
echo "MANAGER_URL:         " $MANAGER_URL
echo "MANAGER_TOKEN:       " $MANAGER_TOKEN
echo "IP_STACK_ACCESS_KEY: " $IP_STACK_ACCESS_KEY


echo "\n${INFO}Install python for remote host ... ${NC}"
ssh root@$INSTANCE_HOST_IP apt-get install -y python
check_error

if [ -d "./venv" ]; then
    echo "\n${INFO}Set virtual environment (venv) ...${NC}"
    source ./venv/bin/activate
    check_error
else
  echo "\n${INFO}Create virtual environment for ansible ... ${NC}"
  virtualenv venv
  check_error

  echo "\n${INFO}Set virtual environment (venv) ...${NC}"
  source ./venv/bin/activate
  check_error

  echo "\n${INFO}Install pip for current system ...${NC}"
  curl https://bootstrap.pypa.io/get-pip.py | python
  check_error
fi

echo "\n${INFO}Install ansible from ansible/requirements.txt ...${NC}"
pip install -r ansible/requirements.txt
check_error

echo "\n${INFO}Set INSTANCE_HOST_IP to ansible/inventory file ...${NC}"
echo "$INSTANCE_HOST_IP" > ansible/inventory
echo "${SUCCESS}SUCCESS";


echo "\n${INFO}Run ansible playbook (ansible/intsall.yml)...${NC}"
ansible-playbook -i ansible/inventory -u root ansible/install.yml -e "DNS_PORT=$PORT CDN_DOMAIN=$DOMAIN. MANAGER_URL=$MANAGER_URL MANAGER_TOKEN=$MANAGER_TOKEN IP_STACK_ACCESS_KEY=$IP_STACK_ACCESS_KEY"
check_error
