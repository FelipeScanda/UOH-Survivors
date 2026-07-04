import pygame

class OrbItem:
    def __init__(self, x, y):
        #Posicion
        self.position = pygame.Vector2(x, y)
        #Radio del item
        self.radius = 10
        #Color
        self.color = (0, 255, 255)

    def draw(self, screen, camera_offset):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.position.x - camera_offset.x), int(self.position.y - camera_offset.y)),
            self.radius
        )