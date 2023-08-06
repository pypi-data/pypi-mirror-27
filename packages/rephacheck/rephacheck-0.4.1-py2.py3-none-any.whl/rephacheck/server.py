#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Determine by voting which is the state of each node.
For this to work properly, you need to have an odd number of nodes.
"""

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

from collections import Counter
import http.server
from io import open
import json
import logging
import logging.handlers
import psycopg2
from socket import AF_INET6

with open('/etc/rephacheck.json') as rephaconf:
    conf = json.load(rephaconf)

LISTEN = conf.get('listen', 'localhost')
PORT = conf.get('port', 8000)
NODES = conf.get('nodes')
CONNINFO = conf.get('conninfo')
TIMEOUT = conf.get('timeout', 5)
CURRENT = conf.get('local_node_id')
LOG_FILE = conf.get('log_file', '/var/log/rephacheck.log')

logger = logging.getLogger('rephacheck')
logger.setLevel(logging.INFO)
file_handler = logging.handlers.RotatingFileHandler(
    LOG_FILE, maxBytes=102400, backupCount=7
)
logger.addHandler(file_handler)


class Server(http.server.HTTPServer):
    address_family = AF_INET6


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.s = get_quorum_state(CURRENT)
        http.server.SimpleHTTPRequestHandler.__init__(self, *args, **kwargs)

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(self.s.encode('utf-8'))
        self.wfile.write('\n'.encode('utf-8'))
        logger.info('client: {} - state: {}'.format(self.client_address[0],
                                                    self.s))

    def do_HEAD(self):
        self._set_headers()


def get_state(addr, port, node_id):
    try:
        # postgresql query
        con_args = {'host': addr, 'port': port, 'connect_timeout': TIMEOUT}
        con_args.update(CONNINFO)
        con = psycopg2.connect(**con_args)
        cur = con.cursor()
        query = 'SELECT active, type FROM repmgr.nodes WHERE node_id = {};'
        cur.execute(query.format(node_id))
        data = cur.fetchone()
        cur.close()
        # return result
        return data
    except Exception:
        # an error occured, so return false by default
        return (False, 'unknown')


def get_quorum_state(node_id):
    # init vars
    votes = []
    # ask each node for the state of `node_id`
    for node in NODES.values():
        active, role = get_state(node['addr'], node['port'], node_id)
        # if node considered active take vote, otherwise fence it
        if active:
            votes.append(role)
        else:
            votes.append('fenced')
    # determines voting result
    results = Counter(votes)
    state = results.most_common(1)[0][0]
    # return result
    return state


def run():
    # run http server
    httpd = Server((LISTEN, PORT), Handler)
    print('serving at port', PORT)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
