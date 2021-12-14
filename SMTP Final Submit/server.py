from socket import AF_INET, SOCK_STREAM, socket, gethostname
import IP_Address
import os.path
import re
import sys
from os import getpid
from time import sleep

global boolean
boolean = True
Boolean = True
save_path = 'forward/'

def GetMAC(ip):
    with os.popen("arp -a") as f:
        data = f.read()
    start = data.find(ip)+len(ip)+7
    end = start + 15
    mac_address = data[start:end]
    return mac_address

IPA = IP_Address.Getting_IP_Address()
GHN = IP_Address.Getting_HostName() 

Welcome_Message = "Welcome to my SMTP Server Side. \n This project is done by Ahmed Nader \n  Hope you'll like it and have a good day \n   :) :) :) :) :) :) :) :) :) :) :) :) :) :) :) \n" 

for letter in Welcome_Message:
  sleep(0.05) # In seconds
  sys.stdout.write(letter)
  sys.stdout.flush() 

print("The SMTP application (Server Side) has fully started")
print("The OS assigned process ID is :", getpid())

while True:
    try:
      sock = (IPA,25)  
      s = socket(AF_INET,SOCK_STREAM)
      print("TCP socket has been created successfully.")
      print("The file descriptor asssigned by the OS is :", s.fileno())
      s.bind(sock)
      print("Server Socket is bound to %s:%d" % s.getsockname())
      s.listen(0)
      break
 
    except:
        print("Socket connection error! Please try again.")
        sys.exit()
while Boolean:
    try:
        client_socket, client_address = s.accept()
        msg= "220 Connection is accepted from the following : " + GHN 
        print(msg)
        client_socket.send(GetMAC(client_address[0]).encode())
        client_socket.send(msg.encode())
        print("220 - Service is fully ready, command to be sent to the client")
        print()
        print("The client is connected from %s %d" % client_address)
        print("The client's IP address is :", client_address[0])
        print("The client's Port Number is :", client_address[1])
        print("The client's MAC Address:", GetMAC(client_address[0]))
        print()
        
    except:
        print("A socket connection error has occurred :( .")   
    
    try:
        helo = client_socket.recv(1024).decode("utf-8")
        print("'HELLO command' has been recieved from the client")
        if helo[:4] == "HELO":
            msg=  "250 (OK), Hello " + GHN + "Pleased to meet you."
            client_socket.send(msg.encode())
            print("250 (OK) command has been sent to the client")
            boolean = True
            
    except:
        print("HELO error, Try again!")
        sys.exit()
    while boolean:
        print("Recieving mail from info")
        # recieve MAIL FROM command
        MailFrom= client_socket.recv(1024).decode("utf-8")
        print("'MAIL FROM command' has been recieved from the client")
        # check if command input is out of order
        _check1 = re.match(r'RCPT(\s+|$)TO:', MailFrom)
        _check2 = re.match(r'DATA', MailFrom)
        # reference to check if email input is valid or not
        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        # checks for valid MAIL FROM command 
        valid= re.match(regex, MailFrom[13:])
        if _check1:
            print("503 Bad sequence of commands")  
            client_socket.send('503 Bad sequence of commands'.encode())
            continue
        if _check2:
            print("503 Bad sequence of commands") 
            client_socket.send('503 Bad sequence of commands'.encode())
            continue
        elif not valid:
            print("501 Syntax error in parameters or arguments. Invalid mail.")
            client_socket.send("501 Syntax error in parameters or arguments".encode())
            continue
        else:
            print("MAIL FROM command accepted")
            From = MailFrom.replace("MAIL FROM", "FROM")
            client_socket.send("250 - OK".encode())
            print("250 (OK) command has been sent to the client")
        _bool = True
        to_list = []
        rcpt_list = []

        while boolean:
            #recieve RCPT TO command
            RCPTTo = client_socket.recv(1024).decode("utf-8")
            print("'RCPT TO command' has been recieved from the client")
            # check if command input is out of order
            check = re.match(r'DATA', RCPTTo)
            # if check:
            # _bool=False   
            check2 = re.match(r'MAIL(\s+|$)FROM:' , RCPTTo)            
            # checks for valid RECEIPT TO command 
            rcpt = re.match(regex, RCPTTo[11:])
            if RCPTTo[:7] == 'Subject':
                RCPTTo = 'DATA'
                _bool = False
                continue
            if _bool is False:
                if check:
                    break
                if check2:
                    print('503 Bad sequence of commands')
                    client_socket.send('503 Bad sequence of commands'.encode())
                    continue
            if not rcpt:
                print('501 Syntax error in parameters or arguments')
                client_socket.send('501 Syntax error in parameters or arguments'.encode())
                continue
            else:
                _bool = False
                # make save names from recipients
                name_of_file = RCPTTo.replace("RCPT TO: ", "")
                name_of_file = name_of_file.strip('>')
                name_of_file = name_of_file.split('@', 1)[-1]
                to = RCPTTo.replace("RCPT TO: ", "")
                rcpt_list.append(to)
                save_name = os.path.join(save_path, name_of_file)
                if not os.path.exists(save_path):
                    os.makedirs(save_path)
                file1 = open(save_name+".txt", "a")
                to_list.append(file1)
    
                client_socket.send('250 OK'.encode())
                print("250 (OK) command has been sent to the client.")
                
            # write From and To in files
            '''for files in to_list:
                file1 = files
                size = len(rcpt_list)
                file1.write(From + "\n")
                file1.write("To: ")
                for rcpt in rcpt_list:
                    size = size - 1
                    if size is 0:
                        file1.write(rcpt + "\n")
                    else:
                        file1.write(rcpt + ", ")'''
            while boolean:
                if not check:
                    # receive DATA command
                    DATACommand = client_socket.recv(1024).decode("utf-8")
                    print("DATA command recieved from the client")
                    # check if command input is out of order
                    check = re.match(r'DATA', DATACommand)
                if not check:
                    print("500 Syntax error: command is unrecognized")
                    client_socket.send('500 Syntax error: command is unrecognized'.encode())
                    continue
                else:
                    print("'354 - Start mail input command' has been sent to the client")
                    client_socket.send('354 Start mail input; end with <CRLF>.<CRLF>'.encode())
                while boolean:
                    # receive mail transactions until QUIT      
                    Data = client_socket.recv(1024).decode("utf-8")
                    print("Mail transactions recieved from client")
                    # to stop mail transactions after "."
                    if Data == '.':
                        client_socket.send('250 OK'.encode())
                        print("250 (OK) command has been sent to the client")
                        boolean = False
                        print("Terminating command recieved from the client")
                        for files in to_list:
                            file1 = files
                            file1.close()
                        quitCmd = client_socket.recv(1024).decode("utf-8")
                        if re.match(r'QUIT', quitCmd):
                            print("'221 - Connection closed command' has been sent to the client")
                            client_socket.send('221 Bye'.encode())
                            boolean = False
                            break
                    else:
                        client_socket.send(Data.encode())
                        for files in to_list:
                            file1 = files
                            file1.write(Data + "\n")
                            continue
    break
        
            
            
            
            
