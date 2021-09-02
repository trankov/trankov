# Convert dict to named tuple (no recursion, only first level)

import collections


to_nt = lambda name, data: collections.namedtuple(name, data.keys())(*data.values())

flat_dict: dict = {'one' : 1, 'two' : 2, 'three' : 3}
converted_dict = to_nt('converted_dict', flat_dict)

print(converted_dict)
print(converted_dict.one, converted_dict.two, converted_dict.three)
