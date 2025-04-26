# StateField

# Русская документация

Правила переходов между статусами, как правило, являются частью реализаций конечных автоматов, и если нужен именно он, то лучше воспользоваться одной из специальных библиотек. Однако контроль переходов может понадобиться и в более простых случаях. Тогда простое решение предпочтительнее сложного.

## Как устроено поле StateField?

Здесь `StateField` реализован на базе `CharField` с обязательным указанием `choices` в форме `TextChoices` — они описывают варианты статусов. Единственное, что добавляется в качестве нового параметра поля — это набор правил переходов, который описывается как отдельный объект с простым и понятным интерфейсом. Для взаимодействия в БД не меняется ничего, контроль переходов реализован на уровне приложения. Это позволяет быстро внедрить контроль переходов в существующие проекты.

Пример набора статусов:

```python
class PaymentStates(models.TextChoices):
    START = 'START', 'Init Payment'
    INIT = 'INIT', 'Init data received'
    QR_CODE = 'QR_CODE', 'QR code received',
    SUCCESS = 'SUCCESS', 'Payment successfull'
    FAIL = 'FAIL', 'Payment failed'
```

## Что за правила?

Правило для ограничения состоит из исходного чойса и последовательности допустимых для присваивания после него чойсов (для перехода из состояния в состояние). Если переходы запрещены, то вместо последовательности стоит `None`. Если разрешены любые переходы, то должно быть либо указано значение `[...]`, либо можно просто не создавать на этот чойс никакое правило: если ограничения не указаны, то их и нет. Первый случай (с `[...]`) — если нужна наглядность и однозначность, второй (не определять совсем) — если нужна лаконичность.

Проще говоря, если в правилах указан какой-то статус, переход будет возможен только на те статусы, которые для него определены (при этом, `None` — никакие, а `[...]` — любые).

## Как указывать правила?

Есть несколько способов.

Наиболее предпочтительный — класс `TransitionRule`, который принимает 2 аргумента: `start_state` и `target_states`. Например:

```python
my_rules = [
    TransitionRule(
        start_state = PaymentStates.QR_CODE,
        target_states = [PaymentStates.SUCCESS, PaymentStates.FAILED]
    ),
    TransitionRule(...),
    TransitionRule(...),
]
```

В силу природы класса `Enum` (на основе которого построен класс `TextChoises`), если указать строковые значения вместо констант, всё будет работать. Но константы лучше читаются и с ними удобно работать в IDE.

Вместо `TransitionRule`, тем не менее, возможны разные варианты упрощённой записи (показана в разных возможных вариантах):

```python
my_rules = [
    (PaymentStates.INIT, [...]),
    ('QR_CODE', [PaymentStates.SUCCESS, 'FAILED'])
    (PaymentStates.SUCCESS, None),
    ('FAILED': None),
]
```

То есть, вместо экземпляра класса можно передавать кортеж, а вместо констант указывать их значения. При этом, экземпляры `TransitionRule` могут перечисляться вместе с упрощёнными записями. Однако надо помнить, что упрощённые записи всё равно потом конвертируются в класс `TransitionRule`, и это, хотя и небольшие, но лишние накладные расходы. Поэтому первый способ записи работает быстрее и читается лучше.

## Как работать с полем StatusField?

Декларация поля `StatusField` происходит так же, как и `CharField`, со следующими отличиями:
1. Параметр `choices` не передаётся, вместо него передаётся начальное состояние в параметре `default` — строго в виде экземпляра `TextChoices`. На его основе будут автоматически вычислены параметры `choices` и `max_len`.
2. Можно, тем не менее, передать эти параметры явно, но это ни на что, кроме читаемости, не повлияет.
3. Класс `TextChoices` (в нашем примере это `PaymentStates`) не обязательно должен быть создан за пределами модели, но внутри модели он будет расходовать больше ресурсов (т.к. каждый раз будет заново создаваться, а также занимать память по числу активных экземпляров модели).

Параметр `rules` содержит последовательность правил (как описано выше) и передаётся с остальными параметрами.

```python
class PaymentInfo(models.Model):
        class Meta:
            app_label = 'billing'

        state = StateField(  # type: ignore
            verbose_name='Payment state',
            default=PaymentStates.START,
            rules=my_rules
        )
```

К сожалению, мы вынуждены тут писать `# type: ignore`, потому что сам Django не протипизирован, а если типизировать все возможные варианты `rules`, то линтер сходит с ума.

## Если не передать rules.

Запустится проверка по умолчанию. По ней, все состояния должны меняться строго по порядку от начала к концу одно за другим.

При желании, это поведение можно переопределить и назначить другой дефолтный обработчик. За проверку отвечает класс `StateTransitionsChecker`, и дефолтная логика там реализована в методе `check_default_scenario(self)`. Можно переопределить этот метод в подклассе.

После создания подкласса `StateTransitionsChecker` с новым методом, нужно будет также создать подкласс `StatusField` и назначить новый чекер атрибуту `transitions_checker`:

```python
class MyChecker(StateTransitionsChecker):
    def check_default_scenario(self):
        raise ValueError('Empty rules disallowed!')

class MyStateField(StateField):
    transitions_checker = MyChecker
```

