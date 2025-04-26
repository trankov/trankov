from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase

from ..transitions import (
    StateField,
    StateTransitionsChecker,
    TransitionRule,
    TransitionsFieldError,
    get_transition_rules,
)


class TestStates(models.TextChoices):
    START = 'start', 'Начало'
    MIDDLE = 'middle', 'Середина'
    END = 'end', 'Конец'
    ANY = 'any', 'Любое'


class TestTransitionRule(TestCase):
    def setUp(self) -> None:
        self.rule = TransitionRule(
            start_state=TestStates.START,
            target_states=[TestStates.MIDDLE, TestStates.END],
        )

    def test_allowed_with_valid_target(self):
        self.assertTrue(self.rule.allowed(TestStates.MIDDLE))
        self.assertTrue(self.rule.allowed(TestStates.END))

    def test_allowed_with_invalid_target(self):
        self.assertFalse(self.rule.allowed(TestStates.START))
        self.assertFalse(self.rule.allowed(TestStates.ANY))

    def test_allowed_with_ellipsis(self):
        rule = TransitionRule(start_state=TestStates.START, target_states=[...])
        self.assertTrue(rule.allowed(TestStates.MIDDLE))
        self.assertTrue(rule.allowed(TestStates.END))
        self.assertTrue(rule.allowed(TestStates.ANY))

    def test_allowed_with_none(self):
        rule = TransitionRule(start_state=TestStates.START, target_states=None)
        self.assertFalse(rule.allowed(TestStates.MIDDLE))
        self.assertFalse(rule.allowed(TestStates.END))
        self.assertFalse(rule.allowed(TestStates.ANY))


class TestStateTransitionsChecker(TestCase):
    def setUp(self):
        self.rules = [
            TransitionRule(
                start_state=TestStates.START, target_states=[TestStates.MIDDLE]
            ),
            TransitionRule(
                start_state=TestStates.MIDDLE, target_states=[TestStates.END]
            ),
            TransitionRule(start_state=TestStates.END, target_states=None),
        ]

    def test_valid_transition(self):
        checker = StateTransitionsChecker(
            choices_class=TestStates,
            current_state=TestStates.START,
            new_state=TestStates.MIDDLE,
            rules=self.rules,
        )
        self.assertTrue(checker())

    def test_invalid_transition(self):
        checker = StateTransitionsChecker(
            choices_class=TestStates,
            current_state=TestStates.START,
            new_state=TestStates.END,
            rules=self.rules,
        )
        self.assertFalse(checker())

    def test_final_state_transition(self):
        checker = StateTransitionsChecker(
            choices_class=TestStates,
            current_state=TestStates.END,
            new_state=TestStates.START,
            rules=self.rules,
        )
        self.assertFalse(checker())

    def test_invalid_state_raises_error(self):
        with self.assertRaises(TransitionsFieldError):
            StateTransitionsChecker(
                choices_class=TestStates,
                current_state='invalid_state',  # type: ignore
                new_state=TestStates.MIDDLE,
                rules=self.rules,
            )

    def test_default_scenario(self):
        checker = StateTransitionsChecker(
            choices_class=TestStates,
            current_state=TestStates.START,
            new_state=TestStates.MIDDLE,
            rules=None,
        )
        self.assertTrue(checker())


class TestStateField(TestCase):
    def setUp(self):
        class TestModel(models.Model):
            state = StateField(  # type: ignore
                max_length=10,
                default=TestStates.START,
                rules=[
                    (TestStates.START, [TestStates.MIDDLE]),
                    (TestStates.MIDDLE, [TestStates.END]),
                    (TestStates.END, None),
                ],
            )

            class Meta:
                app_label = 'cycle'

        self.model = TestModel()

    def test_initial_state(self):
        self.assertEqual(self.model.state, TestStates.START)

    def test_valid_transition(self):
        self.model.state = TestStates.MIDDLE
        self.assertEqual(self.model.state, TestStates.MIDDLE)

    def test_invalid_transition_raises_error(self):
        with self.assertRaises(ValidationError):
            self.model.state = TestStates.END

    def test_same_state_transition(self):
        self.model.state = TestStates.START
        self.assertEqual(self.model.state, TestStates.START)

    def test_invalid_state_raises_error(self):
        with self.assertRaises(ValidationError):
            self.model.state = TestStates.ANY


class TestGetTransitionRules(TestCase):
    def test_get_transition_rules(self):
        rules = [
            (TestStates.START, [TestStates.MIDDLE]),
            TransitionRule(
                start_state=TestStates.MIDDLE, target_states=[TestStates.END]
            ),
        ]
        result = get_transition_rules(rules, TestStates)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], TransitionRule)
        self.assertIsInstance(result[1], TransitionRule)
        self.assertEqual(result[0].start_state, TestStates.START)
        self.assertEqual(result[1].start_state, TestStates.MIDDLE)
