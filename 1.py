
import os
from pygame import *

# Obtener la ruta de la carpeta donde está guardado el archivo .py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Clases requeridas



# Escena del juego
win_width = 700
win_height = 500

window = display.set_mode((win_width, win_height))
display.set_caption("Maze")

# Cargar el fondo utilizando BASE_DIR
ruta_fondo = os.path.join(BASE_DIR, "background.jpg")
background = transform.scale(
    image.load(ruta_fondo),
    (win_width, win_height)
)

# Configuración del juego
game = True
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

    # Dibujar el fondo
    window.blit(background, (0, 0))

    # Actualizar la pantalla
    display.update()
    clock.tick(FPS)

# Cerrar correctamente Pygame
quit()
