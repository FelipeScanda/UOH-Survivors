import pygame
import random

from settings import *


class Enemy:

    def __init__(self, x, y, enemy_type="normal"):

        self.enemy_type = enemy_type
        
        #Enemigo normal
        if enemy_type == "normal":
            #Tamaño del enemigo
            self.width = 30
            self.height = 30

            #Velocidad
            self.speed = 150

            #Color
            self.color = (200, 50, 50)

            #Vida
            self.health = 3

        #Enemigo fast
        elif enemy_type == "fast":
            #Tamaño del enemigo
            self.width = 20
            self.height = 20

            #Velocidad
            self.speed = 260

            #Color
            self.color = (255, 140, 0)

            #Vida
            self.health = 1

        #Enemigo tank
        elif enemy_type == "tank":
            #Tamaño del enemigo
            self.width = 50
            self.height = 50

            #Velocidad
            self.speed = 80

            #Color
            self.color = (120, 0, 120)

            #Vida
            self.health = 8

        #Rectángulo del enemigo
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self, player, dt):

        # Posición jugador
        player_pos = pygame.Vector2(
            player.rect.centerx,
            player.rect.centery
        )

        # Posición enemigo
        enemy_pos = pygame.Vector2(
            self.rect.centerx,
            self.rect.centery
        )

        # Dirección hacia jugador
        direction = player_pos - enemy_pos

        # Normalizar
        if direction.length() > 0:
            direction = direction.normalize()

        # Mover enemigo
        self.rect.x += direction.x * self.speed * dt
        self.rect.y += direction.y * self.speed * dt

    def take_damage(self, amount):
        
        #Resta vida al enemigo
        self.health -= amount

        #Retorna si la vida es menor a 0 o no
        return self.health <= 0

    def draw(self, screen):

        pygame.draw.rect(screen, self.color, self.rect)