import requests


data = requests.post(
    'https://datasend.webpython.graders.eldf.ru/submissions/1/',
    headers={'Authorization': 'Basic YWxsYWRpbjpvcGVuc2VzYW1l'}
).json()

data = requests.put(
    'https://datasend.webpython.graders.eldf.ru/submissions/super/duper/secret/',
    headers={'Authorization': 'Basic Z2FsY2hvbm9rOmt0b3RhbWE='}
).json()

print(data)

