#from pepe_run import window
from tkinter import *
from PIL import Image,ImageTk

testwindow=Tk()
testwindow.geometry("600x800")

game_over_frame=Frame(testwindow,width=500,height=300)
game_over_frame.pack()

gameover_image_raw=Image.open("assets/gameOver.png")

gameover_image_resized=ImageTk.PhotoImage(gameover_image_raw.resize((500,300)))

gameover_popup=Label(game_over_frame,image=gameover_image_resized)
gameover_popup.place(x=0,y=0)
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
                    
restart_button.place(x=65,y=230)

#score place
score_display=Label(game_over_frame,text="0",
                    width=10,
                    height=1,
                    font=("Komika Axis",15,"bold"),
                    bg="#151552",
                    fg="white"
                    )
score_display.place(x=106,y=117)

testwindow.mainloop()



