import requests
import json

url = 'https://data.humdata.org/api/3/action/package_show?id=hotosm_ind_railways'
headers = {'User-Agent': 'Mozilla/5.0'}
try:
    r = requests.get(url, headers=headers, timeout=20)
    print('Status:', r.status_code)
    if r.status_code == 200:
        data = r.json()
        resources = data['result']['resources']
        for res in resources:
            print(f"{res['name']} ({res.get('format')}) -> {res.get('url')}")
except Exception as e:
    print('Error:', e)
