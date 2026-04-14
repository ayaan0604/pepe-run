from tkinter import Label

class Collectible:
    def __init__(self, playArea, text):
        self.text = text
        self.label = Label(playArea,text=text,font=("Arial",30),padx=0,pady=0,bg="black",fg="#CB0AF2")
        self.x = 0
        self.y = 0

