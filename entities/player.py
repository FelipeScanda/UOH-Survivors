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

        # Aplicar movimiento usando delta time
        self.rect.x += dx * self.speed * dt
        self.rect.y += dy * self.speed * dt

    def draw(self, screen):

        pygame.draw.rect(screen, self.color, self.rect)