from datetime import date

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from user.models import UserPrivate, User


class UserPrivateModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):        
        cls.user_data = {
            "email": "email@email.com",
            "password": "123456",
            "extra_info": "extra text",
            "phone_list": ["(47)99999-9999"]
        }

        cls.user = User.objects.create_user(**cls.user_data)

        cls.data = {
            "user": cls.user,
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
        self.assertRaises(IntegrityError, UserPrivate.objects.create, **self.data)


    def test_invalid_cpf(self):
        users = [
            User.objects.create(email=f"email{i}@email.com", password=self.user_data["password"], phone_list=self.user_data["phone_list"])
        for i in range(5)]

        self.data["cpf"] = "306.254.720-0"
        self.data["user"] = users[0]
        self.assertRaises(ValidationError, UserPrivate.objects.create(**self.data).full_clean)
        
        self.data["cpf"] = "306.254.720-022"
        self.data["user"] = users[1]
        self.assertRaises(ValidationError, UserPrivate.objects.create(**self.data).full_clean)

        self.data["cpf"] = "30625472004"
        self.data["user"] = users[2]
        self.assertRaises(ValidationError, UserPrivate.objects.create(**self.data).full_clean)

        self.data["cpf"] = "30602540720004"
        self.data["user"] = users[3]
        self.assertRaises(ValidationError, UserPrivate.objects.create(**self.data).full_clean)

        """
            CPF must validate like the equation found on https://www.calculadorafacil.com.br/computacao/validar-cpf
        """
        self.data["user"] = users[4]
        self.data["cpf"] = "306.254.720-03"
        self.assertRaises(ValidationError, UserPrivate.objects.create(**self.data).full_clean)

    
