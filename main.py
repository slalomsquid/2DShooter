import pygame
from pygameUtils import *
import keybinds, constants
from player import Player
from enemy import Enemy
from bullet import Bullet

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
                        bullet = Bullet(player.x, player.y, player.rotation, 5)
                        bullets.append(bullet)
        
        # Input handling

        keys = pygame.key.get_pressed()
        if any(keys[k] for k in keybinds.exit):
            pygame.quit()
            running = False

        # Frame process logic

        player_surface = player.process(mouse_pos, mouse_rel, delta_time)
        enemy_surfaces = []
        
        for enemy in enemies:
            tmp_surface = enemy.process((player.x, player.y), delta_time)
            if tmp_surface:
                enemy_surfaces.append(tmp_surface)
        
        rect_map = {obj: obj.rect for obj in (blocks + enemies)}

        player.handle_movement(keys, delta_time, rect_map)
        player.sync_player()

        # Render logic

        for bullet in bullets:
            bullet.update_pos(rect_map, delta_time)
            if bullet.alive == False:
                bullets.remove(bullet)

        draw(player_surface, blocks, enemy_surfaces, mouse_pos, bullets, player, enemies)


if __name__ == "__main__":
    main()