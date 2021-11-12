import socket, select

port = 60003

# 192.168.1.100:60003

sockL = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sockL.bind(("192.168.1.100", port))
sockL.listen(1)

listOfSockets = [sockL]

print(f"Listening on port - {port}")

while True:

    print("server is running")
    tup = select.select(listOfSockets, [], [])
    sock: socket = tup[0][0]

    print("is server blocked?")
    
    
    if (sock==sockL):
        (sockClient, addr) = sockL.accept()
        finalAddr = str(addr).replace("(", "").replace(")", "").replace("'","").replace(", ", ":")
        for _sock in listOfSockets:
                if (_sock != sockL):
                    _sock.send(bytearray(f"[{finalAddr}] (connected)", "utf-8"))
        listOfSockets.append(sockClient)
        print(f"[{finalAddr}] (connected)")
    else:
        sockPeerName = str(sock.getpeername()).replace("(", "").replace(")", "").replace("'","").replace(", ", ":")
        data = sock.recv(2048)

        if not data:
            listOfSockets.remove(sock)
            print(f"[{sockPeerName}] (disconnected)")
            for _sock in listOfSockets:
                if (_sock != sockL):
                    _sock.send(bytearray(f"[{sockPeerName}] (disconnected)", "utf-8"))
            sock.close()
        else:
            print(f"[{sockPeerName}] {data.decode('utf-8')}")
            for _sock in listOfSockets:
                if (_sock != sockL):
                    _sock.send(bytearray(f"[{sockPeerName}] {data.decode('utf-8')}", "utf-8"))
            


