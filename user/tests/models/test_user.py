from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from phone.models import Phone
from user.models import User


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data= {
            "email": "email@email.com",
            "password": "123456",
            "extra_info": "extra text",
            "phone_list": ["(47)99999-9999"]
        }

        cls.user = User.objects.create_user(**cls.data)

    def test_if_an_user_instance_is_created(self):
        self.assertIsNotNone(self.user.id)
    
    
    def test_user_fields(self):
        self.assertIsInstance(self.user.phone_list[0], Phone)

        self.assertIsInstance(self.user.email, str)
        self.assertEqual(self.user.email, self.data["email"])

        self.assertIsInstance(self.user.password, str)
        self.assertNotEqual(self.user.password, self.data["password"])

        self.assertIsInstance(self.user.extra_info, str)
        self.assertEqual(self.user.extra_info, self.data["extra_info"])


    def test_invalids_emails(self):
        self.data["email"] = "email.email.com"
        self.assertRaises(ValidationError, User.objects.create_user, **self.data)

        self.data["email"] = "@email.com"
        self.assertRaises(ValidationError, User.objects.create_user, **self.data)

        self.data["email"] = "email@emailcom"
        self.assertRaises(ValidationError, User.objects.create_user, **self.data)

        self.data["email"] = "email@.com"
        self.assertRaises(ValidationError, User.objects.create_user, **self.data)


    def test_email_unique_field(self):
        self.assertRaises(IntegrityError, User.objects.create_user, **self.data)
