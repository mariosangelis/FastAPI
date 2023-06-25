import Pyro4
import os
import time
import base64
import serpent
import pymongo
import gridfs


@Pyro4.expose
class ImageProcessing():

    def __init__(self):
        self.init=0
        self.mongo_client=None
        self.mongodb=None
        self.image_collection=None



    def save_image(self,image):

        if(self.init==0):
            self.init=1
            self.mongo_client = pymongo.MongoClient("localhost",27017)
            self.mongodb = self.mongo_client["mydatabase"]
            print("Successfully connected to the mongodb database...")

        #Create a object of GridFs for the above database.
        fs = gridfs.GridFS(self.mongodb)
        #Decode image from base64 to bytes using serpent
        image=serpent.tobytes(image)
        #binary_file=open("lake_copy.jpg", "wb")
        #binary_file.write(image)

        fs.put(image, filename="lake_copy.jpg")
        image_file = fs.find_one({'filename': "lake_copy.jpg"})
        if image_file:
            print("Successfully inserted image to mongodb database")

