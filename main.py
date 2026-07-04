import pygame
import sys
import random
import math

from settings import *
from entities.player import Player
from entities.enemy import Enemy
from entities.projectile import Projectile
from entities.xp_gem import XPGem
from entities.orbiting_orb import OrbitingOrb

from items.orb_item import OrbItem

# Inicializa todos los módulos de pygame
pygame.init()

# Crear ventana
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Título de la ventana
pygame.display.set_caption(TITLE)

# Controlador de FPS
clock = pygame.time.Clock()

#Camara
camera_offset = pygame.Vector2()

#Fuente del texto
font = pygame.font.SysFont(None, 36)

# Crear jugador
player = Player(WIDTH // 2, HEIGHT // 2)

#Crear enemigos
enemies = []

#Porpiedades de spawneo de enemigos
enemy_spawn_timer = 0
enemy_spawn_cooldown = 2

#Contador de tiempo de la partida
game_time = 0

#Crear proyectiles
projectiles = []

#Crear gemas de experiencia
xp_gems = []

#Crear orbes e items de orbes
orbs = []
orb_items = []

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

    #Probabilidad de spawn de enemigos
    enemy_type = random.choices(
        ["normal", "fast", "tank"],
        weights=[70, 20, 10]
    )[0]

    enemy = Enemy(x, y, enemy_type)

    #Aumentar las estadisticas de los enemigos con el tiempo
    enemy.health += int(game_time // 20)
    enemy.speed += game_time * 0.5

    enemies.append(enemy)

#Funcion para redistribuir orbes
def redistribute_orbs():
    if len(orbs) == 0:
        return

    angle_step = (2 * math.pi) / len(orbs)

    for index, orb in enumerate(orbs):
        orb.set_angle(index * angle_step)

# Variable principal del game loop
running = True

#Estado de level up
level_up_menu = False

upgrade_options = [
    "Damage",
    "Attack Speed",
    "Move Speed"
]

# GAME LOOP
while running:
    # Delta time
    dt = clock.tick(FPS) / 1000

    # EVENTOS
    for event in pygame.event.get():
        # Detectar cierre de ventana
        if event.type == pygame.QUIT:
            running = False

        #Seleccion de mejoras del menu de level up
        if level_up_menu and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                player.damage += 1
                level_up_menu = False

            elif event.key == pygame.K_2:
                player.shoot_cooldown *= 0.9
                level_up_menu = False

            elif event.key == pygame.K_3:
                player.speed += 50
                level_up_menu = False

    # UPDATE
    if not level_up_menu:
        #Actualiza jugador
        player.handle_movement(dt)

        #Actualiza camara
        camera_offset.x = player.position.x - WIDTH // 2
        camera_offset.y = player.position.y - HEIGHT // 2

        #Actualiza orbes
        for orb in orbs:
            orb.update(dt)

        #Actualiza tiempo de juego
        game_time += dt

        #Actualiza timer de invulnerabilidad
        if player.invulnerability_timer > 0:
            player.invulnerability_timer -= dt

        #Actualiza temporizador de disparo
        player.shoot_timer -= dt

        #Actualiza temporizador de spawn de enemigos
        enemy_spawn_timer += dt

        #Cooldown de spawneo de enemigos
        current_spawn_cooldown = max(0.3, enemy_spawn_cooldown - (game_time * 0.02))

        #Spawn automatico de enemigos
        if enemy_spawn_timer >= current_spawn_cooldown:
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

        #Detecta colision de orbes con los enemigos
        for orb in orbs:
            orb_rect = pygame.Rect(
                orb.position.x - orb.radius,
                orb.position.y - orb.radius,
                orb.radius * 2,
                orb.radius * 2
            )

            for enemy in enemies[:]:

                if orb_rect.colliderect(enemy.rect):
                    #Detecta el cooldown de daño del enemigo, si no tiene cooldown, le hace daño y setea el nuevo cooldown
                    if enemy.damage_cooldown <= 0:
                        died = enemy.take_damage(orb.damage)
                        enemy.damage_cooldown = 0.5

                        if died:

                            xp_gem = XPGem(
                                enemy.rect.centerx,
                                enemy.rect.centery
                            )

                            xp_gems.append(xp_gem)

                            #Posibilidad de dropear un item de orbe
                            if random.random() < 0.1:
                                orb_item = OrbItem(
                                    enemy.rect.centerx,
                                    enemy.rect.centery
                                )

                                orb_items.append(orb_item)

                            enemies.remove(enemy)

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
                    died = enemy.take_damage(player.damage)

                    # Eliminar proyectil
                    if projectile in projectiles:
                        projectiles.remove(projectile)

                    # Si enemigo murió
                    if died:
                        xp_gem = XPGem(
                            enemy.rect.centerx,
                            enemy.rect.centery
                        )

                        #Distintas recompensas segun el tipo de enemigo
                        if enemy.enemy_type == "fast":
                            xp_gem.value = 2

                        elif enemy.enemy_type == "tank":
                            xp_gem.value = 5

                        xp_gems.append(xp_gem)

                        #Posibilidad de dropear un item de orbe
                        if random.random() < 0.1:
                            orb_item = OrbItem(
                                enemy.rect.centerx,
                                enemy.rect.centery
                            )

                            orb_items.append(orb_item)

                        enemies.remove(enemy)

                    break

        player_center = pygame.Vector2(
            player.rect.centerx,
            player.rect.centery
        )

        #Recolecta gemas de xp
        for gem in xp_gems[:]:
            distance = player_center.distance_to(gem.position)

            if distance < 30:
                leveled_up = player.gain_xp(gem.value)

                if leveled_up:
                    level_up_menu = True

                xp_gems.remove(gem)

        #Recolecta items de orbe
        for item in orb_items[:]:
            distance = player_center.distance_to(item.position)

            if distance < 30:
                #Agregar nuevo orbe
                new_orb = OrbitingOrb(player)
                orbs.append(new_orb)

                #Redistribuir los orbes
                redistribute_orbs()

                orb_items.remove(item)

        #Detecta si la vida del jugador llegó a 0
        if player.health <= 0:
            print("GAME OVER")
            running = False

    # DRAW
    screen.fill(BACKGROUND_COLOR)

    #Dibujar al jugador
    player.draw(screen, camera_offset)

    #Dibuja los orbes
    for orb in orbs:
        orb.draw(screen, camera_offset)

    #Dibujar enemigos
    for enemy in enemies:
        enemy.draw(screen, camera_offset)

    #Dibujar proyectiles
    for projectile in projectiles:
        projectile.draw(screen, camera_offset)

    #Dibujar gemas de experiencia
    for gem in xp_gems:
        gem.draw(screen, camera_offset)

    #Dibuja items de orbe
    for item in orb_items:
        item.draw(screen, camera_offset)

    #Barra de vida
    bar_width = 250
    bar_height = 25

    health_ratio = player.health / player.max_health

    pygame.draw.rect(
        screen,
        (100, 0, 0),
        (20, 20, bar_width, bar_height)
    )

    #Vida actual
    pygame.draw.rect(
        screen,
        (255, 0, 0),
        (20, 20, bar_width * health_ratio, bar_height)
    )

    #Barra de XP
    xp_needed = player.level * 5
    xp_ratio = player.xp / xp_needed

    pygame.draw.rect(
        screen,
        (40, 40, 40),
        (20, 60, bar_width, 20)
    )

    pygame.draw.rect(
        screen,
        (50, 150, 255),
        (20, 60, bar_width * xp_ratio, 20)
    )

    #Nivel
    level_text = font.render(
        f"Level {player.level}",
        True,
        (255, 255, 255)
    )

    screen.blit(level_text, (20, 90))

    #Dibuja el tiempo de la partida
    time_text = font.render(
        f"Time: {int(game_time)}s",
        True,
        (255, 255, 255)
    )

    screen.blit(time_text, (20, 130))

    #Dibuja el menu de level up
    if level_up_menu:
        menu_text = font.render(
            "LEVEL UP! Escoge una mejora:",
            True,
            (255, 255, 0)
        )

        option_1 = font.render(
            "1 - Más Daño",
            True,
            (255, 255, 255)
        )

        option_2 = font.render(
            "2 - Más velocidad de ataque",
            True,
            (255, 255, 255)
        )

        option_3 = font.render(
            "3 - Más velocidad de movimiento",
            True,
            (255, 255, 255)
        )

        screen.blit(menu_text, (400, 250))
        screen.blit(option_1, (400, 320))
        screen.blit(option_2, (400, 370))
        screen.blit(option_3, (400, 420))

    # Actualizar pantalla
    pygame.display.flip()

# Cierre limpio
pygame.quit()
sys.exit()