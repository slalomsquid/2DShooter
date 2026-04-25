from pygameUtils import *
import constants

class Block():
    def __init__(self, x, y, size_x, size_y, color=(0, 255, 255), texture=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, size_x, size_y)
        self.size_x = size_x
        self.size_y = size_y
        self.color = color
        self.texture = texture
    
    def draw(self, offset_x, offset_y):

        surface = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)

        draw_rect = pygame.Rect(self.rect.x - offset_x, self.rect.y - offset_y, self.rect.width, self.rect.height)

        pygame.draw.rect(surface, self.color, draw_rect)

        return surface