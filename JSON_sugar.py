# Convert JSON structure to the object's __dict__.
# Just send the JSON string or Python dictionary
# to get the point-to-point notation
# instead of using node tree syntax
#
# USAGE:
# import JSON_sugar
# sugarcube = JSON_sugar.rafinade(json_string_or_dict)
# 

import json

def rafinade(json_string):
    if type(json_string) == dict:
        json_string = json.dumps(json_string)

    class sugar:
        def __init__(self, /, **kwargs):
            self.__dict__.update(kwargs)
            self._root = list(self.__dict__.keys())[0]
        def __repr__(self):
            keys = sorted(self.__dict__)
            items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
            return "{}({})".format(type(self).__name__, ", ".join(items))
        def __eq__(self, other):
            return self.__dict__ == other.__dict__
      
    return json.loads(json_string, object_hook=lambda d: sugar(**d))




if __name__ == '__main__':
    dict_ = {"User" :{"Name" : "trankov", "ID" : 10, "Gender" : {"ID" : 1}}}
    n = rafinade(dict_)
    print(n.User.Gender._root)
