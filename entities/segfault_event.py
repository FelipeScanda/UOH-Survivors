import pygame
import random


class SegFaultEvent:
    def __init__(self):
        self.cooldown = 8
        self.timer = self.cooldown

        self.flash_duration = 0.5
        self.flash_timer = 0

        self.active = False

        self.messages = [
            "SIGSEGV",
            "0xC0000005",
            "core dumped",
            "stack overflow",
            "malloc(): invalid pointer"
        ]

        self.current_message = ""

    def update(self, dt):
        should_trigger = False

        if not self.active:
            self.timer -= dt

            if self.timer <= 0:
                self.active = True
                self.flash_timer = self.flash_duration
                self.current_message = random.choice(self.messages)
                should_trigger = True

        else:
            self.flash_timer -= dt

            if self.flash_timer <= 0:
                self.active = False
                self.timer = self.cooldown

        return should_trigger

    def draw(self, screen, width, height, font):
        if not self.active:
            return

        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        border_color = (255, 0, 0) if random.random() < 0.5 else (0, 255, 0)
        pygame.draw.rect(screen, border_color, (0, 0, width, height), 6)

        error_text = font.render(self.current_message, True, (255, 0, 0))
        screen.blit(error_text, (20, height - 60))
