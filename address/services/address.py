import re
import requests

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ..models.state import State
from ..models.city import City
from ..static.state import STATES_FROM_UF

class Validator:
    @staticmethod
    def zip_code(value):
        if not re.fullmatch(r'([0-9]{5}-[0-9]{3}|[0-9]{8})', value):
            raise ValidationError(
                _('%(value)s should follow the format xxxxx-xxx or xxxxxxxx'),
                params={'value': value},
            )
        
        return "".join(value.split("-"))
    
class AdressServices:
    @staticmethod
    def get_data_from_zip_code(data):
        zip_code = Validator.zip_code(data.zip_code)
        request = requests.get(f"https://viacep.com.br/ws/{zip_code}/json/")
        request_data = request.json()

        data.street = request_data.get("logradouro")
        data.district = request_data.get("bairro")
        data.street = request_data.get("logradouro")
        data.zip_code = request_data.get("cep")
        
        uf = request_data.get("uf")

        data.state, _ = State.objects.get_or_create(state=STATES_FROM_UF[uf][0], uf=uf, uf_code=STATES_FROM_UF[uf][1])
        data.city, _ = City.objects.get_or_create(state=data.state, city=request_data.get("localidade"), ibge=request_data.get("ibge"))

        return data
        
