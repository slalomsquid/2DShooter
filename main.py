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
        self.rect = pygame.Rect(x, y, size_x, size_y)
        self.size_x = size_x
        self.size_y = size_y
        self.color = color
        self.texture = texture

def bullet_movement(bullets):
    for bullet in bullets[:]:
        bullet.x += 5

def handle_movement(player, rectangles, keys):
    dx = 0
    dy = 0

    if any(keys[k] for k in keybinds.up):
        dy -= 5
    if any(keys[k] for k in keybinds.down):
        dy += 5
    if any(keys[k] for k in keybinds.left):
        dx -= 5
    if any(keys[k] for k in keybinds.right):
        dx += 5

    # Try X movement
    if dx != 0:
        new_rect = player.rect.move(dx, 0)
        if not any(obj.colliderect(new_rect) for obj in rectangles):
            player.rect = new_rect

    # Try Y movement
    if dy != 0:
        new_rect = player.rect.move(0, dy)
        if not any(obj.colliderect(new_rect) for obj in rectangles):
            player.rect = new_rect

def draw(player_surface, blocks, enemy_surfaces, mouse_pos, bullets, player, enemies):
    screen.fill((0, 0, 0))
    for block in blocks:
        pygame.draw.rect(screen, block.color, block.rect)

    pygame.draw.rect(screen, "red", player.rect)
    for enemy in enemies:
        pygame.draw.rect(screen, "red", enemy.rect)
    screen.blit(player_surface, (0, 0))

    for enemy_surface in enemy_surfaces:
        screen.blit(enemy_surface, (0, 0))
    
    for bullet in bullets:
        pygame.draw.rect(screen, "white", bullet)

    pygame.draw.circle(screen, (255, 255, 255), mouse_pos, 5)

    render_text(f"FPS: {int(clock.get_fps())}", (0, 0), constants.WHITE, screen, size=30)

    pygame.display.update()

def main():

    blocks = [Block(100, 100, 50, 50), Block(200, 150, 50, 50)]

    enemies = [Enemy(constants.ORIGIN[0]+50, constants.ORIGIN[1], 20, 20)]

    player = Player(constants.ORIGIN[0]+20, constants.ORIGIN[1], 20, 20)

    bullets = []

    rectangles = []

    mouse_pos = (0, 0)
    mouse_rel = (0, 0)

    running = True

    while running:

        delta_time = clock.tick(constants.FPS) / 1000.0

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
                case pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullet = pygame.Rect(player.x, player.y, 10, 5)
                        bullets.append(bullet)
        
        # Input handling
        held_actions = []

        if held_actions:
            if "exit" in held_actions:
                running = False
        keys = pygame.key.get_pressed()
        if any(keys[k] for k in keybinds.exit):
            held_actions.append("exit")
        if any(keys[k] for k in keybinds.shift):
            held_actions.append("shift")

        # Frame process logic

        player_surface = player.process(mouse_pos, mouse_rel, delta_time)

        enemy_surfaces = []

        for enemy in enemies:
            tmp_surface = enemy.process((player.x, player.y), delta_time)
            if tmp_surface:
                enemy_surfaces.append(tmp_surface)
        
        rectangles = [block.rect for block in blocks] + [enemy.rect for enemy in enemies]

        # Render logic
        handle_movement(player, rectangles, keys)
        player.sync_player()
        bullet_movement(bullets)
        draw(player_surface, blocks, enemy_surfaces, mouse_pos, bullets, player, enemies)


if __name__ == "__main__":
    main()

