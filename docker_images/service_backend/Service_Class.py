import Pyro4
import os
import time
import base64
import serpent
import pymongo
import gridfs
from pymongo.errors import ConnectionFailure

image_id=0
@Pyro4.expose
class ImageProcessing():

    def __init__(self,database_ip):
        self.image_collection=None
        self.database_ip=database_ip
        self.mongo_client = pymongo.MongoClient(self.database_ip,27017)
        self.mongodb = self.mongo_client["mydatabase"]

        exit=0
        while True:
            try:
                self.mongo_client.admin.command('ismaster')
            except ConnectionFailure:
                print("Database not available")
                continue
            break
        print("Successfully connected to the mongodb database...")

    def get_image(self,id):
        fs = gridfs.GridFS(self.mongodb)
        image_file = fs.find_one({'id': id}).read()

        if image_file:
            print("Successfully retrieved image with id",id,"from mongodb database")
        else:
            return None

        return image_file

    def save_image(self,image):
        global image_id

        exit=0
        while True:
            try:
                self.mongo_client.admin.command('ismaster')
            except ConnectionFailure:
                print("Database not available")
                continue
            break
        print("Successfully connected to the mongodb database...")

        image_id+=1
        #Create a object of GridFs for the above database.
        fs = gridfs.GridFS(self.mongodb)
        #Decode image from base64 to bytes using serpent
        image=serpent.tobytes(image)

        fs.put(image, id=image_id)
        image_file = fs.find_one({'id': image_id})
        if image_file:
            print("Successfully inserted image with id",image_id,"to mongodb database")

        return image_id



