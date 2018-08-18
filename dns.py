import datetime
import random
from typing import Optional

from dnslib import RR
from dnslib.server import DNSServer
import requests

from geo_ip import get_continent_code_from_ip
import settings


class Resolver:
    def __init__(self):
        super().__init__()
        self.cache = {}
        self.cache_updated = None
        self.cache_refresh = datetime.timedelta(seconds=60)

    def resolve(self, request, handler):
        client_ip, client_port = handler.client_address
        reply = request.reply()

        code_continent = get_continent_code_from_ip(client_ip)
        cdn_node_ip = self.get_cdn_node_ip(code_continent)

        if cdn_node_ip:
            dns_answer = '{} 300 IN A {}'.format(reply.q.qname, cdn_node_ip)
            reply.add_answer(*RR.fromZone(dns_answer))

        return reply

    def get_cdn_node_ip(self, code_continent) -> Optional[str]:
        now = datetime.datetime.now()
        if (now - self.cache_updated) > self.cache_refresh:
            url = settings.NODE_MANAGER_URL + '/api/nodes_by_regions/'
            headers = {'Authentication': 'Token %s' % settings.NODE_MANAGER_TOKEN}
            response = requests.get(url, headers=headers)
            self.cache = response.json()
            self.cache_updated = now

        nodes = self.cache.get(code_continent)
        if not nodes:
            nodes = random.choice(self.cache.values())

        if nodes:
            cdn_node_ip = random.choice(nodes)
            return cdn_node_ip


resolver = Resolver()

server = DNSServer(resolver, port=8053, address='0.0.0.0', tcp=True)
server.start()
