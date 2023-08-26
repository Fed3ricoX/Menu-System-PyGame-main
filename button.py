import pygame

class Button():
    def __init__(self, text, position, size, callback, background_color, text_color, hovering_color):
        self.text = text
        self.rect = pygame.Rect(position, size)
        self.callback = callback
        self.background_color = background_color
        self.text_color = self.base_color= text_color
        self.hovering_color = hovering_color  # Cambia il nome dell'attributo

    def draw(self, screen):
        pygame.draw.rect(screen, self.background_color, self.rect)
        font = pygame.font.Font("assets/font.ttf", 10)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

    def change_color(self, position):
        if self.rect.collidepoint(position):
            self.text_color = self.hovering_color
        else:
            self.text_color = self.base_color
