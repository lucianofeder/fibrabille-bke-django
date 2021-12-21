from django.core.exceptions import ValidationError
from django.test import TestCase

from ...models import Address, City


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
