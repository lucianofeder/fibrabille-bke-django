import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Validator:

    @staticmethod
    def phone(phone):
        if not re.fullmatch(r'^\((?:[14689][1-9]|2[12478]|3[1234578]|5[1345]|7[134579])\)(?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$', phone):
            raise ValidationError(
                _('%(value)s should follow the format (xx)xxxxx-xxxx or (xx)xxxx-xxxx'),
                params={'value': phone},
            )
        
        return phone
        
        # '^\([1-9]{2}\)([2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$'

class PhoneServices:

    @staticmethod
    def split_phone(phone):
        return phone[1:3], phone[4:]