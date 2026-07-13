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
        
        self.cam = Camera(0)
        self.cam.enabled = True
        self.ui = Ui()
        self.savesManager = SavesManager()

        self.current_collectible = None

        self.dj = DJ()

        

    def bindControls(self):

        #ui buttons
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

        #gameover
        self.ui.gameOver.set_button_commands(
            restart= self.restart,
            menu= self.show_main_menu,
            quit= self.exit_game
        )
        
        #main menu
        self.ui.mainMenu.set_button_commands(
            play=self.restart,
            help= self.show_help_screen,
            settings= self.show_settings_screen,
            quit=self.exit_game,                                
        )

        #help menu
        self.ui.helpMenu.set_button_command(cross= self.hide_help_screen)

        #settings menue
        self.ui.settingsMenu.setCommands(
            volumeBar= self.operateVolumeBar,
            enable= self.toggleCam
        )
    
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
            self.speed-=3

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
            self.dj.damagesound()

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

    def show_main_menu(self):
        self.running = False
        self.hide_game_over()
        self.ui.mainMenu.show()
        self.dj.playMainMenuBgm()
    
    def hide_main_menu(self):
        self.ui.mainMenu.hide()
    
    def show_help_screen(self):
        self.ui.helpMenu.show()
    
    def hide_help_screen(self):
        self.ui.helpMenu.hide()
    
    def show_settings_screen(self):
        self.ui.settingsMenu.show()

    def operateVolumeBar(self, volume):
        volume = int(volume)

        self.ui.settingsMenu.setVolumeText(volume)
        self.updateVolume(volume)

    def game_over(self):
    
        
        self.running=False
        self.ui.gameOver.show(self.score)
       
        for btn in self.ui.bottomArea.controlButtons.buttons_list:
            btn.config(state='disabled')
        self.dj.play_gameover_music()

        if self.score > self.highScore:
            self.updateHighScore(self.score)

        self.ui.bottomArea.cam.setText("")

    def setSelectedCamera(self):
        cameraName = self.ui.settingsMenu.dropdown.getSelected()
        self.cam.setCamIndex(cameraName)


    def enableCamera(self):
        self.cam.enabled = True
        self.setSelectedCamera()
        self.cam.startCam()
        self.ui.settingsMenu.setEnableButtonText("Disable Camera")
        self.ui.settingsMenu.dropdown.disableDropDown()
        self.operate_camera()

    def disableCamera(self):
        self.cam.enabled = False
        self.ui.settingsMenu.setEnableButtonText("Enable Camera")
        self.ui.settingsMenu.dropdown.enableDropDown()
        self.ui.bottomArea.cam.disableCam()
        self.cam.release()

    def toggleCam(self):
        if self.cam.enabled:
            self.disableCamera()
        else:
            self.enableCamera()

    def handle_camera_inputs(self, labels):
        if not self.running:
            return

        if not labels:
            return
        
        
        
        if 'up' in labels:
            self.pepe.up()
            self.ui.bottomArea.cam.setText("up")

        elif 'down' in labels:
            self.pepe.down()
            self.ui.bottomArea.cam.setText("down")

        elif 'right' in labels:
            self.pepe.right()
            self.ui.bottomArea.cam.setText("right")

        elif 'left' in labels:
            self.ui.bottomArea.cam.setText("left")
            self.pepe.left()
        
    

    def operate_camera(self):
        # if not self.running:
        #     return

        if not self.cam.enabled:
            return
        
        frame, label = self.cam.read()
        if frame is None:
            self.ui.bottomArea.cam.imageLabel.config(text="Camera error\nPlease try any other camera")
            return
        
        
            
        self.handle_camera_inputs(label)

        self.ui.bottomArea.cam.update_camera(frame=frame)

        # if result['analyzed'] and (result['annotated_frame'] is not None):
        #     self.ui.bottomArea.cam.update_camera(frame=result['annotated_frame'])
        # else:
        #     self.ui.bottomArea.cam.update_camera(frame=result['frame'])

        self.ui.window.after(33, self.operate_camera)

    def restart(self):
        
        
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
        self.hide_main_menu()
        for btn in self.ui.bottomArea.controlButtons.buttons_list:
            btn.config(state='normal')
        
        self.ui.window.after(100, self.spawn_collectible)
        self.ui.window.after(500, self.operate_camera)
        
        self.dj.restart_bgm()

    def exit_game(self):
        self.savesManager.updateHighScore(self.highScore)
        self.cam.release()
        self.ui.window.destroy()

    def setup(self):
        
        self.pepe = self.ui.pepe
        self.collectibles = [Collectible(self.ui.playArea, text) for text in ['🍌','🍉','🍊','🍈','🍇']]
        self.bindControls()
        self.ui.bottomArea.cam.setText("")
        
        self.highScore = self.savesManager.getHighScore()
        self.updateHighScore(self.highScore)
        self.toggleCam()
        self.ui.settingsMenu.dropdown.createDropdown(self.cam.cameraList)

        self.ui.window.protocol("WM_DELETE_WINDOW", self.exit_game )
       
        

    def updateVolume(self, value):
        self.dj.updateVolume(value)
        self.pepe.dj.updateVolume(value)

    def run(self):
        self.setup()
        self.updateVolume(10)
        self.show_main_menu()
        self.ui.window.after(500, self.operate_camera)
        self.ui.window.mainloop()


    
if __name__ == "__main__":
    game = Game()
    game.run()