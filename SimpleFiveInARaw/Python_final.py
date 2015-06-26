from Tkinter import Tk,Button
from Tkinter import*
import Tkinter as tk
from tkFont import Font
import socket,threading

global is_server

        
class Server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.conn = None
        self.addr = None
        self.client_count = 0





        
       
    def run(self):
        global is_server
        global start
        global board
        print "Server"
        HOST = ''
        PORT = 11111
        s = socket.socket()
        s.bind((HOST,PORT))
        s.listen(1)
        print "123"
        start.txv["text"] = "Waintng for other player join..."
        start.txv["fg"] = 'red'
        self.conn, self.addr = s.accept()
        start.txv["text"] = "Player join , have a nice game!"
        start.txv["fg"] = 'black'
        print "Server start!"
        is_server = 1
        for x,y in start.buttons:
            start.buttons[x,y]["state"] = NORMAL
        print is_server
        while True:
            ##x = raw_input("Input :")
            ##self.conn.send(x)
            ##data = self.conn.recv(1024)
            ##print data
            try:
                data = self.conn.recv(1024)
                if not data:
                        break
                if data == "r":
                    start.block_all()
                    start.reset()
                elif data == "s":
                    start.txv["text"] = "%s win , please click Ok to restart!" %(board.opponent)
                    start.ok_btn["state"] = NORMAL
                else :
                    start.reset_btn["state"] = NORMAL
                    for x,y in start.buttons:
                        if board.field[x,y] == ".":
                            start.buttons[x,y]["state"] = NORMAL
                    start.reset_btn["state"] = NORMAL
                    sdata = data.split(",")
                    start.move(int(sdata[0]),int(sdata[1]))
                    print sdata[0]
                print sdata[1]
            except socket.timeout:
                break
    ##def wait_GUI(self):
    ##    global wg
    ##    wg = Tk()
    ##    wg.title(" ")
    ##    wg.geometry("300x120")

    ##    lab = Label(wg,text = "Wainting for other player...")
    ##    lab.pack()
    ##    wg.mainloop()
            


class Client(threading.Thread):
   def __init__(self):
        self.s = None
        threading.Thread.__init__(self)
   def run(self):
        global is_server
        global start
        global board
        HOST = socket.gethostname()
        PORT = 11111
        self.s = socket.socket()
        try:
            self.s.connect((HOST,PORT))
        except :
            print "No Server"
            self.s.close()
            self.create_server()
            return
        print "Has Server"
        is_server = 0
        print is_server
        while True:
            ##data = s.recv(1024)
            ##x = raw_input("Input:")
            ##s.send(x)
            ##print data
            try:
                data = self.s.recv(1024)
                if not data:
                        break
                if data == "r":
                    start.block_all()
                    start.reset()
                elif data == "s":
                    start.txv["text"] = "%s win , please click Ok to restart!" %(board.opponent)
                    start.ok_btn["state"] = NORMAL
                else :
                    start.reset_btn["state"] = NORMAL
                    for x,y in start.buttons:
                        if board.field[x,y] == ".":
                            start.buttons[x,y]["state"] = NORMAL
                    start.reset_btn["state"] = NORMAL
                    sdata = data.split(",")
                    start.move(int(sdata[0]),int(sdata[1]))
                    print sdata[0]
                    print sdata[1]
            except socket.timeout:
                break        
            
            
   
   def create_server(self):
        global server
        server = Server()
        server.start()

        

class Board:
    
    def __init__(self):
        self.player = "O"
        self.opponent = "X"
        self.empty = "."
        self.size = 5
        self.count = 0
        self.field = {}
        for y in range(self.size):
            for x in range(self.size):
                self.field[x,y] = self.empty
    
    def move(self,x,y):
        self.field[x,y] = self.player
        (self.player,self.opponent)=(self.opponent,self.player)

    def judge(self):
        ## O : O win , X : X win , S : even , N : havn't yet
        for x in range(self.size):
            if self.field[x,0] == self.field[x,1] == self.field[x,2] == self.field[x,3] == self.field[x,4] != self.empty:
                if self.field[x,0] == "O":
                    return "O"
                else:
                    return "X"
        
        for y in range(self.size):
            if self.field[0,y] == self.field[1,y] == self.field[2,y] == self.field[3,y] == self.field[4,y] != self.empty:
                if self.field[0,y] == "O":
                    return "O"
                else:
                    return "X"

        if self.field[0,0] == self.field[1,1] == self.field[2,2] == self.field[3,3] == self.field[4,4] != self.empty:
            if self.field[0,0] == "O":
                return "O"
            else:
                return "X"
        if self.field[0,4] == self.field[1,3] == self.field[2,2] == self.field[3,1] == self.field[4,0] != self.empty:
            if self.field[0,0] == "O":
                return "O"
            else:
                return "X"

        if self.count == 25:
            return "S"

        return "N"


