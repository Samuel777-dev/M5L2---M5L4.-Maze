
import os
from pygame import *

# Obtener la ruta de la carpeta donde está guardado el archivo .py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Clases requeridas

# Clase padre para los objetos
class GameSprite(sprite.Sprite):
    # Constructor de clase
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()

        # Cargar la imagen desde la carpeta del proyecto
        ruta_imagen = os.path.join(BASE_DIR, player_image)
        self.image = transform.scale(
            image.load(ruta_imagen),
            (65, 65)
        )
        self.speed = player_speed

        # Cada objeto debe almacenar la propiedad rect
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Clase derivada para el jugador (controlado por las flechas)
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


# Clase derivada para el enemigo (se mueve solo)
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


# Escena del juego
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Laberinto")

# Cargar el fondo desde la carpeta del proyecto
ruta_fondo = os.path.join(BASE_DIR, "background.jpg")
background = transform.scale(
    image.load(ruta_fondo),
    (win_width, win_height)
)


# Personajes del juego
player = Player("hero.png", 5, win_height - 80, 4)
monster = Enemy("cyborg.png", win_width - 80, 280, 2)
final = GameSprite("treasure.png", win_width - 120, win_height - 80, 0)


# Configuración del juego
game = True
finish = False

clock = time.Clock()
FPS = 60


# Música
mixer.init()

ruta_musica = os.path.join(BASE_DIR, "jungles.ogg")
mixer.music.load(ruta_musica)
mixer.music.play()


# Bucle principal del juego
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        # Dibujar el fondo
        window.blit(background, (0, 0))

        # Actualizar el movimiento de los personajes
        player.update()
        monster.update()

        # Dibujar los personajes
        player.reset()
        monster.reset()
        final.reset()

    # Actualizar la pantalla
    display.update()
    clock.tick(FPS)

# Cerrar Pygame
quit()

