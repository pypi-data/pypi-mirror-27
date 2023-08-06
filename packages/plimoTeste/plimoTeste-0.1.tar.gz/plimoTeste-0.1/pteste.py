import requests

response = requests.get('https://httpbin.org/ip')
print('Seu ip é {0}'.format(response.json()['origin']))

