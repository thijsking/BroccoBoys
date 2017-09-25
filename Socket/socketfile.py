import socket

HOST = socket.gethostname()		# Symbolic name, meaning all available interfaces
PORT = 2000  				# Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# Bind socket to local host and port

s.bind((HOST, PORT))
print('Socket now bind')


print('Socket bind complete')

# Start listening on socket
s.listen(10)
print('Socket now listening')

# now keep talking with the client

# wait to accept a connection - blocking call
conn, addr = s.accept()
print('Connected with ' + addr[0] + ':' + str(addr[1]))
# z = bytes('hoi', 'utf8')
# conn.send(z)
data = conn.recv(1024).decode()
print(data)

s.close()