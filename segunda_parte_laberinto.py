
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
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(
            player_image,
            player_x,
            player_y,
            player_speed
        )
        
        self.direction = "izquierda"

    def update(self):
        if self.rect.x <= 470:
            self.direction = "derecha"

        if self.rect.x >= win_width - 85:
            self.direction = "izquierda"

        if self.direction == "izquierda":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height

        # Crear la superficie del muro y rellenarla con el color especificado
        self.image = Surface((self.width, self.height))
        self.image.fill((self.color_1, self.color_2, self.color_3))

        # Cada muro debe almacenar la propiedad rect
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
# Escena del juego
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Laberinto")

# Cargar el fondo desde la carpeta del proyecto
ruta_fondo = os.path.join(BASE_DIR, "fondo.png")
background = transform.scale(
    image.load(ruta_fondo),
    (win_width, win_height)
)


# Personajes del juego
player = Player("fantasma.py.png", 5, win_height - 80, 4)
monster = Enemy("pacman.py.png", win_width - 80, 280, 2)
final = GameSprite("anchetasinfondo.png", win_width - 120, win_height - 80, 0)

w1 = wall(154, 205, 50, 100, 20, 450, 10)
w2 = wall(154, 205, 50, 100, 480, 350, 10)
w3 = wall(154, 205, 50, 10, 20, 10, 380)
# Configuración del juego
game = True
finish = False

clock = time.Clock()
FPS = 60

font.init()

game_font = font.Font(None, 70)

win = game_font.render(
    "¡GANASTE!", 
    True, 
    (255, 215, 0)
    )

lose = game_font.render(
    "¡PERDISTE!",
    True,
    (180, 0, 0)
)

# Música
mixer.init()

ruta_musica = os.path.join(BASE_DIR, "asi te quiero yo.mp3")
mixer.music.load(ruta_musica)
mixer.music.play()

ruta_dinero = os.path.join(BASE_DIR, "money.ogg")
dinero = mixer.Sound(ruta_dinero)

ruta_golpe = os.path.join(BASE_DIR, "kick.ogg")
kick = mixer.Sound(ruta_golpe)

# Bucle principal del juego
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        # Dibujar el fondo
        window.blit(background, (0, 0))

        # Actualizar el movimiento de los personajes
        player.update()
        monster.update()

        # Dibujar los personajes
        player.reset()
        monster.reset()
        final.reset()

        # Dibujar las paredes del laberinto
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()

        # Comprobar colisiones
        if(
        sprite.collide_rect(player, monster) 
        or sprite.collide_rect(player, w1)
        or sprite.collide_rect(player, w2)
        or sprite.collide_rect(player, w3)
        ):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()
            

    

        # Actualizar el movimiento de los personajes
    elif sprite.collide_rect(player, final):
        finish = True
        window.blit(win, (200, 200))
        dinero.play()

    # Actualizar la pantalla
    display.update()
    clock.tick(FPS)

# Cerrar Pygame
quit()

