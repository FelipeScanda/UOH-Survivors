import pygame


class RAMBoomerang:
    def __init__(self, x, y, direction):
        self.width = 30
        self.height = 14

        self.position = pygame.Vector2(x, y)
        self.origin = pygame.Vector2(x, y)

        self.direction = direction

        self.speed = 350
        self.max_distance = 220

        self.state = "outgoing"

        self.rotation = 0
        self.rotation_speed = 360

        self.damage = 3

        self.hit_enemies_outgoing = []
        self.hit_enemies_returning = []

        self.color_outgoing = (0, 200, 0)
        self.color_returning = (200, 40, 40)

        self.finished = False

    def update(self, dt, player):
        if self.state == "outgoing":
            self.position += self.direction * self.speed * dt

            if self.origin.distance_to(self.position) >= self.max_distance:
                self.state = "returning"

        elif self.state == "returning":
            player_center = pygame.Vector2(player.rect.centerx, player.rect.centery)

            to_player = player_center - self.position

            if to_player.length() > 0:
                to_player = to_player.normalize()

            self.position += to_player * self.speed * dt

            if player_center.distance_to(self.position) < 20:
                self.finished = True

        self.rotation += self.rotation_speed * dt

    def get_rect(self):
        return pygame.Rect(
            self.position.x - self.width / 2,
            self.position.y - self.height / 2,
            self.width,
            self.height
        )

    def draw(self, screen, camera_offset):
        color = self.color_outgoing if self.state == "outgoing" else self.color_returning

        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surface, color, surface.get_rect())

        if self.state == "returning":
            pygame.draw.line(surface, (0, 0, 0), (5, 0), (self.width - 5, self.height), 2)
            pygame.draw.line(surface, (0, 0, 0), (0, self.height - 3), (self.width, 3), 2)

        rotated = pygame.transform.rotate(surface, self.rotation)
        rotated_rect = rotated.get_rect(center=(
            int(self.position.x - camera_offset.x),
            int(self.position.y - camera_offset.y)
        ))

        screen.blit(rotated, rotated_rect)
