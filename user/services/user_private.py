import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Validator:
    @staticmethod
    def cpf(cpf):
        regex = r'[0-9]{3}.[0-9]{3}.[0-9]{3}-[0-9]{2}'
        if not cpf:
            raise ValidationError(
                _('Cpf must be provided in the body'),
            )
        
        if not re.fullmatch(regex, cpf):
            raise ValidationError(
                _('%(value)s must follow the format xxx.xxx.xxx-xx.'),
                params={'value': cpf},
            )

        if not Validator.__is_cpf_digits_valid(cpf):
            raise ValidationError(
                _('%(value)s this is an invalid combination for cpf'),
                params={'value': cpf},
            )

    
    @classmethod
    def __is_cpf_digits_valid(cls, cpf):
        cpf_value = ''.join(cpf[:11].split('.'))
        digits = cpf[12:]

        digits_to_verify = ''
        digits_to_verify += cls.__calculate_cpf_digit(cpf_value)
        digits_to_verify += cls.__calculate_cpf_digit(cpf_value)
        return digits == digits_to_verify
            

    @classmethod
    def __calculate_cpf_digit(cls, cpf_splitted):
        sum_digits = 0
        for i in range(9, 0, -1):
            sum_digits += int(cpf_splitted[i - 10]) * i

        rest = sum_digits % 11
        digit = None

        if rest < 2:
            digit = 0
        else:
            digit = 11 - rest
        
        return str(digit)
