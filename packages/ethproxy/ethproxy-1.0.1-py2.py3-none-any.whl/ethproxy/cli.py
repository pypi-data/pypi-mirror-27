#!/usr/bin/env python
import argparse

from ethproxy import settings
from ethproxy.main import run


def main():
    parser = argparse.ArgumentParser(description='Dump github RSS feeds')
    parser.add_argument('--debug', help='Enable debug mode')
    parser.add_argument('--host', help='Hostname from which to serve, default ' + settings.HOST)
    parser.add_argument('--port', help='Port from which to serve, default ' + str(settings.PORT))
    parser.add_argument('--wallet', help='Wallet id, default ' + str(settings.WALLET))
    parser.add_argument('--pool_host', help='Host of pool, default ' + str(settings.POOL_HOST))
    parser.add_argument('--pool_port', help='Port of pool, default ' + str(settings.POOL_PORT))
    parser.add_argument('--pool_host_failover1', help='Host of pool 2, default ' + str(settings.POOL_HOST_FAILOVER1))
    parser.add_argument('--pool_port_failover1', help='Port of pool 2, default ' + str(settings.POOL_PORT_FAILOVER1))
    args = parser.parse_args()

    if args.debug:
        settings.DEBUG = args.debug
    if args.host:
        settings.HOST = args.host
    if args.port:
        settings.PORT = args.port
    if args.wallet:
        settings.WALLET = args.wallet
    if args.pool_host:
        settings.POOL_HOST = args.pool_host
    if args.pool_port:
        settings.POOL_PORT = args.pool_port
    if args.pool_host_failover1:
        settings.POOL_HOST_FAILOVER1 = args.pool_host_failover1
    if args.pool_port_failover1:
        settings.POOL_PORT_FAILOVER1 = args.pool_port_failover1
    run()


if __name__ == '__main__':
    main()
