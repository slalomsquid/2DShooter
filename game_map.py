import constants
from pygameUtils import *

class Game_Map():
    def __init__(self, array, size, color=(0, 255, 255), texture=None):
        super().__init__()
        self.raw_rects = get_rectangles(array, size)
        self.rects = [pygame.Rect(r) for r in self.raw_rects]
        self.color = color
        self.texture = texture
    
    def draw(self, offset_x, offset_y):
                
        surface = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)

        for rect in self.rects:
            moved_rect = (rect[0]-offset_x, rect[1]-offset_y, rect[2], rect[3])
            pygame.draw.rect(surface, constants.BLUE, moved_rect)

        return surface