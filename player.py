import keybinds
from pygameUtils import *

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
        self.max_rotation_speed = 0
        self.health = 100
        self.view_distance = 100

    def handle_held(self, keys, delta_time):
        if "up" in keys:
            # Multiply by dt to make 10 px / s
            # player.y -= player.speed * delta_time
            self.x, self.y = move_at_angle(np.array([self.x, self.y]), self.rotation, self.speed * delta_time)
        if "down" in keys:
            # self.y += self.speed * delta_time
            self.x, self.y = move_at_angle(np.array([self.x, self.y]), self.rotation + 180, self.speed * delta_time)
        if "left" in keys:
            # self.x -= self.speed * delta_time
            self.x, self.y = move_at_angle(np.array([self.x, self.y]), self.rotation - 90, self.speed * delta_time)
        if "right" in keys:
            # self.x += self.speed * delta_time
            self.x, self.y = move_at_angle(np.array([self.x, self.y]), self.rotation + 90, self.speed * delta_time)

    def handle_mouse(self, mouse_pos, mouse_rel):
        self.target_rotation = vector_to_angle(np.array(mouse_pos) - np.array([self.x, self.y]))
        self.rotation = self.target_rotation