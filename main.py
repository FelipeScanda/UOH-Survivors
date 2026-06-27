import pygame
import sys
import random

from settings import *
from entities.player import Player
from entities.enemy import Enemy
from entities.projectile import Projectile
from entities.xp_gem import XPGem

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

#Porpiedades de spawneo de enemigos
enemy_spawn_timer = 0
enemy_spawn_cooldown = 2

#Crear proyectiles
projectiles = []

#Crear gemas de experiencia
xp_gems = []

#Genera 5 enemigos
for i in range(5):

    enemy = Enemy(
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT)
    )

    enemies.append(enemy)

#Funcion para spawnear enemigos
def spawn_enemy():

    side = random.randint(0, 3)

    if side == 0:  # arriba
        x = random.randint(0, WIDTH)
        y = -50

    elif side == 1:  # abajo
        x = random.randint(0, WIDTH)
        y = HEIGHT + 50

    elif side == 2:  # izquierda
        x = -50
        y = random.randint(0, HEIGHT)

    else:  # derecha
        x = WIDTH + 50
        y = random.randint(0, HEIGHT)

    enemy = Enemy(x, y)

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

    #Actualiza timer de invulnerabilidad
    if player.invulnerability_timer > 0:
        player.invulnerability_timer -= dt

    #Actualiza temporizador de disparo
    player.shoot_timer -= dt

    #Actualiza tempórizador de spawn de enemigos
    enemy_spawn_timer += dt

    #Spawn automatico de enemigos
    if enemy_spawn_timer >= enemy_spawn_cooldown:

        spawn_enemy()

        enemy_spawn_timer = 0

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

    #Detecta colisiones de enemigos con el jugador
    for enemy in enemies:

        if enemy.rect.colliderect(player.rect):

            player.take_damage(10)

    #Actualiza proyectiles
    for projectile in projectiles:
        projectile.update(dt)

    for projectile in projectiles[:]:

        projectile_rect = pygame.Rect(
            projectile.position.x - projectile.radius,
            projectile.position.y - projectile.radius,
            projectile.radius * 2,
            projectile.radius * 2
        )

        for enemy in enemies[:]:

            if projectile_rect.colliderect(enemy.rect):

                died = enemy.take_damage(1)

                # Eliminar proyectil
                if projectile in projectiles:
                    projectiles.remove(projectile)

                # Si enemigo murió
                if died:

                    xp_gem = XPGem(
                        enemy.rect.centerx,
                        enemy.rect.centery
                    )

                    xp_gems.append(xp_gem)

                    enemies.remove(enemy)

                break

    player_center = pygame.Vector2(
        player.rect.centerx,
        player.rect.centery
    )

    for gem in xp_gems[:]:

        distance = player_center.distance_to(gem.position)

        if distance < 30:

            player.gain_xp(gem.value)

            xp_gems.remove(gem)

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

    #Dibujar gemas de experiencia
    for gem in xp_gems:
        gem.draw(screen)

    # Actualizar pantalla
    pygame.display.flip()

    # Limitar FPS
    clock.tick(FPS)

# Cierre limpio
pygame.quit()
sys.exit()