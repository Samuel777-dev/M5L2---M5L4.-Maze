
import os
from pygame import *

# Obtener la ruta de la carpeta donde está guardado el archivo .py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Clases requeridas

# Clase padre para los objetos
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()

        # Cargar la imagen desde la carpeta del proyecto
        ruta_imagen = os.path.join(BASE_DIR, player_image)

        self.image = transform.scale(
            image.load(ruta_imagen),
            (65, 65)
        )

        self.speed = player_speed

        # Crear el rectángulo del objeto
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Clase derivada para el jugador
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x < win_width - self.rect.width:
            self.rect.x += self.speed

        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed

        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed


# Clase derivada para el enemigo
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

        if self.rect.x >= win_width - self.rect.width:
            self.direction = "izquierda"

        if self.direction == "izquierda":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


# Clase para los obstáculos
class Wall(sprite.Sprite):
    def __init__(
        self,
        color_1,
        color_2,
        color_3,
        wall_x,
        wall_y,
        wall_width,
        wall_height
    ):
        super().__init__()

        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3

        self.width = wall_width
        self.height = wall_height

        # Crear la superficie de la pared
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))

        # Crear el rectángulo de la pared
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Configuración de la ventana
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


# Crear los personajes
player = Player(
    "hero.png",
    5,
    win_height - 80,
    4
)

monster = Enemy(
    "cyborg.png",
    win_width - 80,
    280,
    2
)

final = GameSprite(
    "treasure.png",
    win_width - 120,
    win_height - 80,
    0
)


# Crear las paredes del laberinto

w1 = Wall(154, 205, 50, 100, 20, 450, 10)#pared superior
w2 = Wall(154, 205, 50, 100, 480, 350, 10)#pared inferior
w3 = Wall(154, 205, 50, 10, 20, 10, 380)#pared izquierda
w4 = Wall(154, 205, 50, 50, 70, 10, 380)#pared izquierda

# Configuración del juego
game = True
finish = False

clock = time.Clock()
FPS = 60


# Configurar los textos de victoria y derrota
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


# Cargar música y sonidos
mixer.init()

ruta_musica = os.path.join(BASE_DIR, "jungles.ogg")
mixer.music.load(ruta_musica)
mixer.music.play(-1)

ruta_dinero = os.path.join(BASE_DIR, "money.ogg")
money = mixer.Sound(ruta_dinero)

ruta_golpe = os.path.join(BASE_DIR, "kick.ogg")
kick = mixer.Sound(ruta_golpe)


# Bucle principal del juego
while game:

    # Detectar eventos
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:

        # Dibujar el fondo
        window.blit(background, (0, 0))

        # Actualizar los personajes
        player.update()
        monster.update()

        # Dibujar los personajes
        player.reset()
        monster.reset()
        final.reset()

        # Dibujar las paredes
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()

        # Detectar colisiones con el enemigo y las paredes
        if (
            sprite.collide_rect(player, monster)
            or sprite.collide_rect(player, w1)
            or sprite.collide_rect(player, w2)
            or sprite.collide_rect(player, w3)
            or sprite.collide_rect(player, w4)
        ):
            finish = True
            window.blit(lose, (200, 200))
            kick.play()

        # Detectar si el jugador llega al tesoro
        elif sprite.collide_rect(player, final):
            finish = True
            window.blit(win, (200, 200))
            money.play()

    # Actualizar la pantalla
    display.update()
    clock.tick(FPS)


# Cerrar Pygame
mixer.music.stop()
quit()
