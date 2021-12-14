#This file is used to be able to obtain the IP Address and Hostname of the computer.

#The below function is used to get the Hostname.
import socket
def Getting_HostName():
    hostname = socket.gethostname()
    return hostname

#The below function is used to get the IP Address.
def Getting_IP_Address():
    IP_A = socket.gethostbyname(socket.gethostname())
    return IP_A
