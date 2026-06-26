import pygame
import sys
import random

from settings import *
from entities.player import Player
from entities.enemy import Enemy
from entities.projectile import Projectile

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

#Crear proyectiles
projectiles = []

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

    #Actualiza temporizador de disparo
    player.shoot_timer -= dt

    #Disparo automático
    if player.shoot_timer <= 0:

        direction = player.shoot(enemies)

        if direction:

            projectile = Projectile(
                player.rect.centerx,
                player.rect.centery,
                direction
            )

            projectiles.append(projectile)

            player.shoot_timer = player.shoot_cooldown

    #Actualiza enemigos
    for enemy in enemies:
        enemy.update(player, dt)

    #Actualiza proyectiles
    for projectile in projectiles:
        projectile.update(dt)

    # DRAW
    screen.fill(BACKGROUND_COLOR)

    #Dibujar al jugador
    player.draw(screen)

    #Dibujar enemigos
    for enemy in enemies:
        enemy.draw(screen)

    #Dibujar proyectiles
    for projectile in projectiles:
        projectile.draw(screen)

    # Actualizar pantalla
    pygame.display.flip()

    # Limitar FPS
    clock.tick(FPS)

# Cierre limpio
pygame.quit()
sys.exit()