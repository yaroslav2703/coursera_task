import requests
from decimal import Decimal
from converter.currency import convert


correct = Decimal('3754.8057')
result = convert(Decimal("1000.1000"), 'RUR', 'JPY', "17/02/2005", requests)

print(convert(Decimal("1000.1000"), 'ZAR', 'KRW', "26/02/2018", requests)) # 92628.4452
if result == correct:
    print("Correct")
else:
    print("Incorrect: %s != %s" % (result, correct))
