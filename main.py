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
from entities.ram_boomerang import RAMBoomerang
from entities.segfault_event import SegFaultEvent

from items.orb_item import OrbItem
from items.ram_boomerang_item import RamBoomerangItem

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption(TITLE)

clock = pygame.time.Clock()

camera_offset = pygame.Vector2()

GRID_SIZE = 64

font = pygame.font.SysFont(None, 36)

menu_skin_1 = pygame.image.load("assets/player/Barranquin1.png").convert_alpha()
menu_skin_2 = pygame.image.load("assets/player/Barranquin2.png").convert_alpha()

menu_skin_1 = pygame.transform.scale(menu_skin_1,(120, 120))
menu_skin_2 = pygame.transform.scale(menu_skin_2,(120, 120))

selected_skin = 1

player = Player(WIDTH // 2, HEIGHT // 2, selected_skin)

enemies = []

enemy_spawn_timer = 0
enemy_spawn_cooldown = 2

game_time = 0

projectiles = []

xp_gems = []

orbs = []
orb_items = []
ram_boomerang_items = []

ram_boomerangs = []
ram_boomerang_level = 0
ram_boomerang_timer = 0
ram_boomerang_cooldown = 4

ram_evolved = False
segfault_event = None

def spawn_enemy():
    side = random.randint(0, 3)

    if side == 0:
        x = random.randint(0, WIDTH)
        y = -50

    elif side == 1:
        x = random.randint(0, WIDTH)
        y = HEIGHT + 50

    elif side == 2:
        x = -50
        y = random.randint(0, HEIGHT)

    else:
        x = WIDTH + 50
        y = random.randint(0, HEIGHT)

    enemy_type = random.choices(
        ["normal", "fast", "tank"],
        weights=[70, 20, 10]
    )[0]

    enemy = Enemy(x, y, enemy_type)

    enemy.health += int(game_time // 20)
    enemy.speed += game_time * 0.5

    enemies.append(enemy)

def redistribute_orbs():
    if len(orbs) == 0:
        return

    angle_step = (2 * math.pi) / len(orbs)

    for index, orb in enumerate(orbs):
        orb.set_angle(index * angle_step)

def draw_button(text, x, y, width, height):
    mouse_pos = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    hovered = button_rect.collidepoint(mouse_pos)
    color = (100, 100, 100)

    if hovered:
        color = (150, 150, 150)

    pygame.draw.rect(screen, color, button_rect)

    label = font.render(
        text,
        True,
        (255, 255, 255)
    )

    label_rect = label.get_rect(center=button_rect.center)
    screen.blit(label, label_rect)
    return button_rect

def reset_game():

    global player
    global enemies
    global projectiles
    global xp_gems
    global orb_items
    global orbs
    global ram_boomerang_items
    global game_time
    global enemy_spawn_timer
    global level_up_menu
    global selected_skin
    global ram_boomerangs
    global ram_boomerang_level
    global ram_boomerang_timer
    global ram_evolved
    global segfault_event

    player = Player(WIDTH // 2, HEIGHT // 2, selected_skin)

    enemies = []
    projectiles = []
    xp_gems = []
    orb_items = []
    orbs = []
    ram_boomerang_items = []
    ram_boomerangs = []
    ram_boomerang_level = 0
    ram_boomerang_timer = 0
    ram_evolved = False
    segfault_event = None

    game_time = 0
    enemy_spawn_timer = 0

    level_up_menu = False

running = True

game_state = "menu"

level_up_menu = False

upgrade_options = [
    "Damage",
    "Attack Speed",
    "Move Speed"
]

while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:

                if game_state == "playing":
                    game_state = "paused"

                elif game_state == "paused":
                    game_state = "playing"

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

    if game_state == "playing" and not level_up_menu:
        player.handle_movement(dt)

        camera_offset.x = player.position.x - WIDTH // 2
        camera_offset.y = player.position.y - HEIGHT // 2

        for orb in orbs:
            orb.update(dt)

        game_time += dt

        if player.invulnerability_timer > 0:
            player.invulnerability_timer -= dt

        player.shoot_timer -= dt

        enemy_spawn_timer += dt

        current_spawn_cooldown = max(0.3, enemy_spawn_cooldown - (game_time * 0.02))

        if enemy_spawn_timer >= current_spawn_cooldown:
            spawn_enemy()
            enemy_spawn_timer = 0

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

        if ram_boomerang_level > 0:
            ram_boomerang_timer -= dt

            if ram_boomerang_timer <= 0:
                direction = player.shoot(enemies)

                if direction:
                    boomerang = RAMBoomerang(
                        player.rect.centerx,
                        player.rect.centery,
                        direction
                    )
                    boomerang.damage = 3 + ram_boomerang_level
                    ram_boomerangs.append(boomerang)
                    ram_boomerang_timer = ram_boomerang_cooldown

        for boomerang in ram_boomerangs:
            boomerang.update(dt, player)

        for enemy in enemies:
            enemy.update(player, dt)

        for enemy in enemies:
            if enemy.rect.colliderect(player.rect):
                player.take_damage(10)

        for orb in orbs:
            orb_rect = pygame.Rect(
                orb.position.x - orb.radius,
                orb.position.y - orb.radius,
                orb.radius * 2,
                orb.radius * 2
            )

            for enemy in enemies[:]:

                if orb_rect.colliderect(enemy.rect):
                    if enemy.damage_cooldown <= 0:
                        died = enemy.take_damage(orb.damage)
                        enemy.damage_cooldown = 0.5

                        if died:

                            xp_gem = XPGem(
                                enemy.rect.centerx,
                                enemy.rect.centery
                            )

                            xp_gems.append(xp_gem)

                            if random.random() < 0.1:
                                orb_item = OrbItem(
                                    enemy.rect.centerx,
                                    enemy.rect.centery
                                )

                                orb_items.append(orb_item)

                            if random.random() < 0.1:
                                ram_item = RamBoomerangItem(
                                    enemy.rect.centerx,
                                    enemy.rect.centery
                                )

                                ram_boomerang_items.append(ram_item)

                            enemies.remove(enemy)

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

                    if projectile in projectiles:
                        projectiles.remove(projectile)

                    if died:
                        xp_gem = XPGem(
                            enemy.rect.centerx,
                            enemy.rect.centery
                        )

                        if enemy.enemy_type == "fast":
                            xp_gem.value = 2

                        elif enemy.enemy_type == "tank":
                            xp_gem.value = 5

                        xp_gems.append(xp_gem)

                        if random.random() < 0.1:
                            orb_item = OrbItem(
                                enemy.rect.centerx,
                                enemy.rect.centery
                            )

                            orb_items.append(orb_item)

                        if random.random() < 0.1:
                            ram_item = RamBoomerangItem(
                                enemy.rect.centerx,
                                enemy.rect.centery
                            )

                            ram_boomerang_items.append(ram_item)

                        enemies.remove(enemy)

                    break

        for boomerang in ram_boomerangs:
            hit_list = (
                boomerang.hit_enemies_outgoing
                if boomerang.state == "outgoing"
                else boomerang.hit_enemies_returning
            )

            for enemy in enemies[:]:
                enemy_center = pygame.Vector2(enemy.rect.centerx, enemy.rect.centery)
                distance = boomerang.position.distance_to(enemy_center)
                collision_distance = boomerang.get_collision_radius() + (enemy.rect.width / 2)

                if distance <= collision_distance and enemy not in hit_list:
                    hit_list.append(enemy)
                    died = enemy.take_damage(boomerang.damage)

                    if died:
                        xp_gem = XPGem(enemy.rect.centerx, enemy.rect.centery)

                        if enemy.enemy_type == "fast":
                            xp_gem.value = 2
                        elif enemy.enemy_type == "tank":
                            xp_gem.value = 5

                        xp_gems.append(xp_gem)

                        if random.random() < 0.1:
                            orb_item = OrbItem(enemy.rect.centerx, enemy.rect.centery)
                            orb_items.append(orb_item)

                        if random.random() < 0.1:
                            ram_item = RamBoomerangItem(enemy.rect.centerx, enemy.rect.centery)
                            ram_boomerang_items.append(ram_item)

                        enemies.remove(enemy)

        ram_boomerangs = [b for b in ram_boomerangs if not b.finished]

        if ram_evolved and segfault_event:
            trigger_crash = segfault_event.update(dt)

            if trigger_crash:
                screen_bounds = pygame.Rect(0, 0, WIDTH, HEIGHT)

                for enemy in enemies[:]:
                    enemy_screen_rect = pygame.Rect(
                        enemy.rect.x - camera_offset.x,
                        enemy.rect.y - camera_offset.y,
                        enemy.rect.width,
                        enemy.rect.height
                    )

                    if not screen_bounds.colliderect(enemy_screen_rect):
                        continue

                    died = enemy.take_damage(9999)

                    if died:
                        xp_gem = XPGem(enemy.rect.centerx, enemy.rect.centery)

                        if enemy.enemy_type == "fast":
                            xp_gem.value = 2
                        elif enemy.enemy_type == "tank":
                            xp_gem.value = 5

                        xp_gems.append(xp_gem)
                        enemies.remove(enemy)

        player_center = pygame.Vector2(
            player.rect.centerx,
            player.rect.centery
        )

        for gem in xp_gems[:]:
            distance = player_center.distance_to(gem.position)

            if distance < 30:
                leveled_up = player.gain_xp(gem.value)

                if leveled_up:
                    level_up_menu = True

                xp_gems.remove(gem)

        for item in orb_items[:]:
            distance = player_center.distance_to(item.position)

            if distance < 30:
                new_orb = OrbitingOrb(player)
                orbs.append(new_orb)

                redistribute_orbs()

                orb_items.remove(item)

        for item in ram_boomerang_items[:]:
            distance = player_center.distance_to(item.position)

            if distance < 30:
                ram_boomerang_level += 1

                if ram_boomerang_level >= 3 and not ram_evolved:
                    ram_evolved = True
                    segfault_event = SegFaultEvent()

                ram_boomerang_items.remove(item)

        if player.health <= 0:
            game_state = "game_over"

    screen.fill(BACKGROUND_COLOR)

    if game_state in ["playing", "paused", "game_over"]:
        grid_color = (40, 40, 40)

        offset_x = int(camera_offset.x % GRID_SIZE)
        offset_y = int(camera_offset.y % GRID_SIZE)

        for x in range(-GRID_SIZE, WIDTH + GRID_SIZE, GRID_SIZE):
            pygame.draw.line(
                screen,
                grid_color,
                (x - offset_x, 0),
                (x - offset_x, HEIGHT)
            )

        for y in range(-GRID_SIZE, HEIGHT + GRID_SIZE, GRID_SIZE):
            pygame.draw.line(
                screen,
                grid_color,
                (0, y - offset_y),
                (WIDTH, y - offset_y)
            )

        player.draw(screen, camera_offset)

        for orb in orbs:
            orb.draw(screen, camera_offset)

        for enemy in enemies:
            enemy.draw(screen, camera_offset)

        for projectile in projectiles:
            projectile.draw(screen, camera_offset)

        for boomerang in ram_boomerangs:
            boomerang.draw(screen, camera_offset)

        for gem in xp_gems:
            gem.draw(screen, camera_offset)

        for item in orb_items:
            item.draw(screen, camera_offset)

        for item in ram_boomerang_items:
            item.draw(screen, camera_offset)

        bar_width = 250
        bar_height = 25

        health_ratio = player.health / player.max_health

        pygame.draw.rect(screen, (100, 0, 0), (30, 20, bar_width, bar_height))

        pygame.draw.rect(screen, (255, 0, 0), (30, 20, bar_width * health_ratio, bar_height))

        xp_needed = player.level * 5
        xp_ratio = player.xp / xp_needed

        pygame.draw.rect(screen, (40, 40, 40), (30, 60, bar_width, 20))

        pygame.draw.rect(screen, (50, 150, 255), (30, 60, bar_width * xp_ratio, 20))

        level_text = font.render(f"Level {player.level}", True, (255, 255, 255))

        screen.blit(level_text, (30, 90))

        time_text = font.render(f"Time: {int(game_time)}s", True, (255, 255, 255))

        screen.blit(time_text, (30, 130))

        orb_text = font.render(f"Orbes: {len(orbs)}", True, (255, 255, 255))
        screen.blit(orb_text, (30, 170))

        ram_text = font.render(f"RAM Boomerang Lv: {ram_boomerang_level}", True, (255, 255, 255))
        screen.blit(ram_text, (30, 210))

        if ram_evolved and segfault_event:
            segfault_event.draw(screen, WIDTH, HEIGHT, font)

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

    if game_state == "menu":
        title = font.render("UOH SURVIVORS", True, (255, 255, 0))

        title_rect = title.get_rect(center=(WIDTH // 2, 180))

        screen.blit(title, title_rect)

        if selected_skin == 1:
            current_preview = menu_skin_1

        else:
            current_preview = menu_skin_2

        preview_rect = current_preview.get_rect(center=(WIDTH // 2, 300))

        screen.blit(current_preview, preview_rect)

        play_button = draw_button("Jugar",WIDTH // 2 - 150,420,300,60)

        skin_1_button = draw_button("Skin 1", WIDTH // 2 - 320, 640, 140, 50)
        skin_2_button = draw_button("Skin 2", WIDTH // 2 + 180, 640, 140, 50)

        quit_button = draw_button("Salir",WIDTH // 2 - 150,520,300,60)

        if pygame.mouse.get_pressed()[0]:

            if play_button.collidepoint(pygame.mouse.get_pos()):
                reset_game()
                game_state = "playing"

            elif quit_button.collidepoint(pygame.mouse.get_pos()):
                running = False

            elif skin_1_button.collidepoint(pygame.mouse.get_pos()):
                selected_skin = 1

            elif skin_2_button.collidepoint(pygame.mouse.get_pos()):
                selected_skin = 2

    if game_state == "paused":
        pause_text = font.render("PAUSA", True, (255, 255, 0))

        pause_rect = pause_text.get_rect(center=(WIDTH // 2, 180))

        screen.blit(pause_text, pause_rect)

        continue_button = draw_button("Continuar",WIDTH // 2 - 150,260,300,60)

        menu_button = draw_button("Menu Principal",WIDTH // 2 - 150,360,300,60)

        quit_button = draw_button("Salir",WIDTH // 2 - 150,460,300,60)

        if pygame.mouse.get_pressed()[0]:
            if continue_button.collidepoint(pygame.mouse.get_pos()):
                game_state = "playing"

            elif menu_button.collidepoint(pygame.mouse.get_pos()):
                game_state = "menu"

            elif quit_button.collidepoint(pygame.mouse.get_pos()):
                running = False

    if game_state == "game_over":
        over_text = font.render("GAME OVER", True, (255, 0, 0))

        over_rect = over_text.get_rect(center=(WIDTH // 2, 180))

        screen.blit(over_text, over_rect)

        retry_button = draw_button("Reintentar",WIDTH // 2 - 150,260,300,60)

        menu_button = draw_button("Menu Principal",WIDTH // 2 - 150,360,300,60)

        quit_button = draw_button("Salir",WIDTH // 2 - 150,460,300,60)

        if pygame.mouse.get_pressed()[0]:

            if retry_button.collidepoint(pygame.mouse.get_pos()):
                reset_game()
                game_state = "playing"

            elif menu_button.collidepoint(pygame.mouse.get_pos()):
                game_state = "menu"

            elif quit_button.collidepoint(pygame.mouse.get_pos()):
                running = False

    pygame.display.flip()

pygame.quit()
sys.exit()
