import os

from pygame import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        ruta_imagen = os.path.join(BASE_DIR, player_image)
        self.image = transform.scale(
            image.load(ruta_imagen),
            (65, 65)
        )
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
        
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
            
class Enemy(GameSprite):
    direction = "izquierda"

    def update(self):
        if self.rect.x <= 470:
            self.direction = "derecha"

        if self.rect.x >= win_width - 85:
            self.direction = "izquierda"

        if self.direction == "izquierda":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Laberinto")

ruta_fondo = os.path.join(BASE_DIR, "fondolaberinto.jpg")
background = transform.scale(image.load(ruta_fondo), (win_width, win_height))

player = Player("hero.png", 5, win_height - 80, 4)
monster = Enemy("cyborg.png", win_width - 80, 280, 2)
final = GameSprite("anchetasinfondo.png", win_width - 120, win_height - 80, 0)
game = True
finish = False

clock = time.Clock()
FPS = 60


mixer.init()

ruta_musica = os.path.join(BASE_DIR, "musicafondo.ogg")
mixer.music.load(ruta_musica)
mixer.music.play()



while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(background, (0, 0))
        player.update()
        monster.update()

        player.reset()
        monster.reset()
        final.reset()

    display.update()
    clock.tick(FPS)
    
quit()