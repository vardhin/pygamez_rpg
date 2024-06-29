import pygame
import random
import math
from settings import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, tile_pos, size, frame_rate=5):
        super().__init__()
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.sprite_width = self.sprite_sheet.get_width() // 10
        self.sprite_height = self.sprite_sheet.get_height() // 8
        self.size = size
        self.frames = self.extract_frames(self.sprite_sheet, self.sprite_width, self.sprite_height)
        self.tile_pos = tile_pos
        self.pixel_pos = [tile_pos[0] * TILE_SIZE, tile_pos[1] * TILE_SIZE]
        self.direction = 'down'
        self.frame = 0
        self.frame_rate = frame_rate
        self.is_moving = False
        self.speed = 2
        self.idle_direction_map = {'down': 0, 'left': 1, 'up': 2, 'right': 3}
        self.move_direction_map = {'up': 6, 'down': 4, 'left': 5, 'right': 7}

        self.rect = pygame.Rect(self.pixel_pos[0], self.pixel_pos[1], size[0], size[1])
        self.collision_rect = pygame.Rect(self.pixel_pos[0], self.pixel_pos[1] + size[1] - 10, size[0] - 15, 10)
        self.true_collide_rect = pygame.Rect(self.pixel_pos[0] + 10, self.pixel_pos[1] + self.size[1] - 20, self.size[0] - 20, 20)

        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.update_image()

    def extract_frames(self, sheet, width, height):
        frames = []
        for y in range(8):
            row_frames = []
            for x in range(10):
                frame = sheet.subsurface(pygame.Rect(x * width, y * height, width, height))
                row_frames.append(frame)
            frames.append(row_frames)
        return frames

    def move(self, direction, obstacles):
        speed = self.speed  # NPC movement speed, can be adjusted
        diagonal_speed = speed / (2 ** 0.5)
        self.is_moving = False
        new_pixel_pos = self.pixel_pos[:]

        if direction == 'up':
            new_pixel_pos[1] -= speed
            self.direction = 'up'
            self.is_moving = True
        elif direction == 'down':
            new_pixel_pos[1] += speed
            self.direction = 'down'
            self.is_moving = True
        elif direction == 'left':
            new_pixel_pos[0] -= speed
            self.direction = 'left'
            self.is_moving = True
        elif direction == 'right':
            new_pixel_pos[0] += speed
            self.direction = 'right'
            self.is_moving = True
        elif direction == 'up_left':
            new_pixel_pos[0] -= diagonal_speed
            new_pixel_pos[1] -= diagonal_speed
            self.direction = 'left'
            self.is_moving = True
        elif direction == 'up_right':
            new_pixel_pos[0] += diagonal_speed
            new_pixel_pos[1] -= diagonal_speed
            self.direction = 'right'
            self.is_moving = True
        elif direction == 'down_left':
            new_pixel_pos[0] -= diagonal_speed
            new_pixel_pos[1] += diagonal_speed
            self.direction = 'left'
            self.is_moving = True
        elif direction == 'down_right':
            new_pixel_pos[0] += diagonal_speed
            new_pixel_pos[1] += diagonal_speed
            self.direction = 'right'
            self.is_moving = True

        new_true_collide_rect = pygame.Rect(new_pixel_pos[0] + 10, new_pixel_pos[1] + self.size[1] - 20, self.size[0] - 20, 20)

        if not any(new_true_collide_rect.colliderect(obstacle.true_collide_rect) for obstacle in obstacles):
            self.pixel_pos = new_pixel_pos
            self.tile_pos = [self.pixel_pos[0] // TILE_SIZE, self.pixel_pos[1] // TILE_SIZE]

        self.frame = (self.frame + 1) % (10 * self.frame_rate) if self.is_moving else 0
        self.update_rects()
        self.update_image()

    def update_rects(self):
        self.rect.topleft = self.pixel_pos
        self.collision_rect.topleft = (self.pixel_pos[0], self.pixel_pos[1] + self.size[1] - 10)
        self.true_collide_rect.topleft = (self.pixel_pos[0] + 10, self.pixel_pos[1] + self.size[1] - 20)

    def update_image(self):
        direction_map = self.move_direction_map if self.is_moving else self.idle_direction_map
        frame_idx = self.frame // self.frame_rate if self.is_moving else 0
        direction_index = direction_map[self.direction]
        self.image = self.frames[direction_index][frame_idx % 10]

    def cast_ray(self, direction, obstacles, distance=50):
        ray_end_pos = list(self.pixel_pos)
        if direction == 'up':
            ray_end_pos[1] -= distance
        elif direction == 'down':
            ray_end_pos[1] += distance
        elif direction == 'left':
            ray_end_pos[0] -= distance
        elif direction == 'right':
            ray_end_pos[0] += distance

        ray_rect = pygame.Rect(ray_end_pos[0], ray_end_pos[1], self.size[0], self.size[1])
        return any(ray_rect.colliderect(obstacle.true_collide_rect) for obstacle in obstacles)

    def move_towards_player(self, player, obstacles):
        distance_to_player = math.hypot(self.pixel_pos[0] - player.pixel_pos[0], self.pixel_pos[1] - player.pixel_pos[1])

        if distance_to_player > 25:
            # Calculate preferred movement direction towards the player
            dx = self.pixel_pos[0] - player.pixel_pos[0]
            dy = self.pixel_pos[1] - player.pixel_pos[1]

            if abs(dx) > abs(dy):
                if dx > 0 and not self.cast_ray('left', obstacles):
                    self.move('left', obstacles)
                elif dx < 0 and not self.cast_ray('right', obstacles):
                    self.move('right', obstacles)
            elif abs(dx) < abs(dy):
                if dy > 0 and not self.cast_ray('up', obstacles):
                    self.move('up', obstacles)
                elif dy < 0 and not self.cast_ray('down', obstacles):
                    self.move('down', obstacles)
            else:
                if dx > 0 and dy > 0:
                    if not self.cast_ray('up_left', obstacles):
                        self.move('up_left', obstacles)
                elif dx > 0 and dy < 0:
                    if not self.cast_ray('down_left', obstacles):
                        self.move('down_left', obstacles)
                elif dx < 0 and dy > 0:
                    if not self.cast_ray('up_right', obstacles):
                        self.move('up_right', obstacles)
                elif dx < 0 and dy < 0:
                    if not self.cast_ray('down_right', obstacles):
                        self.move('down_right', obstacles)
        else:
            # Stop near the player
            self.is_moving = False
            self.frame = 0
            self.update_image()

        # Random scouting movement
        self.random_scout()

    def random_scout(self):
        if random.random() < 0.005:  # Adjust probability for random movement
            directions = ['up', 'down', 'left', 'right', 'up_left', 'up_right', 'down_left', 'down_right']
            random_direction = random.choice(directions)
            self.move(random_direction, [])

    def draw(self, screen, camera_x, camera_y, zoom):
        scaled_image = pygame.transform.scale(self.image, (int(self.size[0] * zoom), int(self.size[1] * zoom)))
        screen.blit(scaled_image, (int((self.rect.x - camera_x) * zoom), int((self.rect.y - camera_y) * zoom)))

        # Scale and adjust the mask coordinates
        scaled_mask = pygame.mask.from_surface(scaled_image)
        mask_rect = scaled_mask.get_rect()
        mask_rect.topleft = (int((self.rect.x - camera_x) * zoom), int((self.rect.y - camera_y) * zoom))

        return scaled_mask, mask_rect
