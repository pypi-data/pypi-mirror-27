#
# Potap module by GuillaumeDesforges
#

from os.path import normcase, join, isabs
from os import getcwd
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json

class Baker:
    def __init__(self, templates_folder_path=None):
        if templates_folder_path == None:
            templates_folder_path = join(getcwd(), 'templates')
        elif not isabs(templates_folder_path):
            templates_folder_path = join(getcwd(), templates_folder_path)
        self.env = Environment(
            loader = FileSystemLoader(templates_folder_path)
        )

    def bake_file(self, data_file_path, template_name):
        template = self.env.get_template(template_name + '.tmpl')
        with open(data_file_path, 'r') as f:
            data_dict = json.loads(f.read())
        return template.render(data_dict)

    def bake(self, name):
        data_file_path = join(getcwd(), 'datas', name + '.json')
        self.bake_file(data_file_path, name)
