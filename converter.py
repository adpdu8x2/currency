import requests
import os
import json
import time
from django.conf import settings

class CurrencyConverter():
    if not settings.configured:
        settings.configure()
    currency_file_path = '{}/currency.json'.format(settings.MEDIA_ROOT)
    allowed_currency = ['USD', 'EUR', 'CZK', 'PLN']
    
    def __init__(self):
        self.update_currency()
        if not os.path.exists(self.currency_file_path):
            self.update_currency()
        file_creation_time = os.path.getmtime(self.currency_file_path)
        seconds_ago = time.time()-file_creation_time
        if seconds_ago > 86400:
            self.update_currency()
        
    def convert(self, amount, from_currency, to_currency):
        if from_currency not in self.allowed_currency:
            raise ValueError('Wrong parameter "from_currency".')
        if to_currency not in self.allowed_currency:
            raise ValueError('Wrong parameter "to_currency".')
        if not amount:
            raise ValueError('Amount is required.')
        try:
            amount = float(amount)
        except:
            raise TypeError('Amount must be integer or float.')
        if amount <= 0:
            raise ValueError('Amount must be positive.')
        with open(self.currency_file_path, 'r') as f:
            rates = json.loads(f.read())
            if from_currency == 'USD':
                usds = amount
            else:
                usds = amount / rates[from_currency]
            if to_currency == 'USD':
                result = usds
            else:
                result = usds * rates[to_currency]
        return {
            "amount": amount,
            "from_currency": from_currency,
            "to_currency": to_currency,
            "result": round(result, 2)
        }
        
    def update_currency(self):
        req = requests.get('https://openexchangerates.org/api/latest.json?app_id=aa31d145e130462b9c2d973ac307e8ce')
        data = json.loads(req.text)
        rates = data.get('rates')
        if not rates:
            return
        with open(self.currency_file_path, 'w') as f:
            out = {
                "EUR": rates.get("EUR"),
                "CZK": rates.get("CZK"),
                "PLN": rates.get("PLN"),
            }
            json_str = json.dumps(out)
            f.write(json_str)
            f.close()
        
        
        
        
        