



Through the docker-compose.yml file, we initiate the following 3 services:

1) MongoDB database running on port 27017
2) service_backend running Pyro daemon on port 9000
3) service_frontend running FastAPI endpoint

First, service_backend polls Mongodb until it is up and running.
This is done through an ImageProcessing object. When the object is ready and the database is up and running, the functions are declared to the Pyro Daemon to be served through RPC calls. Then, the PyroID is stored in a collection called "PyroIDs".

The FastAPI endpoint can receive get and put HTTP requests.
When it is initiated, it polls Mongodb until receiving the PyroID.

1) When it receives a put request, it passes the image to the service_backend through the save_image RPC call.
Then the RPC call is executed and the image is inserted into the database.
It is important to clarify the steps of serialization and type conversion until the image is stored in the database.
First, the client reads the bytes of the image. In order to pass the image to the FastAPI endpoint, the dictionary should be converted to a json string using json.dumps(). For this to
be done, every field of the dictionary should be JSON serializable. For this reason, the image should have been converted to a string before json.dumps() is called. Otherwise, the following error will be shown: TypeError: Object of type bytes is not JSON serializable. For this reason, the client converts the image from bytes to string as follows: b = base64.encodebytes(f).decode('utf-8'). Then, at the endpoint json loads in automatically called so the item argument is already a dictionary.
The endpoint converts the image to bytes (not base64) as follows: decoded_image=base64.b64decode(item.image) and calls the PRC function passing image data as an argument. However, Pyro serializes the object and converts it to dict. To convert the image back to bytes, the service_backend calls: image=serpent.tobytes(image) and then store the image to the db. For each image stored in the db, an id is generated and returned to the client. Then, the client can use this id to retrieve the image.

2) When it receives a get request, it calls the get_image RPC function passing an id as an argument.
The service_backend performs a search of the database to find the image through the received id. It returns the image in bytes to the API endpoint.
The endpoint calls serpent to transform the data from dict to bytes and then returns it to the client over HTTP. Thus, the endpoint creates a dictionary and for this reason, the image should be converted to string through the following function: ret_image=base64.encodebytes(ret_image).decode('utf-8').
Finally, the client decodes again the data calling the following function: data=base64.b64decode(data), and writes the bytes of the image to a file.






