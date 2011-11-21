from collections import defaultdict, namedtuple
from django.forms import CharField

plugins_register = {'input':{},'process':{},'output':{}}

PluginTuple = namedtuple('PluginTuple',['category','plugin'])
def register(plugin_type, plugin_sub_type, name, klass):
    plugins_register[plugin_type][name] = PluginTuple(category=plugin_sub_type, plugin=klass)

def plugin_dict(plugin_type):
    choices = defaultdict(list)
    for name, plugin in plugins_register[plugin_type].items():
        choices[plugin.category].append((name, plugin.plugin.name)) #TODO: Add nicer name in plugin?
    return choices.items()

def input_plugins_as_choices():
    return plugin_dict('input')

def output_plugins_as_choices():
    return plugin_dict('output')

def process_plugins_as_choices():
    return plugin_dict('process')

def get_output_plugin(name):
    return plugins_register['output'][name]

def get_process_plugin(name):
    return plugins_register['process'][name]

def get_input_plugin(name, default=PluginTuple('choice',CharField)):
    return plugins_register['input'].get(name, default)
