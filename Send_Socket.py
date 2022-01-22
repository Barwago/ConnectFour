import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Host= socket.gethostname() #En annen pc
Port= 1234 
msg=''
#Socket is the end point that recives data
#We send and recive data with socket
server.bind((Host, Port)) #Socket oppkobling

server.listen(5)
clientsocket, address = server.accept() #If anyone tries to connect, we accept
#data = clientsocket.recv(1024)
#print(data.decode('utf-8')) #Til string 
print(f"connection from {address} has been established!")


#Store the clientsocket object and ip adress to adress
msg=input()
clientsocket.send(bytes(msg, "utf-8")) #Send information to clientsocket
clientsocket.close

