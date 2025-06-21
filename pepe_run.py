from tkinter import *
from PIL import Image,ImageTk   

windowHeight=600
windowWidth=800

playwidth=windowWidth*0.95
playHeight=windowHeight*0.75

controlHeight=windowHeight*0.19
controlWidth=windowWidth*0.4

def right():
    current=smallpepeLabel.winfo_x()
    if current>=0.85*playwidth:
        print("Pepe cant move more right")
        return
    smallpepeLabel.config(image=smallPepe_right)
    print(f"Pepe moved to right")
    smallpepeLabel.place(x=current+50)

def left():
    current=smallpepeLabel.winfo_x()
    if current<=0.05*playwidth:
        print("Pepe cant move more left")
        return
    smallpepeLabel.config(image=smallPepe_left)
    print(f"Pepe moved to left")
    smallpepeLabel.place(x=current-50)


def up():
    current=smallpepeLabel.winfo_y()
    if current<0.05*playHeight:
        print("Pepe cant move more up")
        return
    
    print(f"Pepe moved up")
    smallpepeLabel.place(y=current-30)

def down():
    current=smallpepeLabel.winfo_y()
    if current>0.75*playHeight:
        print("Pepe cant move more down")
        return
    
    print(f"Pepe moved down")
    smallpepeLabel.place(y=current+30)

window=Tk()
window.geometry(f"{windowWidth}x{windowHeight}")
window.title("Pepe Run")
pepe=PhotoImage(file="assets/pepe.png",height=windowHeight,width=windowWidth)

window.iconphoto(True,pepe)


backgroundimg=Image.open("assets/background_image.png")
resizedBgimg=backgroundimg.resize((windowWidth,windowHeight))
bgimage=ImageTk.PhotoImage(resizedBgimg)
bglabel=Label(image=bgimage)
bglabel.place(x=0,y=0)

#frame for play area
playArea=Frame(window,width=playwidth,height=playHeight,bd=10,relief=RAISED)
playArea.place(x=20,y=20)
#bg for play area
rawpabg=Image.open("assets/playareaBG.png")
resizedpabg=rawpabg.resize((playwidth,playHeight))
playAreaBg=ImageTk.PhotoImage(image=resizedpabg)
playAreaBglabel=Label(playArea,image=playAreaBg)
playAreaBglabel.place(x=0,y=0)


smallPepe_right=PhotoImage(file="assets/small_pepe_right.png")
smallPepe_left=PhotoImage(file="assets/small_pepe_left.png")
smallpepeLabel=Label(playArea,image=smallPepe_right,bd=8,relief=RAISED,padx=10,pady=10,bg="black")
smallpepeLabel.place(x=int(0.05*playwidth),y=int(0.05*playHeight))

#frame for control area
control=Frame(window,width=controlWidth,height=controlHeight,bd=10,relief=SUNKEN,bg="black")
control.place(x=(windowWidth/2-controlWidth/2),y=windowHeight*0.8)

#button config
rightButton=Button(control,text="➡️",font=("Arial",15,"bold"),fg="#00CB0A",bg="#241629",relief=RAISED,bd=5)
leftButton=Button(control,text="⬅️",font=("Arial",15,"bold"),fg="#00CB0A",bg="#241629",relief=RAISED,bd=5)
upButton=Button(control,text="⬆️",font=("Arial",15,"bold"),fg="#00CB0A",bg="#241629",relief=RAISED,bd=5)
downButton=Button(control,text="⬇️",font=("Arial",15,"bold"),fg="#00CB0A",bg="#241629",relief=RAISED,bd=5)

#button placemnet
rightButton.place(x=controlWidth*0.6,y=0.2*controlHeight)
leftButton.place(x=controlWidth*0.25,y=0.2*controlHeight)
upButton.place(x=controlWidth/2.3,y=0.01*controlHeight)
downButton.place(x=controlWidth/2.3,y=0.45*controlHeight)

rightButton.config(command=right)
leftButton.config(command=left)
upButton.config(command=up)
downButton.config(command=down)


window.mainloop()