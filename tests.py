import unittest
import requests
import json
from converter import CurrencyConverter


class TestConverter(unittest.TestCase):
    
    converter = CurrencyConverter()
        
    def from_currency(self):
        self.assertRaises(ValueError, self.converter.convert, '2', 'DFG', 'EUR')

    def to_currency(self):
        self.assertRaises(ValueError, self.converter.convert, '2', 'USD', 'DFG')  
        
    def amount(self):
        self.assertRaises(TypeError, self.converter.convert, 'r1', 'USD', 'EUR')
        
    def negative_amount(self):
        self.assertRaises(ValueError, self.converter.convert, '-1', 'USD', 'EUR')
        
    def same_currency(self):
        expect_result = {'result': 2.0, 'from_currency': 'EUR', 'amount': 2.0, 'to_currency': 'EUR'}
        self.assertEqual(expect_result, self.converter.convert('2', 'EUR', 'EUR'))
        
class TestConverterAPI(unittest.TestCase):  

    def status_code(self):
        req = requests.get('http://localhost/currency/?type=json')
        self.assertEqual(r.status_code, 200)
        
    def amount(self):
        req = requests.get('http://localhost/currency/?type=json&amount=3w&from_currency=USD&to_currency=EUR')
        data = json.loads(req.text)
        self.assertEqual(data['error'], True)
        
    def negative_amount(self):
        req = requests.get('http://localhost/currency/?type=json&amount=-1&from_currency=USD&to_currency=EUR')
        data = json.loads(req.text)
        self.assertEqual(data['error'], True)

    def from_currency(self):
        req = requests.get('http://localhost/currency/?type=json&amount=-1&from_currency=dfg&to_currency=EUR')
        data = json.loads(req.text)
        self.assertEqual(data['error'], True)

    def to_currency(self):
        req = requests.get('http://localhost/currency/?type=json&amount=1&from_currency=USD&to_currency=dfg')
        data = json.loads(req.text)
        self.assertEqual(data['error'], True)
        
    def same_currency(self):
        expect_result = {'result': 2.0, 'from_currency': 'EUR', 'amount': 2.0, 'to_currency': 'EUR'}
        req = requests.get('http://localhost/currency/?type=json&amount=1&from_currency=EUR&to_currency=EUR')
        data = json.loads(req.text)
        self.assertEqual(data, expect_result)
        

if __name__ == '__main__':
    unittest.main()
