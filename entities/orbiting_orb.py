import pygame
import math

class OrbitingOrb:
    def __init__(self, player):
        #Jugador que tiene el arma
        self.player = player
        #Radio de los orbes
        self.radius = 12
        #Distancia de giro
        self.distance = 100
        #Angulo de giro
        self.angle = 0
        #Velocidad de rotacion
        self.rotation_speed = 3
        #Daño
        self.damage = 1
        #Color
        self.color = (0, 255, 255)
        #Posicion
        self.position = pygame.Vector2()

    def update(self, dt):
        # Rotar
        self.angle += self.rotation_speed * dt

        # Posición alrededor del jugador
        x = (
            self.player.rect.centerx +
            math.cos(self.angle) * self.distance
        )

        y = (
            self.player.rect.centery +
            math.sin(self.angle) * self.distance
        )

        self.position.x = x
        self.position.y = y

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.position.x), int(self.position.y)),
            self.radius
        )