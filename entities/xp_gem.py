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

    def draw(self, screen, camera_offset):

        #Dibujar experiencia
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.position.x - camera_offset.x), int(self.position.y - camera_offset.y)),
            self.radius
        )