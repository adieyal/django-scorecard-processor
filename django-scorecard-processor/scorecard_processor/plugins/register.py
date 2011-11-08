from collections import defaultdict, namedtuple

plugins_register = {}

PluginTuple = namedtuple('PluginTuple',['category','plugin'])
def register(plugin_type, name, klass):
    plugins_register[name] = PluginTuple(category=plugin_type, plugin=klass)

def plugins_as_choices():
    choices = defaultdict(list)
    for name, plugin in plugins_register.items():
        choices[plugin.category].append((plugin.name, name)) #TODO: Add nicer name in plugin?
    return choices.items()
