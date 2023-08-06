import os
###
# Examples of command line for miners:
#
#   ethminer.exe --farm-recheck 200 -G -F http://HOST:PORT/
#   ethminer.exe --farm-recheck 300 -G -F http://HOST:PORT/rig1
#
#   ethminer.exe -G -F http://127.0.0.1:8080/
#   ethminer.exe --farm-recheck 100 -G -F http://192.168.0.33:8080/rig1
#
#  farm-recheck parameter is very individual. Just test different values.
#
#  You can submit shares without workername or
#  You can provide workername:
#   - with url like "/rig1"
#   - or use automatically numbering(integer) based on IP of miner
#
#  Servers:
#    EU-Server:  eth-eu.dwarfpool.com  (France)
#    US-Server:  eth-us.dwarfpool.com  (EastCoast: Montreal,Canada)
#    US-Server:  eth-us2.dwarfpool.com (WestCoast: Las Vegas)
#    RU-Server:  eth-ru.dwarfpool.com  (Moscow)
#    HK-Server:  eth-hk.dwarfpool.com  (Hong-Kong)
#    CN-Server:  eth-cn.dwarfpool.com  (Shanghai)
#    SG-Server:  eth-sg.dwarfpool.com  (Singapore)
#    AU-Server:  eth-au.dwarfpool.com  (Melbourne)
#
# Note: most of these settings are probably useless
###

# ******************** GENERAL SETTINGS ***************

# Enable some verbose debug (logging requests and responses).
DEBUG = os.environ.get("DEBUG", False)

# Destination for application logs, files rotated once per day.
LOGDIR = 'log/'

# Main application log file.
LOGFILE = None
LOG_TO_FILE = False

# Possible values: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOGLEVEL = 'INFO'

# How many threads use for synchronous methods (services).
# 30 is enough for small installation, for real usage
# it should be slightly more, say 100-300.
THREAD_POOL_SIZE = 30

# RPC call throws TimeoutServiceException once total time since request has been
# placed (time to delivery to client + time for processing on the client)
# crosses _TOTAL (in second).
# _TOTAL reflects the fact that not all transports deliver RPC requests to the clients
# instantly, so request can wait some time in the buffer on server side.
# NOT IMPLEMENTED YET
#RPC_TIMEOUT_TOTAL = 600

# RPC call throws TimeoutServiceException once client is processing request longer
# than _PROCESS (in second)
# NOT IMPLEMENTED YET
#RPC_TIMEOUT_PROCESS = 30

# ******************** TRANSPORTS *********************

# Hostname or external IP to expose
HOSTNAME = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", 8080)
HOST = HOSTNAME
COIN = "ETH"

# Port used for Socket transport. Use 'None' for disabling the transport.
LISTEN_SOCKET_TRANSPORT = 3333

# Port used for HTTP Poll transport. Use 'None' for disabling the transport
LISTEN_HTTP_TRANSPORT = 8000

# Port used for HTTPS Poll transport
LISTEN_HTTPS_TRANSPORT = 8001

# Port used for WebSocket transport, 'None' for disabling WS
LISTEN_WS_TRANSPORT = 8002

# Port used for secure WebSocket, 'None' for disabling WSS
LISTEN_WSS_TRANSPORT = 8003

# ******************** SSL SETTINGS ******************

# Private key and certification file for SSL protected transports
# You can find howto for generating self-signed certificate in README file
SSL_PRIVKEY = 'server.key'
SSL_CACERT = 'server.crt'

# ******************** TCP SETTINGS ******************

# Enables support for socket encapsulation, which is compatible
# with haproxy 1.5+. By enabling this, first line of received
# data will represent some metadata about proxied stream:
# PROXY <TCP4 or TCP6> <source IP> <dest IP> <source port> </dest port>\n
#
# Full specification: http://haproxy.1wt.eu/download/1.5/doc/proxy-protocol.txt
TCP_PROXY_PROTOCOL = False

# ******************** HTTP SETTINGS *****************

# Keepalive for HTTP transport sessions (at this time for both poll and push)
# High value leads to higher memory usage (all sessions are stored in memory ATM).
# Low value leads to more frequent session reinitializing (like downloading address history).
HTTP_SESSION_TIMEOUT = 3600 # in seconds

# Maximum number of messages (notifications, responses) waiting to delivery to HTTP Poll clients.
# Buffer length is PER CONNECTION. High value will consume a lot of RAM,
# short history will cause that in some edge cases clients won't receive older events.
HTTP_BUFFER_LIMIT = 10000

# User agent used in HTTP requests (for both HTTP transports and for proxy calls from services)
#USER_AGENT = 'Stratum/0.1'
USER_AGENT = 'PoolServer'

# Provide human-friendly user interface on HTTP transports for browsing exposed services.
BROWSER_ENABLE = True

SIGNING_ID = None

# ******************** OTHER CORE SETTINGS *********************
# Use "echo -n '<yourpassword>' | sha256sum | cut -f1 -d' ' "
# for calculating SHA256 of your preferred password
ADMIN_PASSWORD_SHA256 = None # Admin functionality is disabled
#ADMIN_PASSWORD_SHA256 = '9e6c0c1db1e0dfb3fa5159deb4ecd9715b3c8cd6b06bd4a3ad77e9a8c5694219' # SHA256 of the password

# IP from which admin calls are allowed.
# Set None to allow admin calls from all IPs
ADMIN_RESTRICT_INTERFACE = '127.0.0.1'

###
# Command line for miners:
#   ethminer.exe -G -F http://YOUR_PROXY_IP:8080/
#   ethminer.exe -G -F http://YOUR_PROXY_IP:8080/rig1
#
#  You can submit shares without workername or
#  You can provide workername:
#   - with url like "/rig1"
#   - or use automatically numbering(integer) based on IP of miner
###

# Coin address where money goes.
WALLET = os.environ.get("WALLET", "XXXXXX")

# It's useful for individually monitoring and statistic.
ENABLE_WORKER_ID = False

# On DwarfPool you have option to monitor your workers via email.
# If WORKER_ID is enabled, you can monitor every worker/rig separately.
MONITORING = False
MONITORING_EMAIL = 'mail@example.com'

# Main pool
POOL_HOST = os.environ.get("POOL_HOST", "eth-eu.dwarfpool.com")
POOL_PORT = os.environ.get("POOL_PORT", 8008)

# Failover pool.
POOL_FAILOVER_ENABLE = True
POOL_HOST_FAILOVER1 = os.environ.get("POOL_HOST_FAILOVER1", "eth-ru.dwarfpool.com")
POOL_PORT_FAILOVER1 = os.environ.get("POOL_PORT_FAILOVER1", 8008)
POOL_HOST_FAILOVER2 = os.environ.get("POOL_HOST_FAILOVER2", "eth-us.dwarfpool.com")
POOL_PORT_FAILOVER2 = os.environ.get("POOL_PORT_FAILOVER2", 8008)
POOL_HOST_FAILOVER3 = os.environ.get("POOL_HOST_FAILOVER3", "eth-hk.dwarfpool.com")
POOL_PORT_FAILOVER3 = os.environ.get("POOL_PORT_FAILOVER3", 8008)
