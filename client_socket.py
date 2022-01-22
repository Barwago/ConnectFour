import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

Host= socket.gethostname() #En annen pc (UR roboten senere)
Port= 1234 
#Socket is the end point that recives data
#We send and recive data with socket

client.connect((Host, Port)) #Socket oppkobling

full_msg = ''

while True:
 msg = client.recv(8)
 if len(msg) <=0:
    break
 full_msg+=msg.decode("utf-8")   
 
print(full_msg)