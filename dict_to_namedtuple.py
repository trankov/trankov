
from collections import namedtuple


# Convert dict to named tuple (no recursion, only first level)

to_nt = lambda name, data: namedtuple(name, data.keys())(*data.values())

flat_dict: dict = {'one' : 1, 'two' : 2, 'three' : 3}
converted_dict = to_nt('converted_dict', flat_dict)

print(converted_dict)
print(converted_dict.one, converted_dict.two, converted_dict.three)



# Convert dict to NESTED named tuple (recursion, all levels)

def to_namedtuple(name, dict_data) -> namedtuple:
    return namedtuple(
            name, dict_data.keys()
        )(*(
            to_namedtuple(k, v) 
                if isinstance(v, dict) 
                else v 
            for k, v in dict_data.items()))

nested_dict: dict = {'one' : 1, 'two' : 2, 'three' : {'four' : 4, 'five' : {'six': 6}}}
converted_dict = to_namedtuple('converted_dict', nested_dict)

print(converted_dict)
print(f'{converted_dict.one=}', 
      f'{converted_dict.two=}', 
      f'{converted_dict.three=}',
      f'{converted_dict.three.four=}',
      f'{converted_dict.three.five=}',
      f'{converted_dict.three.five.six=}',
      sep='\n')
