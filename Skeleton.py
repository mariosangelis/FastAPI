from Service_Class import *
import base64
import netifaces as ni

Daemon=0
def main():
	global Daemon

	#Create a Daemon instance. Set also the nat ip and the nat port for port forwarding purposes

	ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
	print(ip)  # should print "192.168.100.37"


	Daemon = Pyro4.Daemon(host=ip,port=9000)
	object_id = Daemon.register(ImageProcessing())
	print(object_id)

	Daemon.requestLoop()

if __name__=="__main__":
    main()
