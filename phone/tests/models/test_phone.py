from datetime import date

from django.test import TestCase
from django.core.exceptions import ValidationError

from phone.models import Phone


class PhoneModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):        
        cls.data = {
            "phone": "(47)99999-9999"
        }

        cls.phone = Phone.objects.create(**cls.data)
        

    def test_if_a_phone_instance_is_created(self):
        self.assertIsNotNone(self.phone.id)
    

    def test_phone_fields(self):
        self.assertIsInstance(self.phone.phone, str)
        self.assertEqual(self.phone.phone, "99999-9999")

        self.assertIsInstance(self.phone.ddd, str)
        self.assertEqual(self.phone.ddd, "47")


    def test_invalid_phone(self):
        self.data["phone"] = "(47)99999-99999"
        self.assertRaises(ValidationError, Phone.objects.create, **self.data)
        
        self.data["phone"] = "(47)999999-999"
        self.assertRaises(ValidationError, Phone.objects.create, **self.data)

        self.data["phone"] = "(473)9999-9999"
        self.assertRaises(ValidationError, Phone.objects.create, **self.data)

        self.data["phone"] = "(7)99999-99999"
        self.assertRaises(ValidationError, Phone.objects.create, **self.data)

        self.data["phone"] = "(47399999-9999"
        self.assertRaises(ValidationError, Phone.objects.create, **self.data)
    
        self.data["phone"] = "(47)9999999999"
        self.assertRaises(ValidationError, Phone.objects.create, **self.data)

