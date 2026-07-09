from ui import Ui
from collectibles import Collectible
import random
from camera import Camera
from sound import DJ
from saveManager import SavesManager


class Game:
    def __init__(self):
        self.score = 0
        self.highScore = 0
        self.speed = 100
        self.lives = 3
        self.running = True
        
        self.cam = Camera("saved_model.pt", 0)
        self.ui = Ui()
        self.savesManager = SavesManager()

        self.current_collectible = None

        self.dj = DJ()

        

    def bindControls(self):
        self.ui.bottomArea.controlButtons.set_commands(
            left = self.pepe.left,
            right= self.pepe.right,
            up = self.pepe.up,
            down= self.pepe.down

        )
        

        #binding the same to keyboard keys
        self.ui.window.bind("<Left>",self.pepe.left)
        self.ui.window.bind("<Right>",self.pepe.right)
        self.ui.window.bind("<Up>",self.pepe.up)
        self.ui.window.bind("<Down>",self.pepe.down)

        #restart button
        self.ui.gameOver.set_restart(command=self.restart)
        self.ui.gameOver.set_quit(command= self.exit_game)
    
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
        self.ui.topArea.update_score(self.score)
    
    def update_speed(self):
        if self.speed>=40:
            self.speed-=2

    def update_lives(self):

        self.lives-=1

        if self.lives==0: 
            self.game_over()
            

        self.ui.topArea.update_lives(self.lives)

    def updateHighScore(self, score):
        self.ui.topArea.updateHighScore(score=score)
        self.highScore = score
        

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
        self.ui.gameOver.show(self.score)
    
    def hide_game_over(self):
        self.ui.gameOver.hide()

    def game_over(self):
    
        
        self.running=False
        self.ui.gameOver.show(self.score)
       
        for btn in self.ui.bottomArea.controlButtons.buttons_list:
            btn.config(state='disabled')
        self.dj.play_gameover_music()

        if self.score > self.highScore:
            self.updateHighScore(self.score)

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
        # if not self.running:
        #     return
        
        result = self.cam.read()
        if result['analyzed']:
            self.handle_camera_inputs(result['labels'])
            self.ui.bottomArea.cam.update_camera(frame=result['annotated_frame'])
        
        else:
            self.ui.bottomArea.cam.update_camera(frame=result['frame'])
        

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
        for btn in self.ui.bottomArea.controlButtons.buttons_list:
            btn.config(state='normal')
        self.spawn_collectible()
        self.dj.restart_bgm()
        self.operate_camera()

    def exit_game(self):
        self.savesManager.updateHighScore(self.highScore)
        self.cam.release()
        self.ui.window.destroy()

    def setup(self):
        
        self.pepe = self.ui.pepe
        self.collectibles = [Collectible(self.ui.playArea, text) for text in ['🍌','🍉','🍊','🍈','🍇']]
        self.bindControls()
        
        self.highScore = self.savesManager.getHighScore()
        self.updateHighScore(self.highScore)

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