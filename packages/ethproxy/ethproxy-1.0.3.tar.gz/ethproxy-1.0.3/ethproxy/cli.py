#!/usr/bin/env python
import argparse

from ethproxy import settings
from ethproxy.main import run


def main():
    parser = argparse.ArgumentParser(description='Dump github RSS feeds')
    parser.add_argument('--debug', "-D", help='Enable debug mode')
    parser.add_argument('--host', "-H", help='Hostname from which to serve, default ' + settings.HOST)
    parser.add_argument('--port', "-P", type=int, help='Port from which to serve, default ' + str(settings.PORT))
    parser.add_argument('--wallet', "-W", help='Wallet id, default ' + settings.WALLET)
    parser.add_argument('--pool_host', "-PH", help='Host of pool, default ' + settings.POOL_HOST)
    parser.add_argument('--pool_port', "-PP", type=int, help='Port of pool, default ' + str(settings.POOL_PORT))
    parser.add_argument('--pool_host_failover1', "-PHF1", help='Host of failover pool 1, default ' + settings.POOL_HOST_FAILOVER1)
    parser.add_argument('--pool_port_failover1', "-PPF1", type=int, help='Port of failover pool 1, default ' + str(settings.POOL_PORT_FAILOVER1))
    parser.add_argument('--pool_host_failover2', "-PHF2", help='Host of failover pool 2, default ' + settings.POOL_HOST_FAILOVER2)
    parser.add_argument('--pool_port_failover2', "-PPF2", type=int, help='Port of failover pool 2, default ' + str(settings.POOL_PORT_FAILOVER2))
    parser.add_argument('--pool_host_failover3', "-PHF3", help='Host of failover pool 3, default ' + settings.POOL_HOST_FAILOVER3)
    parser.add_argument('--pool_port_failover3', "-PPF3", type=int, help='Port of failover pool 3, default ' + str(settings.POOL_PORT_FAILOVER3))
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
    if args.pool_host_failover2:
        settings.POOL_HOST_FAILOVER2 = args.pool_host_failover2
    if args.pool_port_failover2:
        settings.POOL_PORT_FAILOVER2 = args.pool_port_failover2
    if args.pool_host_failover3:
        settings.POOL_HOST_FAILOVER3 = args.pool_host_failover3
    if args.pool_port_failover3:
        settings.POOL_PORT_FAILOVER3 = args.pool_port_failover3
    run()


if __name__ == '__main__':
    main()
