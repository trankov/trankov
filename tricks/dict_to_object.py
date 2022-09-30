# Convert JSON or dict to the object (for using point notation).
#
# USAGE:
# import dict2object
# sugarcube = dict2object.rafinade(json_string_or_dict)
#

import json


def rafinade(stringordict):

    if type(stringordict) is dict:
        stringordict = json.dumps(stringordict)

    class Sugar:
        def __init__(self, /, **kwargs):
            self.__dict__.update(kwargs)
            self._root = list(self.__dict__.keys())[0]

        def __repr__(self):
            keys = sorted(self.__dict__)
            items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
            return f'{type(self).__name__}({", ".join(items)})'

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

    return json.loads(stringordict, object_hook=lambda data: Sugar(**data))


# This method is shorter, but lack some features of above


def chainer(name, dict_):
    ret_val = type(name, (), dict_)

    for prop, value in ret_val.__dict__.items():
        if (
            not prop.startswith("__")
            and not prop.endswith("__")
            and type(value) is dict
        ):
            setattr(ret_val, prop, chainer(prop, value))

    return ret_val


if __name__ == "__main__":

    dict_ = {"User": {"Name": "trankov", "ID": 10, "Gender": {"ID": 1}}}

    n = rafinade(dict_)
    print(
        n,
        n.User,
        n.User.Name,
        n.User.ID,
        n.User.Gender,
        n.User.Gender.ID,
        n.User.Gender.ID._root,
        n.User.Gender._root,
        sep="\n",
    )
    print()

    n = chainer("n", dict_)
    print(n, n.User, n.User.Name, n.User.ID, n.User.Gender, n.User.Gender.ID, sep="\n")
