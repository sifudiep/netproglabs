
import tkinter as tk
import tkinter.messagebox as tkmsgbox
import tkinter.scrolledtext as tksctxt
import socket

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
        self.ipPort.insert(tk.END, '192.168.1.100:60003')
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) connect
        self.ipPort.bind('<Return>', connectHandler)
        self.ipPort.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=5)
        padder.pack(side="left")
        #
        self.connectButton = tk.Button(self.groupCon,
            command = connectButtonClick, width=10)
        self.connectButton.pack(side="left")
        #
        padder = tk.Label(self.groupCon, padx=1)
        padder.pack(side="left")
        #
        self.clearButton = tk.Button(self.groupCon, text='clr msg',
            command = clearButtonClick)
        self.clearButton.pack(side="left")

        
        #-------------------------------------------------------------------
        # row 2: the message field (chat messages + status messages)
        #-------------------------------------------------------------------
        self.msgText = tksctxt.ScrolledText(height=15, width=42,
            state=tk.DISABLED)
        self.msgText.pack(side="top")

        
        #-------------------------------------------------------------------
        # row 3: sending messages
        #-------------------------------------------------------------------
        self.groupSend = tk.LabelFrame(bd=0)
        self.groupSend.pack(side="top")
        #
        self.textInLbl = tk.Label(self.groupSend, text='message', padx=10)
        self.textInLbl.pack(side="left")
        #
        self.textIn = tk.Entry(self.groupSend, width=38)
        # if the focus is on this text field and you hit 'Enter',
        # it should (try to) send
        self.textIn.bind('<Return>', sendMessage)
        self.textIn.pack(side="left")
        #
        padder = tk.Label(self.groupSend, padx=5)
        padder.pack(side="left")
        #
        self.sendButton = tk.Button(self.groupSend, text = 'send',
            command = sendButtonClick)
        self.sendButton.pack(side="left")
        
        
        # set the focus on the IP and Port text field
        self.ipPort.focus_set()

def clearButtonClick():
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.delete(1.0, tk.END)
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)

def connectButtonClick():
    # forward to the connect handler
    connectHandler(g_app)

def sendButtonClick():
    # forward to the sendMessage method
    sendMessage(g_app)

# the connectHandler toggles the status between connected/disconnected
def connectHandler(master):
    if g_bConnected:
        disconnect()
    else:
        tryToConnect()

# a utility method to print to the message field        
def printToMessages(message):
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.insert(tk.END, message + '\n')
    # scroll to the end, so the new message is visible at the bottom
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)

# if attempt to close the window, it is handled here
def on_closing():
    if g_bConnected:
        if tkmsgbox.askokcancel("Quit",
            "You are still connected. If you quit you will be"
            + " disconnected."):
            myQuit()
    else:
        myQuit()

# when quitting, do it the nice way    
def myQuit():
    disconnect()
    g_root.destroy()

# utility address formatting
def myAddrFormat(addr):
    return '{}:{}'.format(addr[0], addr[1])



# disconnect from server (if connected) and
# set the state of the programm to 'disconnected'
def disconnect():
    # we need to modify the following global variables
    global g_bConnected
    global g_sock

    if (g_bConnected):
        g_sock = None
        g_bConnected = False
        clearButtonClick()
        printToMessages("Disconnected from server!")

    g_app.connectButton['text'] = 'connect'

    
# attempt to connect to server    
def tryToConnect():
    # we need to modify the following global variables
    global g_bConnected
    global g_sock

    g_sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    g_sock.settimeout(0.1)
    ipAndPort = g_app.ipPort.get().split(':')
    try:
        g_sock.connect((f'{ipAndPort[0]}', int(ipAndPort[1])))
        g_bConnected = True
        g_app.connectButton['text'] = 'disconnect'
        clearButtonClick()
        printToMessages(f"Connected to {ipAndPort[0]}:{ipAndPort[1]}!")
    except:
        printToMessages(f"Could not connect to {ipAndPort[0]}:{ipAndPort[1]}")


    # your code here
    # try to connect to the IP address and port number
    # as indicated by the text field g_app.ipPort
    # a call to g_app.ipPort.get() delivers the text field's content
    # if connection successful, set the program's state to 'connected'
    # (e.g. g_app.connectButton['text'] = 'disconnect' etc.)



# attempt to send the message (in the text field g_app.textIn) to the server
def sendMessage(master):
    if (g_bConnected == False): 
        printToMessages("Please connect to a server before sending messages.")
        return

    try:
        g_sock.sendall(bytearray(master.textIn.get(), "utf-8"))
        master.textIn.delete(0,len(master.textIn.get()))
    except:
        disconnect()

    # your code here
    # a call to g_app.textIn.get() delivers the text field's content
    # if a socket.error occurrs, you may want to disconnect, in order
    # to put the program into a defined state

# poll messages
def pollMessages():
    if (g_bConnected == False):
        g_root.after(g_pollFreq, pollMessages)
        return

    # reschedule the next polling event
    g_root.after(g_pollFreq, pollMessages)
    
    g_sock.settimeout(0)
    try:
        receivedMessage = g_sock.recv(2048).decode("utf-8")
        printToMessages(receivedMessage)
    except:
        pass
    # your code here
    # use the recv() function in non-blocking mode
    # catch a socket.error exception, indicating that no data is available




# by default we are not connected
g_bConnected = False
g_sock = None

# set the delay between two consecutive calls to pollMessages
g_pollFreq = 200 # in milliseconds

# launch the gui
g_root = tk.Tk()
g_app = Application(master=g_root)

# make sure everything is set to the status 'disconnected' at the beginning
disconnect()

# schedule the next call to pollMessages
g_root.after(g_pollFreq, pollMessages)

# if attempt to close the window, handle it in the on-closing method
g_root.protocol("WM_DELETE_WINDOW", on_closing)

# start the main loop
# (which handles the gui and will frequently call pollMessages)
g_app.mainloop()
