
############################################
# This file gives function getifip() which
# you can use to learn the IP address of the
# first interface whose IP is not 127.0.0.1
# IMPORTANT: you need to run pip install 
# netifaces for this to work.
############################################

# The necessary files
import socket, fcntl, struct
import netifaces

#############################################
# Retrieves the ip of the network card with 
# an IPv4 address that is not 127.0.0.1.
# @return - the string containing the IP 
# address of the network adapter that is not
# if the IP is not 127.0.0.1; returns None
# if no such interface is detected
##############################################
def getifip():

	# Get all the network interfaces on the system
	networkInterfaces = netifaces.interfaces()
	
	# The IP address
	ipAddr = None
	
	# Go through all the interfaces
	for netFace in networkInterfaces:
		
		# The IP address of the interface
		addr = netifaces.ifaddresses(netFace)[2][0]['addr'] 
		
		# Get the IP address
		if not addr == "127.0.0.1":
			
			# Save the IP addrss and break
			ipAddr = addr
			break	 
			
	return ipAddr


print getifip()	

#print("The ip of the current system is: " + getifip(b"eth0"))
