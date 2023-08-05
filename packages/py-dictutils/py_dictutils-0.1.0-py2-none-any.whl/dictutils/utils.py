def getattr_with_default(object, name, default=None):
    if hasattr(object, name):
        return getattr(object, name, default)
    else:
        return default


def deep_getattr(obj, attr, separator='.'):
    return reduce(getattr_with_default, attr.split(separator), obj)
