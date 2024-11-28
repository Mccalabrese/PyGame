import pygame
pygame.init()

class Button(pygame.sprite.Sprite):
    def __init__(self, colorOn, colorOff, bell, xCor, yCor):
        pygame.sprite.Sprite.__init__(self)
        self.colorOn = colorOn
        self.colorOff = colorOff
        self.bell = bell
        self.xCor = xCor
        self.yCor = yCor

        self.image = pygame.Surface((100, 100))
        self.image.fill(self.colorOff)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.xCor, self.yCor)
        self.clicked = False

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def selected(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.clicked = True
            return True
        return False

    def update(self, screen):
        self.image.fill(self.colorOn)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.bell is not None:
            self.bell.play()  # Play sound immediately when button is illuminated
        pygame.display.update()
        pygame.time.wait(500)
        self.image.fill(self.colorOff)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        pygame.display.update()