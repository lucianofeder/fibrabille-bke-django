from django.core.exceptions import ValidationError
from django.test import TestCase
from django.db import IntegrityError

from ...models import State

class StateModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = {
            "state": "Santa Catarina",
            "uf": "SC",
            "uf_code": "11"
        }

        cls.state = State.objects.create(**cls.data)
        cls.state.save()
    
    
    def test_if_a_state_instance_is_created(self):
        self.assertIsNotNone(self.state.id)
    

    def test_state_fields(self):
        self.assertIsInstance(self.state.state, str)
        self.assertEqual(self.state.state, self.data["state"])

        self.assertIsInstance(self.state.uf, str)
        self.assertEqual(self.state.uf, self.data["uf"])

        self.assertIsInstance(self.state.uf_code, str)
        self.assertEqual(self.state.uf_code, self.data["uf_code"])
    

    def test_state_field_unique(self):
        state = {
            "state": "Santa Catarina",
            "uf": "PR",
            "uf_code": "12"
        }

        self.assertRaises(IntegrityError, State.objects.create, **state)
    

    def test_uf_field_unique(self):
        state = {
            "state": "Santa Catarina 2",
            "uf": "SC",
            "uf_code": "11"
        }

        self.assertRaises(IntegrityError, State.objects.create, **state)
    

    def test_uf_field_bigger_then_two(self):
        data = {
            "state": "Santa Catari 2",
            "uf": "ZCC",
            "uf_code": "13"
        }

        state = State.objects.create(**data)

        self.assertRaises(ValidationError, state.full_clean)

