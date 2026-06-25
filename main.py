import pygame
import sys

from settings import *


# Inicializa todos los módulos de pygame
pygame.init()


# Crear ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Título de la ventana
pygame.display.set_caption(TITLE)


# Controlador de FPS
clock = pygame.time.Clock()


# Variable principal del game loop
running = True

# GAME LOOP
while running:

    # EVENTOS
    for event in pygame.event.get():

        # Detectar cierre de ventana
        if event.type == pygame.QUIT:
            running = False

    # UPDATE

    # DRAW
    screen.fill(BACKGROUND_COLOR)


    # Actualizar pantalla
    pygame.display.flip()


    # Limitar FPS
    clock.tick(FPS)


# Cierre limpio
pygame.quit()
sys.exit()