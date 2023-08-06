import json
import os

from terminaltables import AsciiTable

class Storage():
    def __init__(self):

        self.file_path = self.get_file_path()
        # self.file_path = os.path.expanduser("~") + "/.junc.json"
        self.create_file(self.file_path)

    def get_file_path(self):
        path = open('./storage_path', 'r').read().replace('\n', '')
        if not path:
            with open('./storage_path', 'w') as f:
                path = os.path.expanduser("~") + "/junc.json"
                f.write(path)
                return path
        return path


    def set_new_location(self, location):
        server_list = self.get_servers()
        try:
            with open('./storage_path', 'w') as f:
                f.write(location)
            self.file_path = location
        except PermissionError:
            print("Error: Permission denied. Run again with sudo or pick another location")
            return False
        self.write(server_list)

    def create_file(self, file_path):
        try:
            open(file_path, 'a')
        except PermissionError:
            print("Error: Permission denied. Using default location. Please choose a different location")
            self.file_path = os.path.expanduser("~") + "/junc.json"
        return True

    def write(self, server_dict):
        with open(self.file_path, 'w') as f:
            json.dump(server_dict, f, indent=4)
        return True

    def get_servers(self):
        try:
            return json.loads(open(self.file_path, 'r').read())
        except json.decoder.JSONDecodeError:
            return []

    def get_server_table(self):
        server_list = self.get_servers()
        if not server_list:
            return "No Servers :("
        table_data = [
            ['Name', "Address", "Location"],
        ]
        for server in server_list:
            table_data.append([server['name'], server['username'] + "@" + server['ip'], server['location']])
        return AsciiTable(table_data).table
