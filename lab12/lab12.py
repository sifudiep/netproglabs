# Fråga tills imon
# Vad kommer finnas på tentan? Fokus på Labbarna eller Slides?
# Lab11a, Lab10 och Lab8a har presenterats men inte betygsatts


import tkinter as tk
import tkinter.messagebox as tkmsgbox
import tkinter.scrolledtext as tksctxt

import firebase_admin
from firebase_admin import db

import json

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()


    def create_widgets(self):
    
        #-------------------------------------------------------------------
        # row 1: connection stuff (and a clear-messages button)
        #-------------------------------------------------------------------
        self.groupName = tk.LabelFrame(bd=0)
        self.groupName.pack(side="top")

        self.nameLbl = tk.Label(self.groupName, text="Name", padx=10)
        self.nameLbl.pack(side="left")

        self.nameIn = tk.Entry(self.groupName, width=20)
        self.nameIn.pack(side="left")
        
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

def sendButtonClick():
    # forward to the sendMessage method
    sendMessage(g_app)

# a utility method to print to the message field        
def printToMessages(message):
    g_app.msgText.configure(state=tk.NORMAL)
    g_app.msgText.insert(tk.END, message + '\n')
    # scroll to the end, so the new message is visible at the bottom
    g_app.msgText.see(tk.END)
    g_app.msgText.configure(state=tk.DISABLED)

# if attempt to close the window, it is handled here
def on_closing():
    if tkmsgbox.askokcancel("Quit",
            "You are still connected. If you quit you will be"
            + " disconnected."):
            g_root.destroy()

# attempt to send the message (in the text field g_app.textIn) to the server
def sendMessage(master):
    message = g_app.textIn.get()
    user = g_app.nameIn.get()
    
    global ref
    newMessage = { 'text' : message, 'user' : user}
    ref.child('messages').push(newMessage)


def handleMessage(message):
    printToMessages(f"{message['user']} : {message['text']}")
    

def streamHandler(incomingData):
    if incomingData.event_type == 'put':
        if incomingData.path == '/':
            # This is the very first reading just after subscription:
            # we get all messages or None (if no messages exists).
            if incomingData.data != None:
                for key in incomingData.data:
                    message = incomingData.data[key]
                    handleMessage(message)
        else:
            # Not the first reading.
            # Someone wrote a new message that we just got.
            message = incomingData.data
            handleMessage(message)

databaseURL = "https://lab12-accd6-default-rtdb.europe-west1.firebasedatabase.app/"

cred = firebase_admin.credentials.Certificate("lab12.json")
firebase_admin.initialize_app(cred, {"databaseURL": databaseURL})
ref = firebase_admin.db.reference("/")

newMessage = {'name' : 'Mikael', 'text' : "Hello  again on december 7th, wow."}

g_listenToFirebaseStream = True

g_root = tk.Tk()
g_app = Application(g_root)

# Start listen to stream
ref.child('messages').listen(streamHandler)

# if attempt to close the window, handle it in the on-closing method
g_root.protocol("WM_DELETE_WINDOW", on_closing)

# start the main loop
# (which handles the gui and will frequently call pollMessages)
g_app.mainloop()