При необходимости, можно написать вообще собственный чекер, если он будет соответствовать `TransitionsCheckerProtocol`. Не знаю, кому и зачем это может быть нужно, но возможность такая есть.

## Что происходит при некорректном переходе?

Срабатывает `ValidationError` из `django.core.exceptions`. Её, поэтому, можно штатно обрабатывать в формах и `clean`-методах модели, в том числе, это будет работать в Django Admin.

## Это не конечный автомат
Потому что он не всегда нужен, когда нужен контроль переходов между состояниями. Если нужен именно конечный автомат, то найдите соответствующую библиотеку в PyPI.

# English Documentation

Transition rules between statuses are typically part of finite state machine implementations, and if that's what's needed, it's better to use one of the specialized libraries. However, transition control might be required in simpler cases, where a simple solution is preferable to a complex one.

## How is the StateField structured?

Here, `StateField` is implemented based on `CharField` with the mandatory specification of `choices` in the form of `TextChoices` — they describe the status options. The only new parameter added is a set of transition rules, described as a separate object with a simple and understandable interface. For database interaction, nothing changes; transition control is implemented at the application level. This allows for quick implementation of transition control in existing projects.

Example of status set:

```python
class PaymentStates(models.TextChoices):
    START = 'START', 'Init Payment'
    INIT = 'INIT', 'Init data received'
    QR_CODE = 'QR_CODE', 'QR code received'
    SUCCESS = 'SUCCESS', 'Payment successful'
    FAIL = 'FAIL', 'Payment failed'
```

## What are the "rules"?

A rule for restriction consists of the initial choice and a sequence of allowed choices that can be assigned after it (for transitioning from one state to another). If transitions are prohibited, use `None` instead of a sequence. If any transitions are allowed, use `[...]` or simply do not create a rule for that choice: if restrictions are not specified, they do not exist. The first case (with `[...]`) is for clarity and unambiguity, the second (not defining at all) is for conciseness.

In simple terms, if a status is specified in the rules, the transition will only be possible to the statuses defined for it (where `None` means none, and `[...]` means any).

## How to specify the rules?

There are several ways.

The most preferred is the `TransitionRule` class, which takes 2 arguments: `start_state` and `target_states`. For example:

```python
my_rules = [
    TransitionRule(
        start_state = PaymentStates.QR_CODE,
        target_states = [PaymentStates.SUCCESS, PaymentStates.FAILED]
    ),
    TransitionRule(...),
    TransitionRule(...),
]
```

Due to the nature of the `Enum` class (on which `TextChoices` is based), string values can be used instead of constants, but constants are more readable and convenient to work with in IDEs.

Instead of `TransitionRule`, simplified notations are possible (shown in different variants):

```python
my_rules = [
    (PaymentStates.INIT, [...]),
    ('QR_CODE', [PaymentStates.SUCCESS, 'FAILED']),
    (PaymentStates.SUCCESS, None),
    ('FAILED': None),
]
```

That is, you can pass a tuple instead of a class instance, and string values instead of constants. Instances of `TransitionRule` can be listed along with simplified entries. However, remember that simplified entries are still converted to `TransitionRule`, which adds some overhead. Therefore, the first method is faster and more readable.

## How to work with the StatusField?

Declaring the `StatusField` field is the same as for `CharField`, with the following differences:
1. The `choices` parameter is not passed; instead, the initial state is passed in the `default` parameter — strictly as an instance of `TextChoices`. Based on it, the `choices` and `max_len` parameters will be automatically calculated.
2. You can still pass these parameters explicitly, but it will only affect readability.
3. The `TextChoices` class (in our example, `PaymentStates`) does not have to be created outside the model, but inside the model it will consume more resources (as it will be created every time and take up memory for each model instance).

The `rules` parameter contains a sequence of rules (as described above) and is passed with the other parameters.

```python
class PaymentInfo(models.Model):
    class Meta:
        app_label = 'billing'

    state = StateField(  # type: ignore
        verbose_name='Payment state',
        default=PaymentStates.START,
        rules=my_rules
    )
```

Unfortunately, we have to write `# type: ignore` here because Django itself is not typed, and typing all possible variants of `rules` would drive the linter crazy.

## If rules are not passed.

The default check will run. According to it, all states must change strictly in order from beginning to end.

If desired, this behavior can be overridden and another default handler assigned. The check is handled by the `StateTransitionsChecker` class, and the default logic is implemented in the `check_default_scenario(self)` method. You can override this method in a subclass.

After creating a subclass of `StateTransitionsChecker` with a new method, you also need to create a subclass of `StatusField` and assign the new checker to the `transitions_checker` attribute:

```python
class MyChecker(StateTransitionsChecker):
    def check_default_scenario(self):
        raise ValueError('Empty rules disallowed!')

class MyStateField(StateField):
    transitions_checker = MyChecker
```

If necessary, you can write your own checker if it complies with `TransitionsCheckerProtocol`. I don't know who might need this, but the option is there.

## What happens with an incorrect transition?

A `ValidationError` from `django.core.exceptions` is triggered. It can be handled normally in forms and model `clean` methods, including in Django Admin.

## This is not a finite state machine
Because it's not always needed when transition control between states is required. If you need a full finite state machine, find the appropriate library on PyPI.
