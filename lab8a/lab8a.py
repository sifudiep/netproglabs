
import tkinter as tk
import tkinter.messagebox as tkmsgbox
import tkinter.scrolledtext as tksctxt
from tkinter import END
import socket, select

## fix client connected tries to connect again
## fix port can be input by user

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
    
        #-------------------------------------------------------------------
        # row 1: connection stuff (and a clear-messages button)
        #-------------------------------------------------------------------
        self.groupCon = tk.LabelFrame(bd=0)
        self.groupCon.pack(side="top")
        #
        self.ipPortLbl = tk.Label(self.groupCon, text='IP:port', padx=10)
        self.ipPortLbl.pack(side="left")
        #
        self.ipPort = tk.Entry(self.groupCon, width=20)
        self.ipPort.insert(0, '192.168.1.100:60003')
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) connect
        self.ipPort.bind('<Return>', serverGoUpOrDownClick)
        self.ipPort.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=5)
        padder.pack(side="left")
        #
        self.connectButton = tk.Button(self.groupCon,
            command = serverGoUpOrDownClick, text="Go Up", width=10)
        self.connectButton.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=4)
        padder.pack(side="left")
        #
        self.clearButton = tk.Button(self.groupCon, text='clr msg',
            command = clearButtonClick)
        self.clearButton.pack(side="left")

        
        #-------------------------------------------------------------------
        # row 2: the message field (chat messages + status messages)
        #-------------------------------------------------------------------
        self.msgText = tksctxt.ScrolledText(height=18, width=50,
            state=tk.DISABLED)
        self.msgText.pack(side="top", padx=20)

        
        #-------------------------------------------------------------------
        # row 3: sending messages
        #-------------------------------------------------------------------
        self.groupBroadcast = tk.LabelFrame(bd=0)
        self.groupBroadcast.pack(side="top")
        #
        self.textInLbl = tk.Label(self.groupBroadcast, text='broadcast message', padx=10)
        self.textInLbl.pack(side="left")
        #
        self.textIn = tk.Entry(self.groupBroadcast, width=38)
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) send
        self.textIn.bind('<Return>', broadcastButtonClick)
        self.textIn.pack(side="left")
        #
        padder = tk.Label(self.groupBroadcast, padx=5)
        padder.pack(side="left")
        #
        self.sendButton = tk.Button(self.groupBroadcast, text = 'send to all',
            command = broadcastButtonClick)
        self.sendButton.pack(side="left")

        #-------------------------------------------------------------------
        # row 4: connected clients
        #-------------------------------------------------------------------
        self.groupClients = tk.LabelFrame(bd=0)
        self.groupClients.pack(side="top")
        #
        padder = tk.Label(self.groupClients, padx= 20).pack(side="left")
        #
        self.connectedLbl = tk.Label(self.groupClients, text="connected clients", padx=10)
        self.connectedLbl.pack(side="left")
        #
        self.connectedClientsListbox = tk.Listbox(self.groupClients, width=38)
        self.connectedClientsListbox.pack(side="left")
        #
        self.groupDisconnectButtons = tk.LabelFrame(self.groupClients, bd=0, padx=10)
        self.groupDisconnectButtons.pack(side="left")

        self.disconnectAllButton = tk.Button(self.groupDisconnectButtons, text="disconnect all", command=disconnectAllClientsClick)
        self.disconnectAllButton.pack(side="top")

        padder = tk.Label(self.groupDisconnectButtons, padx= 30).pack(side="top")

        self.disconnectSelectedButton = tk.Button(self.groupDisconnectButtons, text="disconnect selected", command=disconnectSelectedClientClick)
        self.disconnectSelectedButton.pack(side="top")

        #-------------------------------------------------------------------
        # row 5: individual message
        #-------------------------------------------------------------------
        self.groupIndividualMessage = tk.LabelFrame(bd=0)
        self.groupIndividualMessage.pack(side="top")
        #
        self.individualMessageLbl = tk.Label(self.groupIndividualMessage, text="individual message", padx=10)
        self.individualMessageLbl.pack(side="left")
        #
        self.individualMessageInput = tk.Entry(self.groupIndividualMessage, width=38)
        self.individualMessageInput.bind('<Return>', sendMessageToIndividualClick)
        self.individualMessageInput.pack(side="left")

        self.individualMessageButton = tk.Button(self.groupIndividualMessage, text="send to selected", command=sendMessageToIndividualClick)
        self.individualMessageButton.pack(side="left")

        
        # set the focus on the IP and Port text field
        self.ipPort.focus_set()

