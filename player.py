import constants, keybinds
from pygameUtils import *

class Player():

    def __init__(self, x, y, size_x, size_y, sprite, color=(255, 50, 50), texture=None, speed=200):
        super().__init__()
        self.rect = pygame.Rect(x, y, size_x, size_y)
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.color = color
        self.texture = texture
        self.speed = speed
        self.rotation = 0
        self.target_rotation = 0
        self.max_rotation_speed = 360
        self.health = 100
        self.view_distance = 100
        self.fov = 60
        self.walk_to_mouse = False
        self.sprite_direction = "left"
        self.animation_count = 0
        self.ANIMATION_DELAY = 3
        self.SPRITES = sprite
        self.hit = False
        self.vel = "idle"
        self.hit_count = 0

    def handle_movement(self, keys, delta_time, rectangles):
        dx = 0
        dy = 0

        speed = self.speed * delta_time

        forward = angle_to_vector(self.rotation)
        strafe = angle_to_vector(self.rotation - 90)

        self.vel = "idle"

        if keys [pygame.K_LSHIFT]:
            self.walk_to_mouse = True
        else:
            self.walk_to_mouse = False

        if any(keys[k] for k in keybinds.up):
            if self.walk_to_mouse:
                dx += forward[0] * speed
                dy += forward[1] * speed
            else:
                dy -= speed
        if any(keys[k] for k in keybinds.down):
            if self.walk_to_mouse:
                dx -= forward[0] * speed
                dy -= forward[1] * speed
            else:
                dy += speed
        if any(keys[k] for k in keybinds.left):
            if self.sprite_direction != "left":
                self.sprite_direction = "left"
            if self.walk_to_mouse:
                dx += strafe[0] * speed
                dy += strafe[1] * speed
            else:
                dx -= speed
        if any(keys[k] for k in keybinds.right):
            if self.sprite_direction != "right":
                self.sprite_direction = "right"
            if self.walk_to_mouse:
                dx += strafe[0] * speed
                dy += strafe[1] * speed
            else:
                dx += speed

        # Try X movement
        if dx != 0:
            new_rect = self.rect.move(dx, 0)
            if not any(obj.colliderect(new_rect) for obj in rectangles.values()):
                self.x += dx
                self.vel = "moving"

        # Try Y movement
        if dy != 0:
            new_rect = self.rect.move(0, dy)
            if not any(obj.colliderect(new_rect) for obj in rectangles.values()):
                self.y += dy
                self.vel = "moving"

        self.rect.center = (self.x, self.y)
        
    def handle_mouse(self, mouse_pos, mouse_rel, delta_time):
        pass
        # self.target_rotation = vector_to_angle(np.array(mouse_pos) - np.array([self.x, self.y]))
        # self.rotation = move_towards_angle(self.rotation, self.target_rotation, self.max_rotation_speed * delta_time)
        # # self.rotation = lerp_angle(self.rotation, self.target_rotation, delta_time*2)

    def process(self, mouse_pos, mouse_rel, offset_x, offset_y, delta_time):
        self.target_rotation = vector_to_angle(np.array(mouse_pos) - np.array([self.x, self.y]))
        self.rotation = move_towards_angle(self.rotation, self.target_rotation, self.max_rotation_speed * delta_time)
        # self.rotation = lerp_angle(self.rotation, self.target_rotation, delta_time*2)

        view_left = self.rotation - 30
        view_right = self.rotation + 30

        view_left_strafe = angle_to_vector(view_left)
        view_right_strafe = angle_to_vector(view_right)

        # Create temporary overlay to allow transparency
    
    def update_sprite(self, fps):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"

        elif self.vel != "idle":
            sprite_sheet = "run"

        if self.hit:
            self.hit_count += 1 
        if self.hit_count > fps * 5:
            self.hit = False
            self.hit_count = 0
        
        sprite_sheet_name = sprite_sheet + "_" + self.sprite_direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
    
    def draw(self, offset_x, offset_y):

        surface = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
        
        poly = create_view_cone_polygon(self)

        poly = [(px - offset_x, py - offset_y) for (px, py) in poly]

        pygame.draw.polygon(surface, (255, 255, 255, 50), poly)

        surface.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))

        return surface
    
    def sync_player(self):
        self.rect.center = (self.x, self.y)

if __name__ == "__main__":
    print("This is a utility file, not meant to be run directly")