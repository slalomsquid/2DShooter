import pygame
import numpy as np

pygame.init()

font = pygame.font.SysFont("Arial", 40)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
CREAM = (238, 222, 197)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
GREEN = (0, 255, 0)
NONE = (0, 0, 0)

def render_text(text, pos, color, canv, size=1, center=False, transparent=False):
    font_obj = pygame.font.SysFont(None, size) 
    if transparent:
        text_surface = pygame.surface(pygame.SRCALPHA)
        text_surface = text_surface.convert_alpha()
    else:
        text_surface = font_obj.render(str(text), False, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (pos[0], pos[1])
    canv.blit(text_surface, text_rect)

def render_player_arrow(pos, ang, color, canv):
    triangle_points = [move_at_angle(pos, ang, 20), move_at_angle(pos, ang+120, 20), pos, move_at_angle(pos, ang+240, 20)]
    # p1 = move_at_angle(pos, dir + 90, 20)
    # p2 = move_at_angle(pos, dir + 210, 20)
    # p3 = move_at_angle(pos, dir + 330, 20)
    
    # triangle_points = [p1.flatten(), p2.flatten(), p3.flatten()]
    pygame.draw.polygon(canv, color, triangle_points)

def render_map(map, cell_x, cell_y, canv):
    for cell in range(len(map)):
        for tile in range(len(map[cell])):
            if map[cell][tile] == 1:
                pygame.draw.rect(canv, CYAN, (tile*cell_x, cell*cell_y, cell_x, cell_y))

def draw_alpha_line(color, alpha, start, end, width, canv):
    # Calculate height of the wall slice
    height = end[1] - start[1]
    if height <= 0: return

    # Create a tiny surface just for this one ray slice
    # Note: We use a fixed width or ray_width
    line_surf = pygame.Surface((width, int(height)), pygame.SRCALPHA)
    
    # Fill it with the color and the calculated alpha
    line_surf.fill((*color, alpha))
    
    # Blit it to the main canvas at the start position
    canv.blit(line_surf, start)

# VECTOR MATH #

def angle_to_vector(angle):
    """Returns a vector with a length of 1 for a given angle, <angle -> left, >angl -> right"""
    return np.round(np.array([np.cos(np.radians(angle+90)),np.sin(np.radians(angle+90))]), 4)

def translate_vect(vect, displacement):
    return vect + displacement

def move_in_direction(vect, dir, velocity):
    displacement = dir * velocity
    return vect + displacement

def move_at_angle(vect, angle, velocity):
    dir = angle_to_vector(angle)
    displacement = dir * velocity
    # return np.array(vect + displacement, dtype=object)
    return vect + displacement

def get_vector_magnitude(vector):
    return np.linalg.norm(vector)

def get_distance_between(vect1, vect2):
    return np.linalg.norm(vect1 - vect2)

def simplify_vector(vector):
    if np.linalg.norm(vector) != 0:
        return vector / np.linalg.norm(vector)
    # return np.array([0,0])
    return vector

def vector_to_angle(dir):
    return np.degrees(np.arctan2(dir[1], dir[0]))-90

def cast_ray(start_pos, angle, game_map, size_x, size_y, max_distance=100):
    # Get the normalized direction vector
    direction = angle_to_vector(angle)
    
    # How far we move each step (smaller = more accurate)
    step_size = 1
    ray_pos = np.array(start_pos, dtype=float)
    distance_traveled = 0

    while True:
        # Move the ray forward
        ray_pos += direction * step_size
        distance_traveled += step_size

        # Convert world position to grid coordinates
        map_x = int(ray_pos[0] // size_x)
        map_y = int(ray_pos[1] // size_y)
        
        # Check if we are out of bounds
        if distance_traveled > max_distance or map_y < 0 or map_y >= len(game_map) or map_x < 0 or map_x >= len(game_map[0]):
            break
            
        # Check if we hit a wall (1)
        if game_map[map_y][map_x] != 0:
            return (ray_pos, distance_traveled, game_map[map_y][map_x]) # Return the coordinate where we hit

def decimal_range(start, stop, increment):
    while start < stop: # and not math.isclose(start, stop): Py>3.5
        yield start
        start += increment

def lerp(start, end, t):
    return start + t * (end - start)

def move_towards(current, target, max_distance_delta):
    to_vector = target - current
    dist = np.linalg.norm(to_vector)
    if dist <= max_distance_delta or dist == 0:
        return target
    return current + to_vector / dist * max_distance_delta