from django.test import TestCase

from ...models import Address, City, State

class CityModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.state_data = {
            "state": "Santa Catarina",
            "uf": "SC",
            "uf_code": "11"
        }

        cls.state = State.objects.create(**cls.state_data)

        cls.state.save()

        cls.data = {
            "city": "Joinville",
            "state": cls.state
        }

        cls.data = {
            "city": "Joinville",
            "state": cls.state
        }

        cls.city = City.objects.create(**cls.data)
    

    def test_if_a_city_instance_is_created(self):
        self.assertIsNotNone(self.city.id)
    

    def test_city_fields(self):
        self.assertIsInstance(self.city.city, str)
        self.assertEqual(self.city.city, self.data["city"])
    

    def test_city_state_relationship(self):
        self.assertEqual(self.city.state, self.state)
    
