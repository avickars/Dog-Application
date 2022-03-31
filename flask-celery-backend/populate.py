import requests

site = 'http://127.0.0.1:5001/upload/'
filename = '2-min.png'

refresh_token ='htaPxPvGKCPsYkhGZkaKeLMjnFYaYZ'
lost = 0
lat = 49.191855
long = -122.867152

data = {
        'refresh_token': refresh_token,
        'lost': lost,
        'lat': lat,
        'long': long
     }

files = {'image': open('2-min.png','rb').read()}

request = requests.post(site, files=files, data=data)

print(request)