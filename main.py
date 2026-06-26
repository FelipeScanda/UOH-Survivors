import pygame
import sys
import random

from settings import *
from entities.player import Player
from entities.enemy import Enemy

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

#Crear enemigos
enemies = []

for i in range(5):

    enemy = Enemy(
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT)
    )

    enemies.append(enemy)

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
    #Actualiza jugador
    player.handle_movement(dt)

    #Actualiza enemigos
    for enemy in enemies:
        enemy.update(player, dt)

    # DRAW
    screen.fill(BACKGROUND_COLOR)

    #Dibujar al jugador
    player.draw(screen)

    #Dibujar enemigos
    for enemy in enemies:
        enemy.draw(screen)

    # Actualizar pantalla
    pygame.display.flip()

    # Limitar FPS
    clock.tick(FPS)

# Cierre limpio
pygame.quit()
sys.exit()