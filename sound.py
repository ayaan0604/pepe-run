import pygame



class DJ:
    def __init__(self):
        pygame.mixer.init()
        self.mixer = pygame.mixer

        self.master_volume = 0.5

        self.mixer.music.set_volume(self.master_volume)

        self.collectSound = self.mixer.Sound("assets/sounds/collect.mp3")
        self.moveSound = self.mixer.Sound("assets/sounds/move.mp3")
        self.damageSound = self.mixer.Sound("assets/sounds/damage.mp3")



    def play_bgm(self):
        self.mixer.music.load("assets/sounds/game_bgm.mp3")
        self.mixer.music.play(-1)

    def play_gameover_music(self):
        self.mixer.music.stop()
        self.mixer.music.load("assets/sounds/gameover_bgm.mp3")
        self.mixer.music.play(-1)

    def restart_bgm(self):
        self.mixer.stop()
        self.play_bgm()

    def collect_sfx(self):
        self.collectSound.set_volume(self.master_volume)
        self.collectSound.play()

    def movesound(self):
        self.moveSound.set_volume(self.master_volume)
        self.moveSound.play()

    def damageSound(self):
        self.damageSound.set_volume(self.master_volume)
        self.damageSound.play()
    
    def stop(self):
        self.mixer.stop()

    def updateVolume(self, value):
        value = float(value)/100
        self.master_volume = value
        self.mixer.music.set_volume(value)

