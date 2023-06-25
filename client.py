# importing the requests library
import requests
from typing import Union
import json
import base64
from pydantic import BaseModel

#----------------------------------------------------------------------------

URL = "http://127.0.0.1:8000/items/"
id=42
URL = URL+str(id)

image=open("lake.jpg", "rb")
f = image.read()
b = base64.encodebytes(f).decode('utf-8')
data = {"name": "lake_image.txt","image":b}
r = requests.put(url = URL, data =json.dumps(data))

# extracting data in json format
data = r.json()
image_id=data['image_id']

#----------------------------------------------------------------------------
URL = "http://127.0.0.1:8000/items/"
id=42
URL = URL+str(id)+"?id="+str(image_id)

r = requests.get(url = URL, params=None)

# extracting data in json format
data = r.json()['data']

data=base64.b64decode(data)
image=open("lake_returned.jpg", "wb")
image.write(data)
