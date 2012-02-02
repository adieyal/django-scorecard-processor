from register import input_plugins_as_choices, output_plugins_as_choices, process_plugins_as_choices
from register import get_input_plugin, get_output_plugin, get_process_plugin
from base import Scalar, Vector
import os

base_dir = os.path.dirname(__file__)
chop = len(base_dir)
for root, dirs, files in os.walk(os.path.dirname(__file__)):
    for name in files:
        if name.endswith(".py") and not name.startswith("__"):
            path = os.path.join(root, name)
            modname=path[chop+1:].split('.')[0].replace('/','.')
            __import__(modname,globals(),locals(),['.'])

