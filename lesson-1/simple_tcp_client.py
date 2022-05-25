import socket

tagret_host = "0.0.0.0"
target_port = 9997

# create socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connected client
client.connect((tagret_host, target_port))

# send some data
client.send(b"AAABBBCCC")

# getting some data
response = client.recv(4096)

print(response.decode())
client.close()