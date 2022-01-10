# Convert flat or nested dict to namespace for writing chain notation.
# Be careful, the result is MUTABLE. Use dict_to_namedtuple.py to protect
# converted data from possible changes.


from types import SimpleNamespace


def to_nested_namespace(dict_data: dict) -> SimpleNamespace:
    assert dict_data is not None, 'Parameter passed have to be a valid dict'
    return SimpleNamespace(**dict((k, to_nested_namespace(v))
                if isinstance(v, dict) else (k, v)
            for k, v in dict_data.items()))

  
converted_dict = to_nested_namespace(nested_dict)
print(converted_dict)
print(f'{converted_dict.one=}', 
      f'{converted_dict.two=}', 
      f'{converted_dict.three=}',
      f'{converted_dict.three.four=}',
      f'{converted_dict.three.five=}',
      f'{converted_dict.three.five.six=}',
      sep='\n')
