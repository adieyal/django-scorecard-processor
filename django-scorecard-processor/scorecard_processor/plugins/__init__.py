from register import plugins_as_choices
import os

for root, dirs, files in os.walk(os.path.dirname(__file__)):
    for name in files:
        if name.endswith(".py") and not name.startswith("__"):
            path = os.path.join(root, name)
            __import__(name.split('.')[0],globals(),locals(),['.'])
