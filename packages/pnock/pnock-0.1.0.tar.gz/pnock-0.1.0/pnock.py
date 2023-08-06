# Python 2 compatibility
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import socket
from multiprocessing.dummy import Pool
import argparse
import sys

"""
Pnock - knocking ports in pure python

Author: Daan de Graaf
"""

DEFAULT_TIMEOUT = 0.5 # 500 milliseconds

def local_ip():
    """ 
    Returns the local IP of the current machine 
    (or at least one of them).
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

# Errors that signal a closed port are dependent on the python version
if sys.version_info >= (3, 0):
    KNOCK_FAIL_ERRORS = (ConnectionRefusedError, OSError)
else:
    KNOCK_FAIL_ERRORS = (socket.error, OSError)


def knock(ip, port, timeout=DEFAULT_TIMEOUT):
    """ Checks if the port is open on the given ip. """
    try:
        socket.create_connection((ip, port), timeout)
        return True
    except KNOCK_FAIL_ERRORS:
        return False

def sweep(ips, port, timeout=DEFAULT_TIMEOUT):
    """ Returns the ips that have a server listening the given port. """
    pool = Pool(len(ips))
    knocks = pool.map(lambda ip: knock(ip, port, timeout), ips)
    pool.close()
    pool.join()
    return [ip for (ip, up) in zip(ips, knocks) if up]

def iface_prefix(iface_ip):
    # Cut off the last octet
    i = iface_ip.rfind('.')
    return iface_ip[:i+1]

def lan_ips(iface_ip=local_ip()):
    """ Returns a list of possible ips for the given interface ip. """
    return ['{}{}'.format(iface_prefix(iface_ip), i) for i in range(255)]

def sweep_lan(port, iface_ip=local_ip(), timeout=DEFAULT_TIMEOUT):
    """ Returns all ips in the LAN where a server is running on port. """
    return sweep(lan_ips(iface_ip), port, timeout)

def main():
    parser = argparse.ArgumentParser(description='LAN Port knocker')
    parser.add_argument('port', type=int, help='The port to knock on')
    parser.add_argument('-i', '--interface', dest='iface_ip', default=local_ip(), help='The interface to scan the LAN of')
    parser.add_argument('-t', '--timeout', dest='timeout', type=float, default=DEFAULT_TIMEOUT, help='The timeout to wait for replies on the knocks')
    args = parser.parse_args()
    print('Knocking port {} on {}0/24'.format(args.port, iface_prefix(args.iface_ip)), file=sys.stderr)
    ips = sweep_lan(args.port, iface_ip=args.iface_ip, timeout=args.timeout)
    for ip in ips:
        print(ip)

if __name__ == "__main__":
    main()
