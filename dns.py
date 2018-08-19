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
        self.clients_cache = {}
        self.cache = {}
        self.cache_updated = None
        self.cache_refresh = datetime.timedelta(seconds=60)

    def resolve(self, request, handler):
        reply = request.reply()

        query = str(request.q.qname)
        if query != settings.CDN_DOMAIN:
            return reply

        client_ip, client_port = handler.client_address

        code_continent = self.get_continent_code_from_ip(client_ip)
        cdn_node_ip = self.get_cdn_node_ip(code_continent)

        if cdn_node_ip:
            dns_answer = '{} 300 IN A {}'.format(reply.q.qname, cdn_node_ip)
            reply.add_answer(*RR.fromZone(dns_answer))

        return reply

    def get_cdn_node_ip(self, code_continent) -> Optional[str]:
        now = datetime.datetime.now()
        if not self.cache_updated or (now - self.cache_updated) > self.cache_refresh:
            url = settings.NODE_MANAGER_URL + '/api/nodes_by_regions/'
            headers = {'Authorization': 'Token %s' % settings.NODE_MANAGER_TOKEN}
            response = requests.get(url, headers=headers)
            self.cache = response.json()
            self.cache_updated = now

        nodes = self.cache.get(code_continent)
        if not nodes:
            not_empty_regions = [i for i in self.cache.values() if i]
            if not_empty_regions:
                nodes = random.choice(not_empty_regions)

        if nodes:
            cdn_node_ip = random.choice(nodes)
            return cdn_node_ip

    def get_continent_code_from_ip(self, client_ip) -> Optional[str]:
        if client_ip not in self.clients_cache:
            continent_code = get_continent_code_from_ip(client_ip)
            self.clients_cache[client_ip] = continent_code
        return self.clients_cache[client_ip]


resolver = Resolver()

# server = DNSServer(resolver, port=8053, address='0.0.0.0', tcp=True)
server = DNSServer(resolver, port=8053, address='0.0.0.0')
server.start()
