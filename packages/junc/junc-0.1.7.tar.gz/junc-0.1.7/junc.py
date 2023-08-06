"""
Usage:
    junc connect <name>
    junc list [--json]
    junc add (<name> <username> <ip>) [<location>]
    junc remove <name>
    junc backup [<file>]

Options:
    -h --help     Show this screen.
    --version     Show version.
    --json        Output server list as JSON instead of a (readable) table

Arguments:
    name          Human-readable name of a server
    username      Username you wish to login with
    ip            The IP of the server
    location      (Optional) Where the server is located (useful for headless machines ie. raspberry pi)

Notes:
    Data is stored in ~/.junc.json
    Default backup location is ~/.junc.json.bak
"""

VERSION = "0.1.7"

import os
import sys

from docopt import docopt
import json

from storage import Storage
from server import *

def cli(args):
    storage = Storage()
    try:
        server_list = storage.get_servers()
    except PermissionError:
        print("Error: Permission denied. Try again with sudo or change permissions on " + storage.file_path + " (Recommended)")
        return False

    if args['list']:
        server_table = storage.get_server_table()
        if args['--json']:
            print(json.dumps(server_list, indent=2))
            return server_list
        print(server_table.table)
        return server_table

    if args['add']:
        server_list.append(new_server(args))
        storage.write(server_list)
        return server_list

    if args['connect']:
        connection = ""
        for server in server_list:
            if server['name'] == args['<name>']:
                connection = server['username'] + "@" + server['ip']
        if not connection:
            print("Couldn't find that server...")
            return False
        print("Connecting...")
        os.system('ssh ' + connection)
        return True

    if args['remove']:
        for i in range(len(server_list)):
            if server_list[i]['name'] == args['<name>']:
                del server_list[i]
                storage.write(server_list)
                return server_list
            if i == len(server_list) - 1:
                print("Couldn't find that server...")
                return False

    if args['backup']:
        storage.backup(args['<file>'])
        print("Done.")
        return True

def main():
    arguments = docopt(__doc__, version="Junc v" + VERSION)
    if not cli(arguments):
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()
