from pygameUtils import *

class Enemy():
    def __init__(self, x, y, size_x, size_y, color=(255, 50, 50), texture=None, speed=200):
        super().__init__()
        self.rect = pygame.Rect(x, y, size_x, size_y)
        self.x = self.rect.centerx
        self.y = self.rect.centery
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

    def process(self, player_pos, delta_time, offset_x, offset_y):
        self.target_rotation = vector_to_angle(np.array(player_pos) - np.array([self.x, self.y]))
        self.rotation = move_towards_angle(self.rotation, self.target_rotation, self.max_rotation_speed * delta_time)
        # self.rotation = lerp_angle(self.rotation, self.target_rotation, delta_time*2)
    
    def hit(self, damage):
        print("Hit")
        # self.health -= damage
        # if self.health <= 0:
        #     # Handle enemy death (e.g., remove from game, play animation, etc.)
        #     pass

    def draw(self, offset_x, offset_y):

        # Create temporary overlay to allow transparency
        surface = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)

        poly = create_view_cone_polygon(self)

        poly = [(px - offset_x, py - offset_y) for (px, py) in poly]

        pygame.draw.polygon(surface, (255, 255, 255, 50), poly)
        
        draw_rotated_rect(surface, self.color, (self.x - self.size_x//2 - offset_x, self.y - self.size_y//2 - offset_y, self.size_x, self.size_y), self.rotation, (self.x, self.y))

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