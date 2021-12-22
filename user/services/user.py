from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from phone.models import Phone


class UserManager(BaseUserManager):
    def create(self, password=None, **kwargs):
        phone_list = UserServices.create_phones(**kwargs)
        del kwargs["phone_list"]
        user = self.model(**kwargs)
        user.password = make_password(password)
        user.save()
        user.phone_list.set(phone_list)
        return user

    def create_user(self, password=None, **kwargs):
        kwargs['is_superuser'] =  False
        return self.create(password=password, **kwargs)

    def create_superuser(self, password=None, **kwargs):
        kwargs['is_superuser'] = True
        return self.create(password=password, **kwargs)


class Validator:
    @staticmethod
    def phone_list(**kwargs):
        phone_list = kwargs.get("phone_list", None)
        if not phone_list or type(phone_list) is not list or len(phone_list) == 0:
            raise ValidationError(
                _('%(value)s must be a list of phones and contain atleast 1 number'),
                params={'value': phone_list},
            )
        return phone_list


class UserServices:
    @staticmethod
    def create_phones(**kwargs):
        phone_list = Validator.phone_list(**kwargs)
        phone_set = []
        for phone in list(dict.fromkeys(phone_list)):
            phone_set.append(Phone.objects.create(phone=phone))
        return phone_set