def addClientToServer(client):
    global g_listOfSockets
    global g_app
    
    g_listOfSockets.append(client)
    g_app.connectedClientsListbox.insert(END, client.getpeername())

def disconnectClientFromServer(peername):
    global g_app
    global g_listOfSockets

    for i in range(1, len(g_listOfSockets)):
        if (g_listOfSockets[i].getpeername() == peername):
            del g_listOfSockets[i]
            g_app.connectedClientsListbox.delete(i-1)
            break

def removeSelectedClientFromServer():
    global g_listOfSockets
    global g_app

    selectedItemText = g_app.connectedClientsListbox.get(g_app.connectedClientsListbox.curselection())

    # Start from index 1 since first item is sockL which is the host
    for i in range(1, len(g_listOfSockets)):
        if (g_listOfSockets[i].getpeername() == selectedItemText):
            del g_listOfSockets[i]
            g_app.connectedClientsListbox.delete(g_app.connectedClientsListbox.curselection())
            break

def removeAllClientsFromServer():
    global g_listOfSockets
    global g_app
    print("removing all clients!!")
    # reversed since deleting first item of list moves 2nd item to first index
    for i in reversed(range(1, len(g_listOfSockets))):
        print(f"index : {i}")
        del g_listOfSockets[i]
        # remove at index (i-1) since gListOfSockets starts from index 1
        g_app.connectedClientsListbox.delete(i-1)


def startServer():
    global g_serverIsUp
    global g_sockL
    global g_listOfSockets
    global g_app

    ipAndPort = g_app.ipPort.get().split(":")

    if (g_serverIsUp == False):
        try:
            g_sockL = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            g_sockL.bind((ipAndPort[0], int(ipAndPort[1])))
            g_sockL.listen(1)

            g_listOfSockets.append(g_sockL)

            g_serverIsUp = True
            g_root.after(g_pollFreq, pollServerRequests)
            clearButtonClick()
            printToMessages("Server is up!")
            g_app.connectButton['text'] = 'Go Down'
        except:
            printToMessages("Server could not be started, most likely because of faulty ip:port")


def pollServerRequests():
    global g_serverIsUp
    global g_listOfSockets

    if (g_serverIsUp):
        g_root.after(g_pollFreq, pollServerRequests)
    else:
        return

    tup = select.select(g_listOfSockets, [], [], 0.0)

    if not tup[0]:
        return

    sock: socket = tup[0][0]

    data = None


    
    if (sock==g_sockL):
        (sockClient, addr) = g_sockL.accept()
        formattedAddr = formatPeerName(str(addr))

        sendMessageToAllClients(f"[{formattedAddr}] (connected)")
        addClientToServer(sockClient)
        print(f"[{formattedAddr}] (connected)")
    else:
        sockPeerName = formatPeerName(str(sock.getpeername()))
        try:
            data = sock.recv(2048)
        except:
            print("Something went wrong...")
            sock = None
            return
        if not data:
            print(f"[{sockPeerName}] (disconnected)")
            sendMessageToAllClients(f"[{sockPeerName}] (disconnected)")
            disconnectClientFromServer(sock.getpeername())
            sock.close()
        else:
            print(f"[{sockPeerName}] {data.decode('utf-8')}")
            sendMessageToAllClients(f"[{sockPeerName}] {data.decode('utf-8')}")

