import socket

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 8080))

message = input("Send a message to localhost:80: ")
sock.sendall(bytearray(message, 'ASCII'))
