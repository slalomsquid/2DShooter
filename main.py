import pygame
from pygameUtils import *
import keybinds
from player import Player

pygame.init()
clock = pygame.time.Clock()
FPS = 60

WIDTH, HEIGHT = 500, 400
ORIGIN = [WIDTH//2, HEIGHT//2]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Platformer Example")

class Block():
    def __init__(self, x, y, size_x, size_y, color=(0, 255, 255), texture=None):
        super().__init__()
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.color = color
        self.texture = texture

blocks = [Block(100, 100, 50, 50), Block(200, 150, 50, 50)]

player = Player(ORIGIN[0], ORIGIN[1], 20, 20)

mouse_pos = (0, 0)
mouse_rel = (0, 0)

running = True

while running:

    delta_time = clock.tick(FPS) / 1000.0

    # Event handling

    for event in pygame.event.get():
        match event.type:
            # Use a switch statment because its more effieient and easier to read than ifs
            case pygame.QUIT:
                running = False
            case pygame.MOUSEMOTION:
                mouse_pos = event.pos
                mouse_rel = event.rel
            # case pygame.KEYDOWN:
            #     if event.key in keybinds.exit:
            #         running = False
            #     elif event.key in keybinds.up:
            #         # handle up
            #         player.y -= 10
            #     elif event.key in keybinds.down:
            #         # handle down
            #         player.y += 10
            #     elif event.key in keybinds.left:
            #         # handle left
            #         player.x -= 10
            #     elif event.key in keybinds.right:
            #         # handle right
            #         player.x += 10
    
    # Input handling

    keys = pygame.key.get_pressed()

    player.handle_keys(keys, delta_time)

    player.handle_mouse(mouse_pos, mouse_rel)

    # Frame process logic

    view_left = player.rotation - 30
    view_right = player.rotation + 30

    view_left_direction = angle_to_vector(view_left)
    view_right_direction = angle_to_vector(view_right)

    # Render logic

    screen.fill((0, 0, 0))

    for block in blocks:
        pygame.draw.rect(screen, block.color, (block.x, block.y, block.size_x, block.size_y))

    # pygame.draw.polygon(screen, (255, 255, 255, 10), [(player.x + 10, player.y + 10), (player.x + 10 + view_left_direction[0]*player.view_distance, player.y + 10 + view_left_direction[1]*player.view_distance), (player.x + 10 + view_right_direction[0]*player.view_distance, player.y + 10 + view_right_direction[1]*player.view_distance)])

    pygame.draw.rect(screen, player.color, (player.x - player.size_x//2, player.y - player.size_y//2, player.size_x, player.size_y))

    pygame.draw.circle(screen, (255, 255, 255), mouse_pos, 5)

    # Create temporary overlay to allow transparency
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    points = [
        (player.x, player.y), 
        (player.x + view_left_direction[0]*player.view_distance, player.y + view_left_direction[1]*player.view_distance), 
        (player.x + view_right_direction[0]*player.view_distance, player.y + view_right_direction[1]*player.view_distance)
    ]
    pygame.draw.polygon(overlay, (255, 255, 255, 50), points)

    # 3. Draw the temporary surface onto the main screen
    screen.blit(overlay, (0, 0))

    pygame.display.update()