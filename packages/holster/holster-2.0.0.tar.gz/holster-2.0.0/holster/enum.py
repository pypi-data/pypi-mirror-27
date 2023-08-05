from collections import OrderedDict

import six


class EnumAttr(object):
    def __init__(self, parent, name, index, value):
        self.parent = parent
        self.name = name
        self.index = index
        self.value = value

    def __eq__(self, other):
        if isinstance(other, EnumAttr):
            return (self.parent == other.parent) and (self.index == other.index)

        return self.value == other

    def __cmp__(self, other):
        if isinstance(other, EnumAttr):
            return self.index - other.index
        return self.value.__cmp__(other)

    def __lt__(self, other):
        if isinstance(other, EnumAttr):
            return self.index < other.index

        return self.index < other

    def __gt__(self, other):
        if isinstance(other, EnumAttr):
            return self.index > other.index

        return self.index > other

    def __le__(self, other):
        if isinstance(other, EnumAttr):
            return self.index <= other.index

        return self.index <= other

    def __ge__(self, other):
        if isinstance(other, EnumAttr):
            return self.index >= other.index

        return self.index >= other

    def __repr__(self):
        return '<EnumAttr {}>'.format(self.name)

    def __str__(self):
        return self.name

    def __int__(self):
        return self.index

    def __hash__(self):
        return hash((self.name, self.index, self.value))


class BaseEnumMeta(type):
    def __getattr__(self, attr):
        if attr.lower() in self._attrs:
            return self._attrs[attr.lower()]
        raise AttributeError

    def __getitem__(self, item):
        return self.get(item)

    def get(self, entry):
        for attr in six.itervalues(self._attrs):
            if attr == entry or attr.name == entry or attr.value == entry:
                return attr

    def add(self, key, value=None):
        self._attrs[key.lower()] = EnumAttr(self, key.lower(), len(self._attrs), value or key)
        return self._attrs[key.lower()]

    @property
    def keys_(self):
        return set(self._attrs.keys())

    @property
    def values_(self):
        return set(i.value for i in six.itervalues(self._attrs))

    @property
    def attrs(self):
        return set(self._attrs.values())


def bitmask_enumerate(seq):
    for i, e in enumerate(seq):
        yield (1 << i), e


def Enum(*args, **kwargs):
    class _T(six.with_metaclass(BaseEnumMeta)):
        pass

    _T._attrs = OrderedDict()

    if args:
        enumer = enumerate
        if kwargs.get('bitmask', True):
            enumer = bitmask_enumerate

        _T._attrs = {e.lower(): EnumAttr(_T, e.lower(), i, e) for i, e in enumer(args)}
    else:
        _T._attrs = {k.lower(): EnumAttr(_T, k.lower(), v, v) for k, v in kwargs.items()}

    return _T
