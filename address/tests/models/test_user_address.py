from django.core.exceptions import ValidationError
from django.test import TestCase

from address.models import user_address

from ...models import UserAddress, Address


#FALTA IMPLEMENTAR RELACAO COM USUARIO E LISTA DE PRODUTOS
class UserAddressModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):        
        cls.instalation = {
            "is_commercial": True,
            "zip_code": "66650-450",
            "number": "03",
            "complement": "Descricao teste",
        }

        cls.charge = {
            "is_commercial": False,
            "zip_code": "63575-970",
            "number": "03",
            "complement": "Descricao teste",
        }

        cls.address_charge = Address.objects.create(**cls.charge)
        cls.address_instalation = Address.objects.create(**cls.instalation)

        cls.data = {
            "address_charge": cls.address_charge,
            "address_instalation": cls.address_instalation,
            "contact": "contato@mail.com",
            "wireless_login": "wifi_login",
            "wireless_password": "wifi_password",
            "onu_login": "onu_login",
            "onu_password": "onu_password"
        }


        cls.user_address = UserAddress.objects.create(**cls.data)


    def test_if_an_user_address_instance_is_created(self):
        self.assertIsNotNone(self.user_address.id)
    
    
    def test_user_address_fields(self):
        self.assertIsInstance(self.user_address.address_charge, Address)

        self.assertIsInstance(self.user_address.address_instalation, Address)

        self.assertIsInstance(self.user_address.contact, str)
        self.assertEqual(self.user_address.contact, self.data["contact"])

        self.assertIsInstance(self.user_address.wireless_login, str)
        self.assertEqual(self.user_address.wireless_login, self.data["wireless_login"])

        self.assertIsInstance(self.user_address.wireless_password, str)
        self.assertEqual(self.user_address.wireless_password, self.data["wireless_password"])

        self.assertIsInstance(self.user_address.onu_login, str)
        self.assertEqual(self.user_address.onu_login, self.data["onu_login"])

        self.assertIsInstance(self.user_address.onu_password, str)
        self.assertEqual(self.user_address.onu_password, self.data["onu_password"])

    
    def test_if_charge_not_sent_must_be_the_same_as_instalation_fields(self):
        data = {
            "address_charge": self.address_charge,
            "contact": "contato@mail.com",
            "wireless_login": "wifi_login",
            "wireless_password": "wifi_password",
            "onu_login": "onu_login",
            "onu_password": "onu_password"
        }

        users_address = UserAddress.objects.create(**data)
        self.assertEqual(user_address.address_charge, user_address.address_instalation)


