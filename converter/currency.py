from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    if cur_from != 'RUR':
        params = {
            'date_req': date
        }
        response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp',
                                params=params)  # Использовать переданный requests
        text = BeautifulSoup(response.content, 'xml')
        nominal = ''
        value = ''
        for v in text.find_all('Valute'):
            if v.CharCode.text == cur_from:
                nominal = Decimal(v.Nominal.text)
                value = v.Value.text.replace(',', '.')
        amount = Decimal(amount) * Decimal(value) / nominal
    params = {
        'date_req': date
    }
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp',
                            params=params)  # Использовать переданный requests
    text = BeautifulSoup(response.content, 'xml')
    nominal = ''
    value = ''
    for v in text.find_all('Valute'):
        if v.CharCode.text == cur_to:
            nominal = Decimal(v.Nominal.text)
            value = v.Value.text.replace(',', '.')
    result = Decimal(amount) * nominal / Decimal(value)
    return result.quantize(Decimal('0.1111'))  # не забыть про округление до 4х знаков после запятой

