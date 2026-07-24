import pygame

class RamBoomerangItem:
    def __init__(self, x, y):
        #Posicion
        self.position = pygame.Vector2(x, y)
        #Tamaño del item
        self.width = 20
        self.height = 20
        #Color
        self.color = (0, 200, 0)

    def draw(self, screen, camera_offset):
        rect = pygame.Rect(
            int(self.position.x - camera_offset.x - self.width / 2),
            int(self.position.y - camera_offset.y - self.height / 2),
            self.width,
            self.height
        )

        pygame.draw.rect(screen, self.color, rect)
