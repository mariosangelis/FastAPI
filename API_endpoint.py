from typing import Union
from fastapi import FastAPI
import base64
import Pyro4
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    Pyro_ID: str
    image: bytes

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    #Decode the image since Pyro will encode it again to base_64 using serpent
    decoded_image=base64.b64decode(item.image)
    ImageProcessingService=Pyro4.Proxy(item.Pyro_ID)
    ImageProcessingService.save_image(decoded_image)
    return {"item_name": item.name, "item_id": item_id,"Pyro_ID":item.Pyro_ID}



