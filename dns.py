from dnslib import RR
from dnslib.server import DNSServer

LOCALHOST = '127.0.0.1'

OTHER_LOCALHOST = '127.0.0.2'


class Resolver:

    def resolve(self, request, handler):
        client_ip, client_port = handler.client_address
        reply = request.reply()

        if client_ip == LOCALHOST:
            instance_app_ip = LOCALHOST
        else:
            instance_app_ip = OTHER_LOCALHOST

        dns_answer = '{} 300 IN A {}'.format(reply.q.qname, instance_app_ip)
        reply.add_answer(*RR.fromZone(dns_answer))
        return reply


resolver = Resolver()

# server = DNSServer(resolver, port=8053, address='localhost', tcp=True)
server = DNSServer(resolver, port=8053, address='0.0.0.0', tcp=True)
server.start()