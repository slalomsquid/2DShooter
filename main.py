import pygame
from pygameUtils import *
import keybinds
from player import Player
from enemy import Enemy
import constants

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
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

# Only run if is the ran file, not if imported as a module
if __name__ == "__main__":

    blocks = [Block(100, 100, 50, 50), Block(200, 150, 50, 50)]

    enemies = [Enemy(300, 300, 20, 20)]

    player = Player(constants.ORIGIN[0]+20, constants.ORIGIN[1], 20, 20)

    mouse_pos = (0, 0)
    mouse_rel = (0, 0)

    running = True

    while running:

        delta_time = clock.tick(constants.FPS) / 1000.0

        # Pre frame logic

        old_x, old_y = player.x, player.y
        player_moved = False

        # Event handling

        for event in pygame.event.get():
            match event.type:
                # Use a switch statment because its more effieient and easier to read than ifs
                case pygame.QUIT:
                    running = False
                case pygame.MOUSEMOTION:
                    mouse_pos = event.pos
                    mouse_rel = event.rel
                    player.handle_mouse(mouse_pos, mouse_rel, delta_time)
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

        actions = []

        held_actions = []

        if any(keys[k] for k in keybinds.exit):
            held_actions.append("exit")
        if any(keys[k] for k in keybinds.up):
            held_actions.append("up")
        if any(keys[k] for k in keybinds.down):
            held_actions.append("down")
        if any(keys[k] for k in keybinds.left):
            held_actions.append("left")
        if any(keys[k] for k in keybinds.right):
            held_actions.append("right")

        if held_actions:
            if "exit" in held_actions:
                running = False


            player_moved = player.handle_held(held_actions, delta_time)

        # Frame process logic

        player_surface = player.process(mouse_pos, mouse_rel, delta_time)

        for enemy in enemies:
            enemy.process((player.x, player.y), delta_time)

        # Move collision from individual classes
        for block in blocks:
            if player_moved:
                if player.x + player.size_x//2 > block.x and player.x - player.size_x//2 < block.x + block.size_x and player.y + player.size_y//2 > block.y and player.y - player.size_y//2 < block.y + block.size_y:
                    player.x, player.y = old_x, old_y
                    break

        # Render logic

        screen.fill((0, 0, 0))

        for block in blocks:
            pygame.draw.rect(screen, block.color, (block.x, block.y, block.size_x, block.size_y))

        screen.blit(player_surface, (0, 0))

        pygame.draw.circle(screen, (255, 255, 255), mouse_pos, 5)

        render_text(f"FPS: {int(clock.get_fps())}", (0, 0), constants.WHITE, screen, size=30)

        pygame.display.update()