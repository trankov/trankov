from collections.abc import Sequence
from dataclasses import dataclass
from types import EllipsisType
from typing import Protocol

from django.core.exceptions import ValidationError
from django.db import models


__all__ = [
    'TransitionRule',
    'StateField',
    'StateTransitionsChecker',
    'TransitionsCheckerProtocol',
]


class TransitionsFieldError(Exception):
    """Exception for state transition errors"""


type TransitionTargetType = (
    Sequence[str | models.TextChoices] | list[EllipsisType] | None
)
type TransitionRuleType = tuple[str | models.TextChoices, TransitionTargetType]


@dataclass(frozen=True, slots=True)
class TransitionRule:
    """
    Rule for state transition.

    - `start_state` - initial state (TextChoices object)
    - `target_states` - list of allowed target states.

    List of allowed states:
    - `[TextChoices.STATE_1, TextChoices.STATE_2, ...]` (sequence of
      TextChoices elements): only these states are allowed for transition
    - Value `[...]` (ellipsis inside list) - any state is allowed
      for transition
    - `None` - final state (transitions are prohibited)
    """

    start_state: models.TextChoices
    target_states: Sequence[models.TextChoices] | list[EllipsisType] | None

    def allowed(self, target_state: models.TextChoices) -> bool:
        """Checks if the target state is allowed for the transition."""
        if self.target_states is None:
            return False
        if self.target_states == [...]:
            return True
        return target_state in self.target_states


class TransitionRuleAdapter:
    def __init__(
        self, tuple_value: TransitionRuleType, choices_class: type[models.TextChoices]
    ) -> None:
        self.start_state, self.target_states = tuple_value
        self.choices_class = choices_class

    @classmethod
    def blind(
        cls,
        blind_value: TransitionRuleType | TransitionRule,
        choices_class: type[models.TextChoices],
    ) -> TransitionRule:
        if isinstance(blind_value, TransitionRule):
            return blind_value
        return cls(blind_value, choices_class).adapt()

    def _convert_to_valid_type(self, value) -> models.TextChoices:
        if isinstance(value, self.choices_class):
            return value
        if isinstance(value, str):
            return self.choices_class(value)
        raise ValueError(f'Invalid value: {value!r}')

    def adapt(self) -> TransitionRule:
        return TransitionRule(
            start_state=self._convert_to_valid_type(self.start_state),
            target_states=[
                self._convert_to_valid_type(state) for state in self.target_states
            ]
            if self.target_states not in (None, [...])
            else self.target_states
        )


def get_transition_rules(
    rules: Sequence[TransitionRuleType | TransitionRule],
    choices_class: type[models.TextChoices],
) -> list[TransitionRule]:
    return [TransitionRuleAdapter.blind(rule, choices_class) for rule in rules]


class TransitionsCheckerProtocol(Protocol):
    def __init__(
        self,
        choices_class: type[models.TextChoices],
        current_state: models.TextChoices,
        new_state: models.TextChoices,
        rules: Sequence[TransitionRule] | None = None,
    ) -> None: ...

    def check_default_scenario(self) -> bool: ...
    def __call__(self) -> bool: ...


@dataclass(slots=True)
class StateTransitionsChecker:
    """Checks state transitions"""

    choices_class: type[models.TextChoices]
    current_state: models.TextChoices
    new_state: models.TextChoices
    rules: Sequence[TransitionRule] | None = None

    def __post_init__(self) -> None:
        if self.new_state not in self.choices_class:
            raise TransitionsFieldError(
                f'New state {self.new_state!r} is not in the choices class'
            )
        if self.current_state not in self.choices_class:
            raise TransitionsFieldError(
                f'Current state {self.current_state!r} is not in the choices class'
            )

    # To redefine this assign <def check_default_scenario(self) -> bool>
    # to the subclass of StateTransitionsChecker and then assign this subclass
    # to attribute <transitions_checker> of the StateField subclass.
    def check_default_scenario(self) -> bool:
        """
        Checks if the new state follows the current state in order.
        Called if state_checker is not set.
        """
        choices = self.choices_class.names
        new_state_index = choices.index(self.new_state.name)
        current_state_index = choices.index(self.current_state.name)
        return new_state_index - current_state_index == 1

    def __call__(self) -> bool:
        if self.rules is None:
            # если нет правил, то проверяем, чтобы новое состояние следовало
            # за текущим по порядку
            return self.check_default_scenario()
        return all(
            # all([]) == True, т.е. если на элемент нет правил, то переход разрешен
            rule.allowed(self.new_state)
            for rule in self.rules
            if rule.start_state == self.current_state
        )


class StateField(models.CharField):
    """Field for state transitions"""

    transitions_checker: type[TransitionsCheckerProtocol] = StateTransitionsChecker

    def __init__(
        self,
        *args,
        default: models.TextChoices,
        rules: Sequence | None = None,
        **kwargs,
    ) -> None:
        kwargs['default'] = default
        super().__init__(*args, **kwargs)
        self._check_statefield_initials()
        self.rules = get_transition_rules(rules, self.choices_class) if rules else None

    def _check_statefield_initials(self):
        if self.default is None:
            raise ValueError('StateField must have default')
        if not isinstance(self.default, models.TextChoices):
            raise ValueError(
                'StateField default must be a subclass of models.TextChoices'
            )

        self.choices_class = type(self.default)
        self.choices = self.choices_class.choices

        max_choice_length = max(
            len(choice_value) for choice_value in self.choices_class.values
        )
        if self.max_length is None:
            self.max_length = max_choice_length
        elif self.max_length < max_choice_length:
            raise ValueError(
                f'StateField max_length (== {self.max_length}) must be >= than'
                f' the longest choice value length (== {max_choice_length})'
            )

    def contribute_to_class(self, cls, name, **kwargs):
        """Adds property with setter for assignment interception."""
        # fmt: off
        super().contribute_to_class(cls, name, **kwargs)
        setattr(cls, name, property(
            lambda obj: obj.__dict__.get(name),
            # Переопределяем сеттер для дескриптора django.db.models
            lambda obj, value: self._set_value(obj, name, value),
        ))
        # fmt: on

    def _set_value(self, obj, name, value):
        """Validates new value before assignment."""
        old_value = getattr(obj, name, None)
        new_value = self.to_python(value)  # Приводим к строке (как CharField)
        # Вызываем валидатор, только если значение изменилось
        if not self._validate_on_change(old_value, new_value):
            raise ValidationError(
                f'State <{new_value}> cannot be assigned to field "{name}" '
                f'after state <{old_value}>'
            )
        # Присваиваем новое значение
        obj.__dict__[name] = new_value

    def _validate_on_change(self, old_value, new_value) -> bool:
        """Calls validator if value has changed."""
        if old_value is None and new_value == self.default:
            # Default initialization is not validated
            return True
        if old_value == new_value:
            # Nothing has changed
            return True
        checker = self.transitions_checker(
            choices_class=self.choices_class,
            current_state=old_value,
            new_state=new_value,
            rules=self.rules,
        )
        return checker()
