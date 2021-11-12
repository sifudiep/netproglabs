import socket, time, json

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 8080))
sock.listen(5)

# while True:
print('\nlistening...\n')
(socketClient, addr) = sock.accept()
print(f"connection from {addr}")

lines = socketClient.recv(1024).decode('utf-8').split("\r\n")

socketClient.sendall(bytearray("HTTP/1.1 200 ok\n", "ASCII") )
socketClient.sendall(bytearray("\n", "ASCII") )
socketClient.sendall(bytearray("<html><body><h1>Your browser sent the following request:</h1>", "ASCII") )

for line in lines:
    socketClient.sendall(bytearray(f'{line}<br>', "ASCII"))

socketClient.sendall(bytearray("</body></html>\n", "ASCII"))

time.sleep(1)
