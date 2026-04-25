import pygame
from pygameUtils import *
import keybinds, constants
from player import Player
from enemy import Enemy
from bullet import Bullet

pygame.init()
clock = pygame.time.Clock()

SCREEN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Platformer Example")

class Block():
    def __init__(self, x, y, size_x, size_y, color=(0, 255, 255), texture=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, size_x, size_y)
        self.size_x = size_x
        self.size_y = size_y
        self.color = color
        self.texture = texture
    
    def draw(self, offset_x, offset_y):
        draw_rect = pygame.Rect(
        self.rect.x - offset_x,
        self.rect.y - offset_y,
        self.rect.width,
        self.rect.height
    )
        pygame.draw.rect(SCREEN, self.color, draw_rect)
    

def draw(player_surface, blocks, enemy_surfaces, mouse_pos, bullets, player, enemies, offset_x, offset_y):
    SCREEN.fill((0, 0, 0))
    for block in blocks:
        block.draw(offset_x, offset_y)

    player.draw(SCREEN, offset_x, offset_y)

    for enemy in enemies:
        enemy.draw(SCREEN, offset_x, offset_y)

    SCREEN.blit(player_surface, (0, 0))

    for enemy_surface in enemy_surfaces:
        SCREEN.blit(enemy_surface, (0, 0))
    
    for bullet in bullets:
        bullet.draw(offset_x, offset_y, SCREEN)

    pygame.draw.circle(SCREEN, (255, 255, 255), mouse_pos, 5)

    render_text(f"FPS: {int(clock.get_fps())}", (0, 0), constants.WHITE, SCREEN, size=30)

    pygame.display.update()

def main():
    offset_x = 0
    offset_y = 0
    blocks = [Block(100, 100, 50, 50), Block(200, 150, 50, 50)]

    enemies = [Enemy(constants.ORIGIN[0]+50, constants.ORIGIN[1], 20, 20)]

    player = Player(constants.ORIGIN[0]+20, constants.ORIGIN[1], 20, 20)

    bullets = []

    mouse_pos = (0, 0)
    mouse_rel = (0, 0)

    scroll_area_width = 200

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

        player_surface = player.process(mouse_pos, mouse_rel, delta_time, offset_x, offset_y)
        enemy_surfaces = []
        
        for enemy in enemies:
            tmp_surface = enemy.process((player.x, player.y), delta_time, offset_x, offset_y)
            if tmp_surface:
                enemy_surfaces.append(tmp_surface)
            
        if ((player.rect.right - offset_x >= constants.WIDTH - scroll_area_width) and player.x_vel > 0 ) or ((player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel
        if ((player.rect.top - offset_y >= constants.HEIGHT - scroll_area_width) and player.y_vel > 0 ) or ((player.rect.bottom - offset_y <= scroll_area_width) and player.y_vel < 0):
            offset_y += player.y_vel

        
        rect_map = {obj: obj.rect for obj in (blocks + enemies)}

        player.handle_movement(keys, delta_time, rect_map)
        player.sync_player()

        # Render logic

        for bullet in bullets:
            bullet.update_pos(rect_map, delta_time)
            if bullet.alive == False:
                bullets.remove(bullet)

        draw(player_surface, blocks, enemy_surfaces, mouse_pos, bullets, player, enemies, offset_x, offset_y)



if __name__ == "__main__":
    main()