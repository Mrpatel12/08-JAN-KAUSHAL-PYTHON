# import requests
# response = requests.get('https://fakestoreapi.com/products/1')
# print(response.json())



import requests

url="https://fakestoreapi.com/products"

rq=requests.get(url)
data=rq.json()

for i in data:
    print(i["id"])
    print(i["title"])
    print(i["price"])
