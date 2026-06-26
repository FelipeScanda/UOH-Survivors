import pygame


class Projectile:

    def __init__(self, x, y, direction):

        #Tamaño del proyectil
        self.radius = 5

        #Posicion del proyectil usando un vector 2D
        self.position = pygame.Vector2(x, y)

        #Direccion en la que viaja el proyectil
        self.direction = direction

        #Velocidad
        self.speed = 500

        #Color
        self.color = (255, 255, 0)

    def update(self, dt):

        #Movimiento del proyectil
        self.position += self.direction * self.speed * dt

    def draw(self, screen):

        #Dibujar el proyectil en pantalla
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.position.x), int(self.position.y)),
            self.radius
        )