import pygame


class XPGem:

    def __init__(self, x, y):

        #Tamaño de la experiencia
        self.radius = 8

        #Posicion de la experiencia
        self.position = pygame.Vector2(x, y)

        #Color
        self.color = (50, 150, 255)

        #Valor
        self.value = 1

    def draw(self, screen):

        #Dibujar experiencia
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.position.x), int(self.position.y)),
            self.radius
        )