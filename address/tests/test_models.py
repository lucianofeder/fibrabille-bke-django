from django.core.exceptions import ValidationError
from django.db.utils import Error
from django.test import TestCase
from django.db import IntegrityError

from ..models import Address, City, State

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
    

class AdressModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):        
        cls.data = {
            "is_commercial": True,
            "zip_code": "66650-450",
            "number": "03",
            "complement": "Descricao teste",
        }
        cls.address = Address.objects.create(**cls.data)


    def test_if_an_address_instance_is_created(self):
        self.assertIsNotNone(self.address.id)
    
    
    def test_address_fields(self):
        self.assertIsInstance(self.address.is_commercial, bool)
        self.assertEqual(self.address.is_commercial, self.data["is_commercial"])

        self.assertIsInstance(self.address.zip_code, str)
        self.assertEqual(self.address.zip_code, self.data["zip_code"])

        self.assertIsInstance(self.address.street, str)

        self.assertIsInstance(self.address.number, str)
        self.assertEqual(self.address.number, self.data["number"])

        self.assertIsInstance(self.address.complement, str)
        self.assertEqual(self.address.complement, self.data["complement"])

        self.assertIsInstance(self.address.district, str)

        self.assertIsInstance(self.address.city, City)


    def test_zip_code_format(self):
        """
            The zip code can either be sent as xxxxx-xxx or xxxxxxxx and must be saved as xxxxx-xxx
        """
        data = {
            "is_commercial": True,
            "zip_code": "66650450",
            "number": "03",
            "complement": "Descricao teste",
        }

        address = Address.objects.create(**data)

        self.assertEqual(address.zip_code, self.data["zip_code"])
    

    def test_zip_code_field_max_nine_chars(self):
        data = {
            "is_commercial": True,
            "zip_code": "66650-4500",
            "number": "03",
            "complement": "Descricao teste",
        }

        self.assertRaises(ValidationError, Address.objects.create, **data)

    

    def test_zip_code_field_only_numbers(self):
        data = {
            "is_commercial": True,
            "zip_code": "66650-45a",
            "number": "03",
            "complement": "Descricao teste",
        }

        self.assertRaises(ValidationError, Address.objects.create, **data)


    def test_invalid_zip_code(self):
        data = {
            "is_commercial": True,
            "zip_code": "6665450",
            "number": "03",
            "complement": "Descricao teste",
        }

        self.assertRaises(ValidationError, Address.objects.create, **data)



    def test_only_zip_code_sent_must_fetch_from_viacep(self):
        """
            If only the cep is sent in the body requisition the information must be fetched from ViaCep
        """

        data = {
            "zip_code": "89211-170"
        }

        address = Address.objects.create(**data)

        self.assertIsNotNone(address.street)
        self.assertIsNotNone(address.district)
        self.assertIsNotNone(address.city)
