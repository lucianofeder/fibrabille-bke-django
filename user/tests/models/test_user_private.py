from datetime import date

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from user.models import UserPrivate


class UserPrivateModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):        
        cls.data = {
            "name": "Name",
            "surname": "Surname",
            "birthdate": date.fromisoformat("2000-09-15"),
            "cpf": "306.254.720-04",
            "mother_name": "Nome teste",
            "father_name": "Nome teste",
        }

        cls.user_private = UserPrivate.objects.create(**cls.data)
        

    def test_if_an_user_private_instance_is_created(self):
        self.assertIsNotNone(self.user_private.id)
    

    def test_user_private_fields(self):
        self.assertIsInstance(self.user_private.name, str)
        self.assertEqual(self.user_private.name, self.data["name"])

        self.assertIsInstance(self.user_private.surname, str)
        self.assertEqual(self.user_private.surname, self.data["surname"])

        self.assertIsInstance(self.user_private.birthdate, date)
        self.assertEqual(self.user_private.birthdate, self.data["birthdate"])

        self.assertIsInstance(self.user_private.cpf, str)
        self.assertEqual(self.user_private.cpf, self.data["cpf"])

        self.assertIsInstance(self.user_private.mother_name, str)
        self.assertEqual(self.user_private.mother_name, self.data["mother_name"])

        self.assertIsInstance(self.user_private.father_name, str)
        self.assertEqual(self.user_private.father_name, self.data["father_name"])
    

    def test_cpf_unique_field(self):
        self.assertRaises(IntegrityError, UserPrivate.objects.create_user, **self.data)


    def test_invalid_cpf(self):
        self.data["cpf"] = "306.254.720-0"
        self.assertRaises(ValidationError, UserPrivate.objects.create, **self.data)
        
        self.data["cpf"] = "306.254.720-022"
        self.assertRaises(ValidationError, UserPrivate.objects.create, **self.data)

        self.data["cpf"] = "30625472004"
        self.assertRaises(ValidationError, UserPrivate.objects.create, **self.data)

        self.data["cpf"] = "30602540720004"
        self.assertRaises(ValidationError, UserPrivate.objects.create, **self.data)

        """
            CPF must validate like the equation found on https://www.calculadorafacil.com.br/computacao/validar-cpf
        """
        self.data["cpf"] = "306.254.720-03"
        self.assertRaises(ValidationError, UserPrivate.objects.create, **self.data)

    
