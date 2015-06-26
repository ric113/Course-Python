from Tkinter import*
from random import randint, sample, choice


class IDgenerator(Frame):
    genderischoice = 0
    cityischoice = 0
    alpha='Z'
    gender=-1

    def __init__(self,master=None):
        global genderischoice
        genderischoice = 0
        global cityischoice
        cityischoice = 0
        Frame.__init__(self,master)
        self.grid()
        self.createWidgets()
        
    def createWidgets(self):
        self.Text1 = Label(self,text="Generate ID randomly :")
        self.Text1.grid(row=0, column=0)

        self.Text2 = Label(self,text="Gender :",fg="brown")
        self.Text2.grid(row=2, column=0)

        self.Text3 = Label(self,text="City :",fg="brown")
        self.Text3.grid(row=3, column=0)
        

        self.idText = Label(self)
        self.idText.grid(row=0 , column=1 , columnspan = 2)

        self.generateButton = Button(self,text="Generate id!",command=self.generateMethod,fg="red")
        self.generateButton.grid(row = 1 , column=0 )

        self.clearButton = Button(self,text="Clear",command=self.clearMethod,fg="red")
        self.clearButton.grid(row = 1 , column=1)
      
        self.manButton = Button(self,text="Man",command=self.manMethod)
        self.manButton.grid(row = 2 , column=1 ,sticky=N+E+W+S,padx=5,pady=5)

        self.womenButton = Button(self,text="Women",command=self.womenMethod)
        self.womenButton.grid(row = 2 , column=2,sticky=N+E+W+S,padx=5,pady=5)
        
        self.taoyuanButton = Button(self,text="Taoyuan",command=self.taoMethod)
        self.taoyuanButton.grid(row = 3 , column=1,sticky=N+E+W+S)
       
        self.taichungButton = Button(self,text="Taichung",command=self.taiMethod)
        self.taichungButton.grid(row = 3 , column=2,sticky=N+E+W+S)
     
        self.hsinchuButton = Button(self,text="Hsinchu",command=self.hsiMethod)
        self.hsinchuButton.grid(row = 3 , column=3,sticky=N+E+W+S)
        
        self.hualienButton = Button(self,text="Hualien",command=self.huaMethod)
        self.hualienButton.grid(row = 4 , column=1,sticky=N+E+W+S)
        
        self.changhuaButton = Button(self,text="Changhua",command=self.chaMethod)
        self.changhuaButton.grid(row = 4 , column=2,sticky=N+E+W+S)
        
        self.pingtungButton = Button(self,text="Pingtung",command=self.pinMethod)
        self.pingtungButton.grid(row = 4 , column=3,sticky=N+E+W+S)
        

    def generateMethod(self):
        self.generateid()
    def manMethod(self):
        global gender
        gender=1
        global genderischoice 
        genderischoice = 1
    def womenMethod(self):
        global gender
        gender=2
        global genderischoice
        genderischoice = 1
    def clearMethod(self):
        self.idText["text"] = ""
    def taoMethod(self):
        global alpha
        alpha='H'
        global cityischoice 
        cityischoice = 1
    def taiMethod(self):
        global alpha
        alpha='B'
        global cityischoice
        cityischoice = 1
    def hsiMethod(self):
        global alpha
        alpha='O'
        global cityischoice
        cityischoice = 1
    def huaMethod(self):
        global alpha
        alpha='U'
        global cityischoice
        cityischoice = 1
    def chaMethod(self):
        global alpha
        alpha='N'
        global cityischoice
        cityischoice = 1
    def pinMethod(self):
        global alpha
        alpha='T'
        global cityischoice
        cityischoice = 1

    def generateid(self):
        letter=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
            'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
            'Y', 'Z']
        num=[10, 11, 12, 13, 14, 15, 16, 17, 34, 18, 19, 20, 21, 22, 35,
             23, 24, 25, 26, 27, 28, 29, 32, 30, 31, 33]
        lettertonum=dict(zip(letter, num))
        global alpha
        global cityischoice
        global gender
        global genderischoice
        
        if cityischoice != 1: 
            alpha = choice(letter)
        if genderischoice != 1:
            r = [choice((1, 2))]+sample(range(0, 10), 7)
        else:
            r = [gender]+sample(range(0, 10), 7)
        k = [ v*(8-i) for i,v in enumerate(r) ]
        chk = (lettertonum[alpha]/10)+(lettertonum[alpha]%10*9) + sum(k)
        chk = (10 - (chk % 10)) % 10
        self.idText["text"] = " "+alpha+''.join(map(str, r))+str(chk)
        self.idText["fg"] = "blue"
        genderischoice = 0
        cityischoice = 0
       

        
if __name__ == '__main__':
    root = Tk()
    root.title("ID generator")
    app = IDgenerator(master=root)
    app.mainloop()
        
