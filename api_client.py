import httpx


headers = {}
with  httpx.Client(base_url='http://127.0.0.1:8000', headers=headers) as client:
    r = client.get('/addresses/3')
    print(r.text)

