from ui import Ui
from collectibles import Collectible
import random
from camera import Camera
from sound import DJ


class Game:
    def __init__(self):
        self.score = 0
        self.speed = 100
        self.lives = 3
        self.running = True
        
        self.cam = Camera("../model/saved_model.pt", 0)
        self.ui = Ui()

        self.current_collectible = None

        self.dj = DJ()

        self.cam = Camera("../model/saved_model.pt", 0)


        

    def bindControls(self):
        self.ui.rightButton.config(command=self.pepe.right)
        self.ui.leftButton.config(command=self.pepe.left)
        self.ui.upButton.config(command=self.pepe.up)
        self.ui.downButton.config(command=self.pepe.down)

        #binding the same to keyboard keys
        self.ui.window.bind("<Left>",self.pepe.left)
        self.ui.window.bind("<Right>",self.pepe.right)
        self.ui.window.bind("<Up>",self.pepe.up)
        self.ui.window.bind("<Down>",self.pepe.down)

        #restart button
        self.ui.restart_button.config(command=self.restart)
    
    def get_collectible(self):
       
        choice=random.choice(self.collectibles)
        collectible=Collectible(self.ui.playArea,
                        text=choice.label.cget("text"),
                        )
    
        return collectible.label

    def destroy_collectible(self):
        self.current_collectible.destroy()
        self.current_collectible = None
        self.ui.window.after(50,self.spawn_collectible)

    def collison(self):
        if not self.current_collectible:
            return

        px,py=self.pepe.smallpepeLabel.winfo_x() , self.pepe.smallpepeLabel.winfo_y()
        cx,cy=self.current_collectible.x, self.current_collectible.y

        return abs(px-cx)<30 and abs(py-cy)<30
    
    def update_score(self):
        self.ui.score_number.config(text=str(self.score))
    
    def update_speed(self):
        if self.speed>=40:
            self.speed-=2

    def update_lives(self):

        self.lives-=1

        if self.lives==0: 
            self.game_over()
            

        self.ui.life_text.config(text="🩷"*self.lives)

    def fall_collectible(self):
        
        if not self.running:
            return
        
        if self.collison():
            self.destroy_collectible()
            #self.ui.window.after(50,self.spawn_collectible)
            self.score+=1
            self.update_score()
            self.update_speed()
            self.dj.collect_sfx()
           
            return

        current_y=self.current_collectible.y
        

        if current_y< self.ui.playArea.winfo_height() * 0.82:
            self.current_collectible.place(x = self.current_collectible.x, y=self.current_collectible.y+10)
            self.current_collectible.y = self.current_collectible.y+10
            self.ui.playArea.after(self.speed,self.fall_collectible)
        else:
            self.destroy_collectible()
            self.update_lives()
            self.dj.damageSound()

    def spawn_collectible(self):
    
        self.current_collectible=self.get_collectible()
        x = int(self.ui.random_x())

        self.current_collectible.x = x
        self.current_collectible.y = 0
        
        self.current_collectible.place(x=self.current_collectible.x, y= self.current_collectible.y)
        self.fall_collectible()

    def show_game_over(self):
        self.ui.game_over_frame.lift()
    
    def hide_game_over(self):
        self.ui.game_over_frame.lower()

    def game_over(self):
    
        
        self.running=False
        self.show_game_over()
        self.ui.score_display.config(text=f"{self.score}")
        for btn in [self.ui.upButton,self.ui.downButton,self.ui.leftButton,self.ui.rightButton]:
            btn.config(state='disabled')
        self.dj.play_gameover_music()

    def handle_camera_inputs(self, labels):
        if not labels:
            return
        
        if 'up' in labels:
            self.pepe.up()

        if 'down' in labels:
            self.pepe.down()

        if 'left' in labels:
            self.pepe.right()

        if 'right' in labels:
            self.pepe.left()
        
    

    def operate_camera(self):
        if not self.running:
            return
        
        result = self.cam.read()
        if result['analyzed']:
            print(result['labels'])
            self.handle_camera_inputs(result['labels'])
            self.ui.update_camera(frame=result['annotated_frame'])
        
        else:
            self.ui.update_camera(frame=result['frame'])

        


        
        

        self.ui.window.after(5, self.operate_camera)

    def restart(self,event=None):
        
        
        if self.current_collectible:
            self.current_collectible.destroy()
        self.score=0
        self.update_score()
        self.lives=self.pepe.maxLives+1
        self.update_lives()
        self.speed=100
        self.running=True
        self.pepe.smallpepeLabel.place(x=random.choice(range(0,int(self.ui.screen.playwidth))),y=random.choice(range(0,int(self.ui.screen.playHeight))))
        self.hide_game_over()
        for btn in [self.ui.upButton,self.ui.downButton,self.ui.leftButton,self.ui.rightButton]:
            btn.config(state='normal')
        self.spawn_collectible()
        self.dj.restart_bgm()
        self.operate_camera()

    def exit_game(self):
        self.cam.release()
        self.ui.window.destroy()

    def setup(self):
        self.ui.setup_ui()
        self.pepe = self.ui.pepe
        self.collectibles = [Collectible(self.ui.playArea, text) for text in ['🍌','🍉','🍊','🍈','🍇']]
        self.bindControls()
        

        self.ui.window.protocol("WM_DELETE_WINDOW", self.exit_game )
       
        



    def run(self):
        self.setup()
        self.spawn_collectible()
        self.lives = self.pepe.maxLives
        self.dj.play_bgm()
        self.operate_camera()
        self.ui.window.mainloop()


    
if __name__ == "__main__":
    game = Game()
    game.run()