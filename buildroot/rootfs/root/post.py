import requests

url = 'https://192.168.1.13:4717/TempDatas/Create'

myobj = {
    "tempdDataID" : 26,
    "temperature" : 98,
    "x" : 550,
    "y" : 8,
    "time" : "2021-01-04T11:10:20"
    }

x = requests.post(url, json=myobj, verify=False)

