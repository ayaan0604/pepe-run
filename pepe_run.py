from tkinter import *
from PIL import Image,ImageTk   
import random
from sound import *

windowHeight=600
windowWidth=900

playwidth=windowWidth*0.95
playHeight=windowHeight*0.75

controlHeight=windowHeight*0.19
controlWidth=windowWidth*0.4

game_running=True

current_collectible=None

maxLives=3
current_lives=maxLives

score=0
speed=100

def random_x():
    return random.random()*(playwidth-100)

def game_over():
    
    global game_running
    game_running=False
    show_game_over()
    score_display.config(text=f"{score}")
    for btn in [upButton,downButton,leftButton,rightButton]:
        btn.config(state='disabled')
    play_gameover_music()

def restart():
    
    global game_running,score,current_collectible,current_lives
    current_collectible.destroy()
    score=0
    update_score(score)
    current_lives=maxLives+1
    update_lives()
    game_running=True
    smallpepeLabel.place(x=random.choice(range(0,int(playwidth))),y=random.choice(range(0,int(playHeight))))
    hide_game_over()
    for btn in [upButton,downButton,leftButton,rightButton]:
        btn.config(state='normal')
    spawn_collectible()
    restart_bgm()


    

def update_lives():
    
    global current_lives
    
    current_lives-=1

    if current_lives==0:
        game_over()

    life_text.config(text="🩷"*current_lives)


def update_score(s):
    score_number.config(text=s)

def destroy_collectible(c:Label):
    c.destroy()
    window.after(50,spawn_collectible)

def get_collectible():
    choice=random.choice(collectibles)
    collectible=Label(playArea,
                      text=choice.cget("text"),
                      font=choice.cget("font"),
                      bg="black",
                      fg="#CB0AF2")
    
    return collectible

def collison(pepe: Label,collectible: Label):
    px,py=pepe.winfo_x() , pepe.winfo_y()
    cx,cy=collectible.winfo_x(), collectible.winfo_y()

    if abs(px-cx)<30 and abs(py-cy)<30:
        destroy_collectible(collectible)
        
        return True

    return False


def fall_collectible(collectible:Label):
    global game_running
    if not game_running:
        return
    
    if collison(smallpepeLabel,collectible):
        global score
        score+=1
        update_score(score)
        collect_sfx()
        return

    current_y=collectible.winfo_y()
    if current_y< playArea.winfo_height():
        collectible.place(y=current_y+5)
        global speed
        playArea.after(speed,fall_collectible,collectible)
    else:
        destroy_collectible(collectible)
        update_lives()
        damageSound()
    
    
    

def spawn_collectible():
    global current_collectible
    current_collectible=get_collectible()
    current_collectible.place(x=random_x(),y=0)
    fall_collectible(current_collectible)
    
def show_game_over():
    game_over_frame.lift()

def hide_game_over():
    game_over_frame.lower()


def right(event=None):
    current=smallpepeLabel.winfo_x()
    if current>=0.85*playwidth:
        
        return
    smallpepeLabel.config(image=smallPepe_right)
    
    smallpepeLabel.place(x=current+50)
    movesound()

def left(event=None):
    current=smallpepeLabel.winfo_x()
    if current<=0.05*playwidth:
       
        return
    smallpepeLabel.config(image=smallPepe_left)
    
    smallpepeLabel.place(x=current-50)
    movesound()


def up(event=None):
    current=smallpepeLabel.winfo_y()
    if current<0.05*playHeight:
        
        return
    
    
    smallpepeLabel.place(y=current-30)
    movesound()

def down(event=None):
    current=smallpepeLabel.winfo_y()
    if current>0.75*playHeight:
       
        return
    
  
    smallpepeLabel.place(y=current+30)
    movesound()

window=Tk()
window.geometry(f"{windowWidth}x{windowHeight}")
window.title("Pepe Run")
pepe=PhotoImage(file="assets/pepe.png",height=windowHeight,width=windowWidth)

window.iconphoto(True,pepe)
window.config(bg="black")

backgroundimg=Image.open("assets/playareaBG.png")
resizedBgimg=backgroundimg.resize((windowWidth,windowHeight))
bgimage=ImageTk.PhotoImage(resizedBgimg)
bglabel=Label(image=bgimage)
#bglabel.place(x=0,y=0)

#frame for play area
playArea=Frame(window,width=playwidth,height=playHeight,bd=10,relief=RAISED)
playArea.place(x=0,y=20)
#bg for play area
rawpabg=Image.open("assets/playareaBG.png")
resizedpabg=rawpabg.resize((int(playwidth-25),int(playHeight-25)))
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

#binding the same to keyboard keys
window.bind("<Left>",left)
window.bind("<Right>",right)
window.bind("<Up>",up)
window.bind("<Down>",down)


#labels for collectibles
c1=Label(playArea,text="🍌",font=("Arial",30),padx=0,pady=0,bg="black",fg="#CB0AF2")
c2=Label(playArea,text="🍉",font=("Arial",30),padx=0,pady=0,bg="black",fg="#CB0AF2")
c3=Label(playArea,text="🍊",font=("Arial",30),padx=0,pady=0,bg="black",fg="#CB0AF2")
c4=Label(playArea,text="🍈",font=("Arial",30),padx=0,pady=0,bg="black",fg="#CB0AF2")
c5=Label(playArea,text="🍇",font=("Arial",30),padx=0,pady=0,bg="black",fg="#CB0AF2")

collectibles=[c1,c2,c3,c4,c5]


#score counter

score_counter=Frame(window,width=200,height=40,bg="black")
score_counter.place(x=0,y=0)
score_text=Label(score_counter,text="Score: ",font=("Komika Axis",15,"bold"),bg="black",fg="yellow")
score_number=Label(score_counter,text="0",font=("Komika Axis",15,"bold"),bg="black",fg="yellow")
score_text.place(x=0,y=0)
score_number.place(x=80,y=0)

#life counter
life_counter=Frame(window,width=100,height=40,bg="black")
life_counter.place(x=windowWidth-100,y=0)
life_text=Label(life_counter,text="🩷"*maxLives,font=("Arial",20),bg="black", fg="red")
life_text.place(x=0,y=0)


#gameoverscreen
game_over_frame=Frame(window,width=500,height=300,bd=10,relief=RAISED)
game_over_frame.place(x=windowWidth/2-250,y=windowHeight/2-200)

gameover_image_raw=Image.open("assets/gameOver.png")

gameover_image_resized=ImageTk.PhotoImage(gameover_image_raw.resize((470,275)))

gameover_popup=Label(game_over_frame,image=gameover_image_resized)

#restart button
restart_button=Button(game_over_frame,
                      text="Restart",
                      bg="#022a14",
                      fg="#28ed38",
                      font=("Lucida Console",15,"bold"),
                      width=15,
                      height=1,
                      bd=0,
                      relief=RAISED)

restart_button.config(command=restart)


#score place
score_display=Label(game_over_frame,text="0",
                    width=10,
                    height=1,
                    font=("Komika Axis",15,"bold"),
                    bg="#151552",
                    fg="white"
                    )

gameover_popup.place(x=0,y=0)
restart_button.place(x=55,y=210)
score_display.place(x=100,y=107)

hide_game_over()


    
if __name__=="__main__":
    play_bgm()
    spawn_collectible()

    window.mainloop()