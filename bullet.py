from pygameUtils import *
import constants

class Bullet():
    def __init__(self, x, y, rotation, radius, color=(255, 255, 0), texture=None, velocity=300):
        super().__init__()
        self.rect = pygame.Rect(x, y, radius * 2, radius * 2)
        self.x = self.rect.centerx
        self.y = self.rect.centery
        self.radius = radius
        self.color = color
        self.texture = texture
        self.speed = velocity
        self.rotation = rotation
        self.alive = True

    def update_pos(self, rectangle_dictionary, delta_time):
        self.x, self.y = move_at_angle(np.array([self.x, self.y]), self.rotation, self.speed * delta_time)
        self.rect.center = (self.x, self.y)
        # Use 1 to invert the values because rect cannot be hashed but object can
        hit_rect = self.rect.collidedict(rectangle_dictionary, 1)
        if hit_rect:
                # hit_rect[1] is the rect, hit_rect[0] is the object
                self.alive = False
                hit_object = hit_rect[0]
                hit_method = getattr(hit_object, "hit", None)
                if hit_method and callable(hit_method):
                    hit_method(self.velocity)

if __name__ == "__main__":
    print("This is a utility file, not meant to be run directly")