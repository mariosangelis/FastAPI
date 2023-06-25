

import Pyro4
import os
import time
import base64
import serpent
import pymongo
import gridfs
from PIL import Image
import io


mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
mongodb = mongo_client["mydatabase"]
image_collection = mongodb["Images"]

fs = gridfs.GridFS(mongodb)
#Decode image from base64 to bytes using serpent
#image=serpent.tobytes(image)

#Open the image in read-only format.
with open("lake_copy.jpg", 'rb') as f:
    image = f.read()

#binary_file=open("lake_copy.jpg", "wb")
#binary_file.write(image)
fs.put(image, filename="lake_copy.jpg")

image_file = fs.find_one({'filename': "lake_copy.jpg"})

if image_file:
    # Retrieve the image data
    image_data = fs.get(image_file._id).read()

    # Create a PIL image object from the image data
    image = Image.open(io.BytesIO(image_data))

    # Display or process the image as needed
    image.show()

    # Save the image to a file
    image.save('retrieved_image.jpg')

#print(mongodb.list_collection_names())
#print("Successfully created mongodb database...")
