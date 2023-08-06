import json
import os

from terminaltables import AsciiTable

class Storage():
    def __init__(self):
        self.file_path = os.path.expanduser("~") + "/.junc.json"
        self.create_file(self.file_path)

    def create_file(self, file_path):
        open(file_path, 'a')
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
