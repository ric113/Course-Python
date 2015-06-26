import socket , tkMessageBox ,thread
from Tkinter import*

##-----------------------------------------------------------------------------------------------------
class Dp(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        ##self.money = 0
        self.label = Label(self,text = "How much you want to deposit:")
        self.label.pack()
        self.entry = Entry(self)
        self.entry.pack()
        self.button = Button(self,text = "Enter",command = self.entcmd)
        self.button.pack()
    def entcmd(self):
        global dpmoney
        global myaccount
        if self.entry.get() == "":
            tkMessageBox.showinfo(message = "No input!")
        else:
            dpmoney = self.entry.get()
            s.send('d:'+myaccount+':'+dpmoney)
            self.destroy()
        ##print dpmoney
        
##------------------------------------------------------------------------------------------------------
class Wd(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        ##self.money = 0
        self.label = Label(self,text = "How much you want to withdraw:")
        self.label.pack()
        self.entry = Entry(self)
        self.entry.pack()
        self.button = Button(self,text = "Enter",command = self.entcmd)
        self.button.pack()
    def entcmd(self):
        global wdmoney
        if self.entry.get() == "":
            tkMessageBox.showinfo(message = "No input!")
        else:
            wdmoney = self.entry.get()
            s.send('w:'+myaccount+':'+wdmoney)
            self.destroy()
##--------------------------------------------------------------------------------------------------------
class Tf(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        ##self.money = 0
        self.grid()

        self.label1 = Label(self,text="Account to transfer in :")
        self.label1.grid(row = 0 , column = 0)
        self.label2 = Label(self,text="Money :")
        self.label2.grid(row = 1 , column = 0)

        self.accountin = Entry(self)
        self.accountin.grid(row = 0 , column = 1)
        self.monin = Entry(self)
        self.monin.grid(row = 1 , column = 1)

        self.entbtn = Button(self,text = "Tranfer" , command = self.tfcmd)
        self.entbtn.grid(row = 2 , column = 1)
    def tfcmd(self):
        global tfaccount
        global tfmoney
        tfaccount = self.accountin.get()
        tfmoney = self.monin.get()
        s.send('t:'+myaccount+':'+tfaccount+':'+tfmoney)
        ##print dpmoney
        self.destroy()
##-----------------------------------------------------------------------------------------------------------
class GUI(Frame):
    def __init__(self,master=None):
        global myaccount
        global balance
        global dpmoney
        global wdmoney
        global tfaccount
        global tfmoney
        
        thread.start_new_thread(self.listen,())
        self.count = 0
        Frame.__init__(self,master)
        self.grid()
        self.createWidgets()
    def listen(self):
        global balance
        print "Hello!"
        while True:
            try:
                data = s.recv(1024)
                dl = data.split(":")
                if dl[0] == "n":
                    balance = dl[1]
                    self.error["text"] = "You don't have enough money , action failed!"
                else:
                    balance = dl[0]
                    self.error["text"] = "Successed!"
                print balance
                self.bal["text"] = "Your balance : %s" % balance
            except socket.timeout:
                print "break!"
                break
    def createWidgets(self):
        self.Text1 = Label(self,text="Your Account :")
        self.Text1.grid(row=0,column=0,padx = 5)
        self.Text2 = Label(self,text="Password :")
        self.Text2.grid(row=1,column=0,padx = 5)
        self.accountinput = Entry(self,width=20)
        self.accountinput.grid(row=0,column=1)
        self.passwordinput = Entry(self,width=20)
        self.passwordinput.grid(row=1,column=1)

        self.enterbtn = Button(self,text="Enter",width=8,bd=4,command = self.entcmd,fg="red")
        self.enterbtn.grid(row=1,column=2,padx = 10)

        self.logoutbtn = Button(self,text="Logout",state = DISABLED,width=8,bd=4,command = self.lgotcmd,fg="red")
        self.logoutbtn.grid(row=3,column=4)

        self.dpbtn = Button(self,text="Deposit",state = DISABLED,width=8,bd=4,command = self.dpcmd,fg="blue")
        self.dpbtn.grid(row=0,column=4)

        self.wdbtn = Button(self,text="Withdraw",state = DISABLED,width=8,bd=4,command = self.wdcmd,fg="blue")
        self.wdbtn.grid(row=1,column=4)

        self.tfbtn = Button(self,text="Transfer",state = DISABLED,width=8,bd=4,command = self.tfcmd,fg="blue")
        self.tfbtn.grid(row=2,column=4)

        self.welcome = Label(self,fg="brown")
        self.welcome.grid(row=2,column=1)
        self.bal = Label(self,fg="brown")
        self.bal.grid(row=3,column=1)
        ##self.noneuse = Label(self,text="    ")
        ##self.noneuse.grid(row=4,column=1)
        self.error = Label(self,fg="red")
        self.error.grid(row=6,column=0,columnspan = 7)
        
    def entcmd(self):
        global myaccount
        global balance
        global ready
        
        self.userinputa = self.accountinput.get()
        self.userinputp = self.passwordinput.get()

        if self.userinputa == "" or self.userinputp == "":
            tkMessageBox.showinfo(message = "Account or Password is blank!")
        elif self.userinputp != "12345":
            self.count = self.count +1
            if self.count == 3:
                tkMessageBox.showinfo(message = "Wrong password , %d times . System Locked , please restart it!" %self.count)
                self.enterbtn["state"] = DISABLED
            else:
                tkMessageBox.showinfo(message = "Wrong password , %d times" %self.count)
        else:
            myaccount = self.userinputa
            s.send('a:'+myaccount)
            self.enterbtn["state"] = DISABLED
            self.logoutbtn["state"] = NORMAL
            self.wdbtn["state"] = NORMAL
            self.dpbtn["state"] = NORMAL
            self.tfbtn["state"] = NORMAL
            self.welcome["text"] = "Welcome %s !" % myaccount
            
            
    def lgotcmd(self):
        self.accountinput.delete(0,200)
        self.passwordinput.delete(0,200)
        self.wdbtn["state"] = DISABLED
        self.dpbtn["state"] = DISABLED
        self.tfbtn["state"] = DISABLED
        self.enterbtn["state"] = NORMAL
        self.logoutbtn["state"] = DISABLED
        self.welcome["text"] = ""
        self.bal["text"] = ""
        self.error["text"] = "Log out successed!"

    def dpcmd(self):
        global balance
        global ready
        Dp()
        
    def wdcmd(self):
        global balance
        global ready
        Wd()
        
    def tfcmd(self):
        global balance
        global ready
        Tf()
##---------------------------------------------------------------------------------------       
if __name__ == '__main__':
    s = socket.socket()
    host = socket.gethostname()
    port = 54321
    s.connect((host,port))
    root = Tk()
    root.title("ATM")
    root.geometry("400x150")
    app = GUI(master=root)
    app.mainloop()
    s.close




