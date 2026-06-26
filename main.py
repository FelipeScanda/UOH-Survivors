import pygame
import sys

from settings import *
from entities.player import Player

# Inicializa todos los módulos de pygame
pygame.init()

# Crear ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Título de la ventana
pygame.display.set_caption(TITLE)

# Controlador de FPS
clock = pygame.time.Clock()

# Crear jugador
player = Player(WIDTH // 2, HEIGHT // 2)

# Variable principal del game loop
running = True

# GAME LOOP
while running:

    # Delta time
    dt = clock.tick(FPS) / 1000

    # EVENTOS
    for event in pygame.event.get():

        # Detectar cierre de ventana
        if event.type == pygame.QUIT:
            running = False

    # UPDATE
    player.handle_movement(dt)

    # DRAW
    screen.fill(BACKGROUND_COLOR)

    #Dibujar al jugador
    player.draw(screen)

    # Actualizar pantalla
    pygame.display.flip()

    # Limitar FPS
    clock.tick(FPS)

# Cierre limpio
pygame.quit()
sys.exit()