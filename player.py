import keybinds
from pygameUtils import *
import constants

class Player():
    def __init__(self, x, y, size_x, size_y, color=(255, 50, 50), texture=None, speed=200):
        super().__init__()
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

    def handle_held(self, keys, delta_time):
        changed = False
        if "shift" in keys:
            self.walk_to_mouse = True
        else:
            self.walk_to_mouse = False
        if "up" in keys:
            # Multiply by dt to make 10 px / s
            if self.walk_to_mouse:
                self.x, self.y = move_at_angle(np.array([self.x, self.y]), self.rotation, self.speed * delta_time)
            else:
                self.y -= self.speed * delta_time
            changed = True
        if "down" in keys:
            if self.walk_to_mouse:
                self.x, self.y = move_at_angle(np.array([self.x, self.y]), self.rotation + 180, self.speed * delta_time)
            else:
                self.y += self.speed * delta_time
            changed = True
        if "left" in keys:
            # self.x -= self.speed * delta_time
            if self.walk_to_mouse:
                self.x, self.y = move_at_angle(np.array([self.x, self.y]), self.rotation - 90, self.speed * delta_time)
            else:
                self.x -= self.speed * delta_time
            changed = True
        if "right" in keys:
            if self.walk_to_mouse:
                self.x, self.y = move_at_angle(np.array([self.x, self.y]), self.rotation + 90, self.speed * delta_time)
            else:
                self.x += self.speed * delta_time
            changed = True
        return changed

    def handle_mouse(self, mouse_pos, mouse_rel, delta_time):
        pass
        # self.target_rotation = vector_to_angle(np.array(mouse_pos) - np.array([self.x, self.y]))
        # self.rotation = move_towards_angle(self.rotation, self.target_rotation, self.max_rotation_speed * delta_time)
        # # self.rotation = lerp_angle(self.rotation, self.target_rotation, delta_time*2)

    def process(self, mouse_pos, mouse_rel, delta_time):
        self.target_rotation = vector_to_angle(np.array(mouse_pos) - np.array([self.x, self.y]))
        self.rotation = move_towards_angle(self.rotation, self.target_rotation, self.max_rotation_speed * delta_time)
        # self.rotation = lerp_angle(self.rotation, self.target_rotation, delta_time*2)

        view_left = self.rotation - 30
        view_right = self.rotation + 30

        view_left_direction = angle_to_vector(view_left)
        view_right_direction = angle_to_vector(view_right)

        # Create temporary overlay to allow transparency
        surface = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)

        pygame.draw.polygon(surface, (255, 255, 255, 50), create_view_cone_polygon(self))

        pygame.draw.rect(surface, self.color, (self.x - self.size_x//2, self.y - self.size_y//2, self.size_x, self.size_y))

        return surface

if __name__ == "__main__":
    print("This is a utility file, not meant to be run directly")