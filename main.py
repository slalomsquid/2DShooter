import constants, keybinds, pygame
from pygameUtils import *
from player import Player
from enemy import Enemy
from bullet import Bullet
from block import Block
from game_map import Game_Map

pygame.init()
clock = pygame.time.Clock()

SCREEN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Platformer Example")

def draw(game_map = None, blocks=[], enemies=[], bullets=[], player=None, offset_x=0, offset_y=0):
        SCREEN.fill(constants.BLACK)

        surfaces = []

        if (new_surf := game_map.draw(offset_x, offset_y)): 
            surfaces.append(new_surf)

        for block in blocks:
            if (new_surf := block.draw(offset_x, offset_y)): 
                surfaces.append(new_surf)

        for enemy in enemies:
            if (new_surf := enemy.draw(offset_x, offset_y)): 
                surfaces.append(new_surf)

        if (new_surf := player.draw(offset_x, offset_y)): 
            surfaces.append(new_surf)

        for bullet in bullets[:]:
            if (new_surf := bullet.draw(offset_x, offset_y)): 
                surfaces.append(new_surf)

        for surface in surfaces:
            if surface:
                SCREEN.blit(surface, (0, 0))

        pygame.display.update()

def main():

    offset_x = 0
    offset_y = 0

    map_array = [
        [0,1,1,1,1,1,1,1,1,1,1],
        [0,1,0,0,0,0,0,0,0,0,1],
        [0,1,0,0,0,0,0,0,0,0,1],
        [0,1,0,0,0,0,0,0,0,0,1],
        [0,1,0,0,0,0,0,0,0,0,1],
        [0,1,1,1,1,0,0,0,0,1,1]
    ]

    game_map = Game_Map(map_array, 10, constants.BLUE)

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
                    mouse_pos = [event.pos[0] + offset_x, event.pos[1] + offset_y]
                    mouse_rel = event.rel
                    player.handle_mouse(mouse_pos, mouse_rel, delta_time)       
                case pygame.KEYDOWN:
                    if any(event.key == key for key in keybinds.shoot):
                        bullet = Bullet(player.rect.centerx, player.rect.centery, player.rotation, 5)
                        bullets.append(bullet)

                    if event.key == pygame.K_SPACE:
                        pass

        
        # Input handling

        keys = pygame.key.get_pressed()
        if any(keys[k] for k in keybinds.exit):
            pygame.quit()
            running = False

        # Frame process logic

        # Process enemies
        for enemy in enemies:
            enemy.process((player.x, player.y), delta_time, offset_x, offset_y) 
        
        rect_map = {obj: obj.rect for obj in (blocks + enemies)}

        for i, rect in enumerate(game_map.rects):
            rect_map[f"tile_{i}"] = rect

        old_x, old_y = player.x, player.y

        player.handle_movement(keys, delta_time, rect_map)

        actual_dx = player.x - old_x
        actual_dy = player.y - old_y

        # Horizontal Scroll
        # Subtract offset to get screen pos
        if player.x - offset_x < constants.SCROLL_MARGIN and actual_dx < 0:
            # Only move offset if player is at the LEFT margin and moving LEFT
            offset_x += actual_dx
            mouse_pos[0] += actual_dx
        elif player.x - offset_x > constants.WIDTH - constants.SCROLL_MARGIN and actual_dx > 0:
            # Only move offset if player is at the RIGHT margin and moving RIGHT
            offset_x += actual_dx
            mouse_pos[0] += actual_dx

        # Vertical Scroll
        if player.y - offset_y < constants.SCROLL_MARGIN and actual_dy < 0:
            # Only move offset if player is at the TOP margin and moving UP
            offset_y += actual_dy
            mouse_pos[1] += actual_dy
        elif player.y - offset_y > constants.HEIGHT - constants.SCROLL_MARGIN and actual_dy > 0:
            # Only move offset if player is at the BOTTOM margin and moving DOWN
            offset_y += actual_dy
            mouse_pos[1] += actual_dy

        player.process(mouse_pos, mouse_rel, offset_x, offset_y, delta_time=delta_time)

        for bullet in bullets[:]:
            bullet.process(delta_time)
            hit_rect = bullet.rect.collidedict(rect_map, 1)
            if hit_rect:
                    # hit_rect[1] is the rect, hit_rect[0] is the object
                    hit_object = hit_rect[0]
                    hit_method = getattr(hit_object, "hit", None)
                    if hit_method and callable(hit_method):
                        hit_method(bullet.velocity)
                    # Delete on collision
                    bullets.remove(bullet)
                    # Brevents rare instance where bullet is removed twice causing crash
                    break
            if bullet.traveled > bullet.max_dist:
                bullets.remove(bullet)

        # Render logic

        draw(game_map=game_map, player=player, enemies=enemies, blocks=blocks, bullets=bullets, offset_x=offset_x, offset_y=offset_y)

if __name__ == "__main__":
    main()