def formatPeerName(name):
    return name.replace("(", "").replace(")", "").replace("'","").replace(", ", ":")

def sendMessageToIndividual():
    global g_app
    global g_listOfSockets

    message = g_app.individualMessageInput.get()
    g_app.individualMessageInput.delete(0, END)

    selectedItemText = g_app.connectedClientsListbox.get(g_app.connectedClientsListbox.curselection())

    # Start from index 1 since first item is sockL which is the host
    for i in range(1, len(g_listOfSockets)):
        if (g_listOfSockets[i].getpeername() == selectedItemText):
            g_listOfSockets[i].send(bytearray("FROM SERVER : " + message, "utf-8"))
            printToMessages(f"SENT TO - [{formatPeerName(str(g_listOfSockets[i].getpeername()))}] : {message}")
            break

def sendMessageToIndividualClick():
    #forward to the sendMessageToIndividual
    sendMessageToIndividual()
    pass

def disconnectAllClientsClick():
    removeAllClientsFromServer()

def disconnectSelectedClientClick():
    removeSelectedClientFromServer()

def clearButtonClick():
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.delete(1.0, tk.END)
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)

def serverGoUpOrDownClick():
    # forward to the connect handler
    serverUpOrDownHandler(g_app)

def broadcastButtonClick():
    # forward to the sendMessage method
    broadcastMessage()

# the connectHandler toggles the status between connected/disconnected
def serverUpOrDownHandler(master):
    global g_serverIsUp
    if g_serverIsUp:
        closeServer()
    else:
        startServer()

# a utility method to print to the message field        
def printToMessages(message):
    global g_app

    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.insert(tk.END, message + '\n')
    # scroll to the end, so the new message is visible at the bottom
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)

# if attempt to close the window, it is handled here
def on_closing():
    global g_serverIsUp

    if g_serverIsUp:
        if tkmsgbox.askokcancel("Quit",
            "You are still connected. If you quit you will be"
            + " disconnected."):
            myQuit()
    else:
        myQuit()

# when quitting, do it the nice way    
def myQuit():
    global g_root

    closeServer()
    g_root.destroy()

# disconnect from server (if connected) and
# set the state of the programm to 'disconnected'
def closeServer():
    # we need to modify the following global variables
    global g_serverIsUp
    global g_sockL
    global g_listOfSockets

    if (g_serverIsUp):
        removeAllClientsFromServer()
        g_serverIsUp = False
        g_sockL = None
        g_listOfSockets = []
        clearButtonClick()
        printToMessages("Server went down!")
        g_app.connectButton['text'] = 'Go Up'



# attempt to send the message (in the text field g_app.textIn) to the serverz
def broadcastMessage():
    global g_app 
    global g_serverIsUp

    if (g_serverIsUp == False): 
        printToMessages("Please connect to a server before sending messages.")
        return
    message = f"SERVER MESSAGE : {g_app.textIn.get()}"
    sendMessageToAllClients(message)

    # your code here
    # a call to g_app.textIn.get() delivers the text field's content
    # if a socket.error occurrs, you may want to disconnect, in order
    # to put the program into a defined state

def sendMessageToAllClients(message):
    if (g_serverIsUp == False):
        printToMessages("Start the the server before broadcasting a message.")
        return

    for socket in g_listOfSockets:
        if (socket != g_sockL):
            socket.send(bytearray(message, "utf-8"))

    printToMessages(message)


# 192.168.1.100:60003
g_sockL = None
g_listOfSockets = []

# by default we are not connected
g_serverIsUp = False

g_pollFreq = 100 # in milliseconds

# launch the gui
g_root = tk.Tk()
g_app = Application(master=g_root)

# make sure everything is set to the status 'disconnected' at the beginning
closeServer()

g_root.after(g_pollFreq, pollServerRequests)

# if attempt to close the window, handle it in the on-closing method
g_root.protocol("WM_DELETE_WINDOW", on_closing)

# start the main loop
# (which handles the gui and will frequently call pollMessages)
g_app.mainloop()