class GUI:
    def __init__(self):
        global board
        global is_server
        self.root = Tk()
        self.root.title("Five In A Row")
        self.root.resizable(width=False,height=False)
        self.font = Font(family = "Helvevtca",size=32)
        board = Board()
        self.buttons = {}
        self.reset_btn = None


        for x,y in board.field:
            handler = lambda x=x,y=y : self.send_to_other(x,y)
            button = Button(self.root,font=self.font,state = DISABLED,command = handler,width = 3 , height = 1)
            button.grid(row = y+1 , column = x)
            self.buttons[x,y] = button
       
        handler = lambda : self.surrender()
        self.reset_btn = Button(self.root,text = "surrender",command = handler,state = DISABLED)
        self.reset_btn.grid(row = board.size +2 , column = 0,columnspan=board.size , sticky = "WE")

        self.txv = Label(self.root,text = "Have a nice game!")
        self.txv.grid(row = 0 , column = 0 , columnspan = board.size , sticky = "WE")

        self.ok_btn = Button(self.root,text = "Ok",state = DISABLED,command = self.ok_click)
        self.ok_btn.grid(row = 8 , column = 0  ,columnspan = board.size , sticky = "WE")

    def surrender(self):
        global board
        if is_server == 1 :
            global server
            server.conn.send("s")
            self.txv["text"] = "%s win , please click Ok to restart!" %(board.opponent)
            self.ok_btn["state"] = NORMAL
        else:
            global client
            client.s.send("s")
            self.txv["text"] = "%s win , please click Ok to restart!" %(board.opponent)
            self.ok_btn["state"] = NORMAL
        self.block_all()
        self.reset_btn["state"] = DISABLED
            

    def ok_click(self):
        self.send_reset()

    def block_all(self):
        for a,b in self.buttons:
                self.buttons[a,b]["state"] = DISABLED
    
    def send_to_other(self,x,y):
        print board.player
        print board.opponent
        self.reset_btn["state"] = DISABLED
        if is_server == 1 :
            global server
            server.conn.send(str(x)+","+str(y))
            self.block_all()
        else:
            global client
            client.s.send(str(x)+","+str(y))
            self.block_all()
       
        self.move(x,y)

    def send_reset(self):
         if is_server == 1 :
            global server
            server.conn.send("r")
            for x,y in self.buttons:
                self.buttons[x,y]["state"] = NORMAL
         else:
            global client
            client.s.send("r")
            for x,y in self.buttons:
                self.buttons[x,y]["state"] = NORMAL
         self.reset()

    def move(self,x,y):
        self.buttons[x,y]["text"] = board.player
        self.buttons[x,y]["state"] = DISABLED
        board.count += 1
        board.move(x,y)
        state = board.judge()
        if(state == "O"):
            self.txv["text"] = "O win , please click Ok to restart!"
            self.ok_btn["state"] = NORMAL
            self.reset_btn["state"] = DISABLED
            print "O win!"
            state = "N"
            self.block_all()
        elif(state == "X"):
            self.txv["text"] = "X win , please click Ok to restart!"
            self.ok_btn["state"] = NORMAL
            self.reset_btn["state"] = DISABLED
            print "X win!"
            state = "N"
            self.block_all()
        elif(state == "S"):
            self.txv["text"] = "Even , please click Ok to restart!"
            self.ok_btn["state"] = NORMAL
            self.reset_btn["state"] = DISABLED
            print "Even"
            state = "N"
            self.block_all()

    def reset(self):
        
        global board
        for x,y in self.buttons:
            self.buttons[x,y]["text"] = " "
        board = Board()
        self.txv["text"] = "Have a nice game!"
        self.ok_btn["state"] = DISABLED

    def mainloop(self):
        self.root.mainloop()
        

if __name__ == '__main__':
    global client
    client = Client()
    client.start()
    
    global start
    start = GUI()
    start.mainloop()

