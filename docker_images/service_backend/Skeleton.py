from Service_Class import *
import base64
import sys
import netifaces as ni

Daemon=0
def main(database_ip):
	global Daemon

	ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

	#Create a Daemon instance. Set also the nat ip and the nat port for port forwarding purposes
	Daemon = Pyro4.Daemon(host=ip,port=9000)
	service_obj=ImageProcessing(database_ip)

	object_id = Daemon.register(service_obj)
	print(object_id)


	print("Create collection PyroIDs")
	id_collection = service_obj.mongodb["PyroIDs"]
	mydict = { "PyroId": str(object_id)}
	x = id_collection.insert_one(mydict)

	Daemon.requestLoop()

if __name__=="__main__":
	main(sys.argv[1])
