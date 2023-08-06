#
# Potap module by GuillaumeDesforges
#

from os.path import normcase, join
from os import getcwd
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json

class Baker:
    def __init__(self):
        self.env = Environment(
            loader = FileSystemLoader(join(getcwd(), 'templates')),
            autoescape = select_autoescape(['html'])
        )

    def bake(self, name):
        template = self.env.get_template(name+'.html')
        with open(join(getcwd(), 'datas', name+'.json'), 'r') as f:
            data_dict = json.loads(f.read())
        return template.render(data_dict)
