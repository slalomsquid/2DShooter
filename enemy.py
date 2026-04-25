import keybinds
from pygameUtils import *

class Enemy():
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
        self.max_rotation_speed = 180
        self.health = 100
        self.view_distance = 100

    def process(self, mouse_pos, mouse_rel, player_pos, delta_time):
        self.target_rotation = vector_to_angle(np.array(player_pos) - np.array([self.x, self.y]))
        self.rotation = move_towards_angle(self.rotation, self.target_rotation, self.max_rotation_speed * delta_time)
        # self.rotation = lerp_angle(self.rotation, self.target_rotation, delta_time*2)

if __name__ == "__main__":
    print("This is a utility file, not meant to be run directly")