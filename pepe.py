from tkinter import PhotoImage, Label, RAISED
from sound import DJ


        
    

class Pepe:
    def __init__(self, playArea,screen):
        self.smallPepe_right=PhotoImage(file="assets/small_pepe_right.png")
        self.smallPepe_left=PhotoImage(file="assets/small_pepe_left.png")
        self.playArea = playArea
        self.screen = screen
        self.startX = 0.05*screen.playwidth
        self.startY = 0.05*screen.playHeight
        self.maxLives = 3

        self.smallpepeLabel=Label(self.playArea,image=self.smallPepe_right,bd=8,relief=RAISED,padx=10,pady=10,bg="black")

        self.dj = DJ()
    
    def place(self):
        
        self.smallpepeLabel.place(x=int(self.startX),y=int(self.startY))
    
    def right(self,event=None):
        current=self.smallpepeLabel.winfo_x()
        if current>=0.85*self.screen.playwidth:
            
            return
        self.smallpepeLabel.config(image=self.smallPepe_right)
        
        self.smallpepeLabel.place(x=current+50)
        self.dj.movesound()

        
        

    def left(self, event=None):
        current=self.smallpepeLabel.winfo_x()
        if current<=0.05*self.screen.playwidth:
        
            return
        self.smallpepeLabel.config(image=self.smallPepe_left)
        
        self.smallpepeLabel.place(x=current-50)
        self.dj.movesound()
        


    def up(self, event=None):
        current=self.smallpepeLabel.winfo_y()
        if current<0.05*self.screen.playHeight:
            
            return
        
        
        self.smallpepeLabel.place(y=current-30)
        self.dj.movesound()

    def down(self,event=None):
        current=self.smallpepeLabel.winfo_y()
        if current>0.75*self.screen.playHeight:
        
            return
        
    
        self.smallpepeLabel.place(y=current+30)
        self.dj.movesound()
        
        
