from pygameUtils import *

class Enemy():
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
        self.max_rotation_speed = 180
        self.health = 100
        self.view_distance = 100
        self.fov = 60
        self.view_cone = create_view_cone_polygon(self)
        self.time_since_seen = 10
        self.last_seen_player_pos = False
        self.times_checked = 0
        self.sprite_direction = "left"
        self.animation_count = 0
        self.ANIMATION_DELAY = 3
        self.SPRITES = sprite
        self.attacked = False
        self.vel = "idle"
        self.hit_count = 0

    def process(self, player_pos, delta_time, offset_x, offset_y):
        if is_point_in_triangle(player_pos, self.view_cone[0], self.view_cone[1], self.view_cone[2]):
            self.time_since_seen = 0.0
            self.last_seen_player_pos = player_pos
            self.times_checked = 0
            self.target_rotation = vector_to_angle(np.array(player_pos) - np.array([self.x, self.y]))
        else:
            if self.time_since_seen < 10:
                # Check if last seen exists
                if self.last_seen_player_pos:
                    if self.times_checked == 0 or 3:
                        self.target_rotation = vector_to_angle(np.array(self.last_seen_player_pos) - np.array([self.x, self.y]))
                    if self.times_checked == 1:
                        self.target_rotation = vector_to_angle(np.array(self.last_seen_player_pos) - np.array([self.x, self.y])) + 30
                    if self.times_checked == 2:
                        self.target_rotation = vector_to_angle(np.array(self.last_seen_player_pos) - np.array([self.x, self.y])) - 30
                    if self.times_checked == 4:
                        self.target_rotation = vector_to_angle(np.array(self.last_seen_player_pos) - np.array([self.x, self.y])) + 180
                if self.rotation == self.target_rotation:
                    self.times_checked += 1
                # if self.rotation == self.target_rotation:
                #     self.target_rotation += 180
        self.rotation = move_towards_angle(self.rotation, self.target_rotation, self.max_rotation_speed * delta_time)
        self.time_since_seen += delta_time
    
    def hit(self, damage):
        self.attacked = True
        print("Hit")
        # self.health -= damage
        # if self.health <= 0:
        #     # Handle enemy death (e.g., remove from game, play animation, etc.)
        #     pass

    def update_sprite(self, fps):
        sprite_sheet = "idle"
        if self.attacked:
            sprite_sheet = "hit"

        elif self.vel != "idle":
            sprite_sheet = "run"
        
        if self.hit:
            self.hit_count += 1 
        if self.hit_count > fps * 5:
            self.attacked = False
            self.hit_count = 0
        
        sprite_sheet_name = sprite_sheet + "_" + self.sprite_direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count // self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1

        self.update()

    def update(self):
        self.rect.center = (self.x, self.y)
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, offset_x, offset_y):

        # Create temporary overlay to allow transparency
        surface = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)

        self.view_cone = create_view_cone_polygon(self)

        poly = [(px - offset_x, py - offset_y) for (px, py) in self.view_cone]

        pygame.draw.polygon(surface, (255, 255, 255, 50), poly)

        #draw_rotated_rect(surface, self.color, (self.x - self.size_x//2 - offset_x, self.y - self.size_y//2 - offset_y, self.size_x, self.size_y), self.rotation, (self.x - offset_x, self.y - offset_y))
        surface.blit(self.sprite, (self.rect.x - offset_x, self.rect.y - offset_y))

        return surface

        draw_rect = pygame.Rect(
        self.rect.x - offset_x,
        self.rect.y - offset_y,
        self.rect.width,
        self.rect.height
    )
        pygame.draw.rect(screen, self.color, draw_rect)

if __name__ == "__main__":
    print("This is a utility file, not meant to be run directly")