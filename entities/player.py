import pygame

from settings import *


class Player:

    def __init__(self, x, y):

        # Tamaño del jugador
        self.width = 40
        self.height = 40

        # Rectángulo del jugador
        self.rect = pygame.Rect(x, y, self.width, self.height)

        # Velocidad
        self.speed = 300

        # Color
        self.color = (50, 200, 50)

        #Propiedades de disparo
        self.shoot_cooldown = 0.5
        self.shoot_timer = 0

        #Experiencia y nivel
        self.xp = 0
        self.level = 1

    def handle_movement(self, dt):

        # Obtener teclas presionadas
        keys = pygame.key.get_pressed()

        dx = 0
        dy = 0

        # Movimiento horizontal
        if keys[pygame.K_a]:
            dx = -1

        if keys[pygame.K_d]:
            dx = 1

        # Movimiento vertical
        if keys[pygame.K_w]:
            dy = -1

        if keys[pygame.K_s]:
            dy = 1

        # Crear vector de movimiento
        movement = pygame.Vector2(dx, dy)

        # Normalizar si hay movimiento
        if movement.length() > 0:
            movement = movement.normalize()

        # Aplicar movimiento usando delta time
        self.rect.x += dx * self.speed * dt
        self.rect.y += dy * self.speed * dt

    def shoot(self, enemies):

        # No disparar si no hay enemigos
        if not enemies:
            return None

        player_pos = pygame.Vector2(
            self.rect.centerx,
            self.rect.centery
        )

        # Buscar enemigo más cercano
        closest_enemy = min(
            enemies,
            key=lambda enemy: player_pos.distance_to(
                pygame.Vector2(
                    enemy.rect.centerx,
                    enemy.rect.centery
                )
            )
        )

        enemy_pos = pygame.Vector2(
            closest_enemy.rect.centerx,
            closest_enemy.rect.centery
        )

        # Dirección hacia enemigo
        direction = enemy_pos - player_pos

        if direction.length() > 0:
            direction = direction.normalize()

        return direction

    def draw(self, screen):

        pygame.draw.rect(screen, self.color, self.rect)