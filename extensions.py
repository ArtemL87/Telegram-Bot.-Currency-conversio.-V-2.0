import requests
import json
from config import keys

class APIException(Exception): # собственный класс исключений, наследуемый от Exception
    pass

class CryptoConverter: # обработка ошибок ввода пользователя
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Невожможно перевести одинаковые валюты.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}'
                               f'\nСписок доступных валют /values')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}'
                               f'\nСписок доступных валют /values')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]

        return round(total_base, 3)
