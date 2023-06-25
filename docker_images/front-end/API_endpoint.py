from typing import Union
from fastapi import FastAPI
import base64
import Pyro4
from pydantic import BaseModel
import uvicorn
import sys
import pymongo
from time import sleep
import serpent

app = FastAPI()
PyroId=None

class database_client():

    def __init__(self,database_ip):
        self.database_ip=database_ip
        self.mongo_client = pymongo.MongoClient(self.database_ip,27017)
        self.mongodb = self.mongo_client["mydatabase"]

        exit=0
        while True:
            try:
                self.mongo_client.admin.command('ismaster')
            except ConnectionFailure:
                print("Server not available")
                continue
            break
        print("Successfully connected to the mongodb database...")



class Item(BaseModel):
    name: str
    image: bytes

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
#def read_item(item_id: int, id: Union[str, None] = None):
def read_item(item_id: int,id:int):

    global PyroId
    #Decode the image since Pyro will encode it again to base_64 using serpent
    #decoded_image=base64.b64decode(item.image)

    ImageProcessingService=Pyro4.Proxy(PyroId)
    ret_image=ImageProcessingService.get_image(id)
    #ret_image=serpent.tobytes(ret_image)

    if(ret_image!=None):
        print("Backend service returned requested image")
        ret_image = serpent.tobytes(ret_image)
        ret_image = base64.encodebytes(ret_image).decode('utf-8')
    else:
        print("Image not found in the database")
        return None

    return {"id": id,"data": ret_image}

@app.put("/items/{item_id}")
def update_item(item_id: int,item: Item):
    global PyroId
    #Decode the image since Pyro will encode it again to base_64 using serpent
    decoded_image=base64.b64decode(item.image)
    ImageProcessingService=Pyro4.Proxy(PyroId)
    ret_id=ImageProcessingService.save_image(decoded_image)
    if(ret_id>0):
        print("Backend service returned, image with id",ret_id,"added to the database")

    return {"image_id": ret_id}


def main(database_ip):
    global PyroId
    db_client=database_client(database_ip)
    id_collection = db_client.mongodb["PyroIDs"]
    x = id_collection.find_one()

    while True:
        if x:
            print("found dict",x['PyroId'],"in collection")
            PyroId=x['PyroId']
            break
        else:
            print("Did not find PyroID, poll database again...")
            sleep(1)

    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__=="__main__":
	main(sys.argv[1])






