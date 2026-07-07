from ui import Screen
import tkinter

screen = Screen()

window = tkinter.Tk()

window.geometry(f"{screen.windowWidth}x{screen.windowHeight}")
window.title("Pepe Run")

window.mainloop()