import socket, time, json

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 8080))
sock.listen(5)

while True:
    print('\nlistening...\n')
    (socketClient, addr) = sock.accept()
    print(f"connection from {addr}")

    line = socketClient.recv(1024).decode('utf-8')
    print(line)