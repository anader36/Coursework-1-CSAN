import socket
def Getting_HostName():
    hostname = socket.gethostname()
    return hostname

def Getting_IP_Address():
    IP_A = socket.gethostbyname(socket.gethostname())
    return IP_A
