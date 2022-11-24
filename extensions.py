import requests
import json
from config import keys

class APIException(Exception):
    pass

class Convert:
    @staticmethod
    def get_prise(base,sym, amount):
         try:
             base_key = keys[base]
         except KeyError:
             raise APIException(f"Валюта {base} не найдена!")

         try:
             sym_key = keys[sym.lower()]
         except KeyError:
             raise APIException(f"Валюта {sym} не найдена!")

         if base_key == sym_key:
             raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

         try:
             amount = float(amount)
         except ValueError:
             raise APIException(f'Не удалось обработать количество {amount}!')

         r = requests.get(f"https://api.exchangeratesapi.io/latest?base={base_key}&symbols={sym_key}")
         resp = json.loads(r.content)
         new_price = resp['rates'][sym_key] * amount
         new_price = round(new_price, 3)
         message = f"Цена {amount} {base} в {sym} : {new_price}"
         return message
