Извлекает значение из сложносочинённых Python-объектов через цепочку последовательно указанных ключей, атрибутов и индексов.

Например, у нас есть такая структура:

```python
our_structure = {
    'structure_name': 'Some name',
    'Python_objects': [
        some_pydatic_structure,
        wsgi_response,
        {
            'another_dict': 11,
            'and_another': 12,
        }
    ],
}
```

Тут есть всё: словари, списки, объекты с атрибутами. Для навигации по этой структуре нужно использовать различные методы и проверки, и/или обработчики ошибок. Было бы удобно просто по порядку указать ключи, имена атрибутов или целочисленные индексы, и получить конечное значение либо None, если такого пути не существует.

`PullOut` это позволяет. Самое простое — перечислить аргументы для извлечения через запятую. Класс-обработчик сам определит, атрибут это, ключ или индекс:

```python
from pullout import PullOut

another_dict = PullOut('Python_objects', 2, 'another_dict').From(our_structure)
```
В этом случае обработчик пройдёт по структуре `our_structure` и извлечёт значение 11. Он определит, что `'Python_objects'` это ключ словаря, `2` это индекс в списке, а `another_dict` снова ключ.

Так же просто он обработает и атрибуты объектов:

```python
if PullOut(
    'Python_objects', 1, 'status_code'
).From(our_structure) != 200:
    print('Wrong wsgi server response')
```

Как ещё можно передать путь к значению:
- Через точечную нотацию: `'Python_objects.0.foo.bar'`
- Индексы в точечной нотации могут быть в квадратных скобках: `'Python_objects[0].foo.bar'`

Можно прямо указать тип аргумента, что повышает читаемость и не требует автоопределения типа (импортируйте типы из `pullout`):
- `Attr('attribute_name')` - атрибут объекта
- `Key(any_valid_key_object)` - ключ словаря
- `Index(any_valid_index_value)` - индекс последовательности

Все эти варианты можно комбинировать:

`('arg_name.0.key_name[12]', Index(-1), 'arg_name', 'another_name')`

Переиспользование:

```python
get_value = PullOut('json', 'my_value', 0)
extracted_values = [
    get_value.From(response)
    for response
    in wsgi_responses
]
```

Классы-типизаторы способны извлекать значения сами по себе, если использовать их экземпляры как вызываемые объекты и передать в них объект для извлечения:

```python
from pullout import Index


sequence = [1, 2, 3, 4, 5, 100]
first_of, last_of = Index(0), Index(-1)
print(first_of(sequence), last_of(sequence), sep=', ')

>>> 1, 100
```

Примеры есть в документации к классам.
