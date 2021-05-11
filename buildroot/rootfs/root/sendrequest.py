import requests

url = 'https://192.168.1.13:4717/TempDatas/Create'

params = dict(
    origin='Chicago,IL',
    destination='Los+Angeles,CA',
    waypoints='Joplin,MO|Oklahoma+City,OK',
    sensor='false'
)

resp = requests.get(url=url, params=params, verify=False)
data = resp.json() # Check the JSON Response Content documentation below
