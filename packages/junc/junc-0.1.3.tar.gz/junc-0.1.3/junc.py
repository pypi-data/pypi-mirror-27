"""
Usage:
    junc connect <name>
    junc list
    junc add (<name> <username> <ip>) [<location>]
    junc remove <name>
    junc location [<new_location>]

Options:
    -h --help     Show this screen.
    --version     Show version.

Notes:
    Data is stored in ~/.junc.json
    Change location with "junc config /full/path/to/new/file"
    When changing locations, your data will be moved to the new location
"""

VERSION = "0.1.3"

import os
import sys

from docopt import docopt

from storage import Storage
from server import *

def cli(args):
    storage = Storage()
    try:
        server_list = storage.get_servers()
        server_table = storage.get_server_table()
    except PermissionError:
        print("Error: Permission denied. Try again with sudo or move to another location (junc location <new_location>)")

    if args['list']:
        print(server_table)

    if args['add']:
        server_list.append(new_server(args))
        storage.write(server_list)

    if args['connect']:
        connection = ""
        for server in server_list:
            if server['name'] == args['<name>']:
                connection = server['username'] + "@" + server['ip']
        if not connection:
            print("Couldn't find that server...")
            sys.exit(1)
        os.system('ssh ' + connection)

    if args['remove']:
        for i in range(len(server_list)):
            if server_list[i]['name'] == args['<name>']:
                del server_list[i]
                break
            if i == len(server_list) - 1:
                print("Couldn't find that server...")
        storage.write(server_list)

    if args['location']:
        if not args['<new_location>']:
            print(storage.file_path)
            sys.exit(0)
        if storage.set_new_location(args['<new_location>']):
            print("New location set")
def main():
    arguments = docopt(__doc__, version="Junc v" + VERSION)
    cli(arguments)

if __name__ == '__main__':
    main()
