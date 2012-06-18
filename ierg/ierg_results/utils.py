def calc_values(value):
    if isinstance(value, basestring):
        if '-' in value:
            values = [float(value) for value in value.split('-')]
            value = sum(values) / len(values)
        elif '<' in value:
            value = float(value.replace('<', '')) / 2
        elif '>' in value:
            value = (float(value.replace('>', '')) + 100) / 2
    return value

