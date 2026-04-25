from pygameUtils import *
import constants

class Bullet():
    def __init__(self, x, y, rotation, radius, color=(255, 255, 0), texture=None, velocity=300):
        super().__init__()
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.texture = texture
        self.velocity = velocity
        self.rotation = rotation

    def process(self, delta_time):
        self.x, self.y = move_at_angle(np.array([self.x, self.y]), self.rotation, self.velocity * delta_time)
        self.rect.center = (self.x, self.y)
        # Use 1 to invert the values because rect cannot be hashed but object can
        # hit_rect = self.rect.collidedict(rectangle_dictionary, 1)
        # if hit_rect:
        #         # hit_rect[1] is the rect, hit_rect[0] is the object
        #         self.alive = False
        #         hit_object = hit_rect[0]
        #         hit_method = getattr(hit_object, "hit", None)
        #         if hit_method and callable(hit_method):
        #             hit_method(self.velocity)

    def draw(self, offset_x, offset_y):
         
        surface = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
    
        pygame.draw.circle(surface, self.color, (self.x - offset_x, self.y - offset_y), self.radius)

        return surface

if __name__ == "__main__":
    print("This is a utility file, not meant to be run directly")