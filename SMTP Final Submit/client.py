#These are the list of libraries used to run the client side.
from socket import AF_INET, SOCK_STREAM, socket
from os import getpid
import sys
import IP_Address
from time import sleep

#Function to display the welcome message for the client side.
Ending_Message = "Welcome to my SMTP Client Side. \n This project is done by Ahmed Nader \n  Hope you'll like it and have a good day \n   :) :) :) :) :) :) :) :) :) :) :) :) :) :) :) \n" 

for letter in Ending_Message:
  sleep(0.05) # In seconds
  sys.stdout.write(letter)
  sys.stdout.flush()

#Function used to use the stored variables in another file.
IPA = IP_Address.Getting_IP_Address()

#Setting up the TCP socket to receive.
sock = (IPA,7777)
Server_IPAddress= input("Please enter the SMTP server's IP Address: ")
Server_PortAddress= int(input("Please enter the SMTP server's Port Address: "))
ServerAddress = (Server_IPAddress,Server_PortAddress)

print()
print("The SMTP application (Client Side) has fully started")
print("The OS assigned process ID is :", getpid())
s = socket(AF_INET,SOCK_STREAM)
print("TCP-SMTP Socket has been created successfully")
s.bind(sock)
print("Client Socket is bound to %s:%d" % s.getsockname())
s.connect(ServerAddress)
print('Socket is connected to %s:%d' % s.getpeername())
# check for handshake/connection made 
MacA = s.recv(1024).decode("utf-8")
msg = s.recv(1024).decode("utf-8")
if msg[:3] != '220':
    print('Unable to connect to server. Please try again later.')
    s.close()
    sys.exit()
else:
    print("The server's response is :", msg)
    print("The server's response also is: The client's MAC address is", MacA)
    
# Send HELO command and print server response
heloCommand = 'HELO'
s.send(heloCommand.encode())
print("Helo command has been sent to the server")
recv1 = s.recv(1024).decode("utf-8")
if recv1[:3] != '250':
    print("Unable to connect to server. Please try again later.")
    s.close()
    sys.exit() 
else:
    print("250 (OK) command has been recieved from the server")
x = 0   
while True: 
    # input Sender email (send MAIL FROM command to server)
    while True:
        FromMail = input('\nFrom: ')
        msg ='MAIL FROM: <' + FromMail + '>'
        s.send(msg.encode())
        print()
        print("'MAIL FROM command' has been sent to the server")
        FromOK = s.recv(1024).decode("utf-8")
        if FromOK[:3] != "250":
            print(FromOK)
            print ('Please enter a valid email address.')
            continue
        else:
            print("250 (OK) command has been recieved from the server") 
            break
    # input email recipients separated by comma and space (send RCPT TO command to server)
    while True:
        if x == 1:
            break
        print()
        receiptTo = input('To: ')
        ListTo = receiptTo.split(", ")
        for tos in ListTo: 
            msg = 'RCPT TO: <' + tos + '>'
            s.send(msg.encode())
            print()
            print("'RCPT TO command' has been sent to the server")
            okTo = s.recv(1024).decode("utf-8")
            def toCheck():
                if okTo[:3] != "250":
                    print ("One or more email addresses are invalid. Please re-enter the correct email.")
                    global x
                    x = 0
                    return
                else: 
                    print("250 (OK) command has been recieved from the server")
                    x = 1 
                    return 
            toCheck()
            if x == 0:
                break
    # send data to server
    s.send('DATA'.encode())
    print("'DATA command' has been sent to the server")    
    okData = s.recv(1024).decode("utf-8")
    if okData[:3] != "354":
        print ('There is an error.')
    else:
        print("'354 - Start mail input command' has been recieved from the server")
    # mail transactions - formatting the email
    FromWrite = ('From: ' + FromMail)
    s.send(FromWrite.encode())
    s.recv(1024).decode("utf-8")
    
    ToWrite = ('To: ' + receiptTo)
    s.send(ToWrite.encode())
    s.recv(1024).decode("utf-8")

    print()    
    SubjectRead = input('Subject: ')
    msg= 'Subject: ' + SubjectRead + '\n'
    s.send(msg.encode())
    s.recv(1024).decode("utf-8")
        
    sys.stdout.write('Message: ')
    
    while True:
        # mail body contents 
        DataRead = input()
        if DataRead == '':
            DataRead = '\r'
        s.sendall(DataRead.encode())
        
        okEnd = s.recv(1024).decode("utf-8")
        if okEnd[:3] == '250':
            s.send('QUIT'.encode())
            print("Mail content has been sent to server for analysing process.") 
            print("250 (OK) command has been sent to the server")
            quitMsg = s.recv(1024).decode("utf-8")
            if quitMsg[:3] != '221':
                print ('There was an error. Quitting.')
                sys.exit()
            else:
                print("'221 - Connection closed command' has been recieved from the server")
                s.close()
                sys.exit()
                break
        else:
            continue    
                
                
                
        
        
        
        
