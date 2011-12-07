class Value(object):
    def __init__(self, item, extractor_class=None):
        if extractor_class:
            self.value = self.extractor_class(item)
        else:
            self.value = item

    def __repr__(self):
        return repr(self.value)

    def __unicode__(self):
        return unicode(self.value)

class Scalar(Value):
    def get_value(self):
        try:
            return self.value.get_value()
        except AttributeError:
            return self.value

    def get_values(self):
        try:
            return self.value.get_value()
        except AttributeError:
            return self.value

class Vector(Value):
    def __init__(self, item, extractor_class=None):
        if extractor_class:
            self.value = self.extractor_class(item)
        else:
            self.value = item

    def __repr__(self):
        return repr(self.value)

    def __unicode__(self):
        return unicode(self.value)

    def get_values(self):
        try:
            return self.value.get_values()
        except AttributeError:
            return self.value
