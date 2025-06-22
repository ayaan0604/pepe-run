import pygame


pygame.mixer.init()

def play_bgm():
    pygame.mixer.music.load("assets/sounds/game_bgm.mp3")
    pygame.mixer.music.play(-1)

def play_gameover_music():
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/sounds/gameover_bgm.mp3")
    pygame.mixer.music.play(-1)

def restart_bgm():
    pygame.mixer.stop()
    play_bgm()

def collect_sfx():
    sfx=pygame.mixer.Sound("assets/sounds/collect.mp3")
    sfx.play()

def movesound():
    sfx=pygame.mixer.Sound("assets/sounds/move.mp3")
    sfx.play()

def damageSound():
    sfx=pygame.mixer.Sound("assets/sounds/damage.mp3")
    sfx.play()


