#!/usr/bin/env python

from __future__ import print_function

import sys
import codecs
import urllib2
import json
import base64
import time

import colorama

# TODO: Config file / args
MASTER_LIST_URL = 'http://master.openra.net/games_json'
MODRA = 'ra@release-20171014'
REFRESH_TIME = 5

def print_server(server):
    print(server['name'], end='')
    if 'started' in server:
        print(colorama.Fore.RED + ' (started)')
    else:
        print(colorama.Fore.GREEN + ' (waiting)')

    if server['clients']:
        for client in server['clients']:
            print(base64.b64decode(client).decode('utf8'))

    print(colorama.Style.RESET_ALL)

def print_active(servers):
    for server in servers:
        if server['mods'] == MODRA:
            if int(server['maxplayers']) == 2: # fuck teamgames
                if int(server['players']) > 0 or int(server['spectators']) > 0:
                    print_server(server)


def main():
    while True:
        print(chr(27) + '[2J') # clear screen
        resp = urllib2.urlopen(MASTER_LIST_URL).read().decode('utf8')
        servers = json.loads(resp)
        print_active(servers)
        time.sleep(REFRESH_TIME)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
