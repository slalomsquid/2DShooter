import pygame
from pygameUtils import *
import keybinds

WIDTH, HEIGHT = 500, 400
ORIGIN = [WIDTH//2, HEIGHT//2]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Example")

class Block():
    def __init__(self, x, y, sx, sy):
        super().__init__()
        self.x = x
        self.y = y
        self.sx = sx
        self.sy = sy
        self.color = (0, 255, 255)

blocks = [Block(100, 100, 50, 50), Block(200, 150, 50, 50)]

running = True

while running:
    for event in pygame.event.get():
        match event.type:
            # Use a switch statment because its more effieient and easier to read than ifs
            case pygame.QUIT:
                running = False
            case pygame.KEYDOWN:
                if event.key in keybinds.exit:
                    running = False
                elif event.key in keybinds.up:
                    # handle up
                    pass

                # match event.key:
                #     case keybinds.exit:
                #         running = False
                #     case keybinds.up:
                #         pass
                #     case keybinds.down:
                #         pass
                #     case keybinds.left:
                #         pass
                #     case keybinds.right:
                #         pass

    screen.fill((0, 0, 0))

    for block in blocks:
        pygame.draw.rect(screen, block.color, (block.x, block.y, block.sx, block.sy))

    pygame.display.flip()