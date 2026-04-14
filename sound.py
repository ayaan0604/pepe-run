import pygame



class DJ:
    def __init__(self):
        pygame.mixer.init()
        self.mixer = pygame.mixer
        self.mixer.music.set_volume(0.5)

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
        sfx=self.mixer.Sound("assets/sounds/collect.mp3")
        sfx.play()

    def movesound(self):
        sfx=self.mixer.Sound("assets/sounds/move.mp3")
        sfx.play()

    def damageSound(self):
        sfx=self.mixer.Sound("assets/sounds/damage.mp3")
        sfx.play()


