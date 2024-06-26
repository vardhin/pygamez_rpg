import pygame
from settings import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, pos, size, frame_rate=5):
        super().__init__()
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.sprite_width = self.sprite_sheet.get_width() // 10
        self.sprite_height = self.sprite_sheet.get_height() // 8
        self.size = size
        self.frames = self.extract_frames(self.sprite_sheet, self.sprite_width, self.sprite_height)
        self.pos = pos
        self.direction = 'down'
        self.frame = 0
        self.frame_rate = frame_rate
        self.is_moving = False

        self.idle_direction_map = {'down': 0, 'left': 1, 'up': 2, 'right': 3}
        self.move_direction_map = {'up': 6, 'down': 4, 'left': 5, 'right': 7}

        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.collision_rect = pygame.Rect(pos[0], pos[1] + size[1] - 10, size[0] - 15, 10)
        self.true_collide_rect = pygame.Rect(pos[0] + 10, pos[1] + size[1] - 20, size[0] - 20, 20)

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
        speed = 2  # NPC movement speed, can be adjusted
        self.is_moving = False
        new_pos = self.pos[:]

        if direction == 'up':
            new_pos[1] -= speed
            self.direction = 'up'
            self.is_moving = True
        elif direction == 'down':
            new_pos[1] += speed
            self.direction = 'down'
            self.is_moving = True
        elif direction == 'left':
            new_pos[0] -= speed
            self.direction = 'left'
            self.is_moving = True
        elif direction == 'right':
            new_pos[0] += speed
            self.direction = 'right'
            self.is_moving = True

        new_true_collide_rect = pygame.Rect(new_pos[0] + 10, new_pos[1] + self.size[1] - 20, self.size[0] - 20, 20)

        if not any(new_true_collide_rect.colliderect(obstacle.true_collide_rect) for obstacle in obstacles):
            self.pos = new_pos

        self.frame = (self.frame + 1) % (10 * self.frame_rate) if self.is_moving else 0
        self.update_rects()
        self.update_image()

    def update_rects(self):
        self.rect.topleft = self.pos
        self.collision_rect.topleft = (self.pos[0], self.pos[1] + self.size[1] - 10)
        self.true_collide_rect.topleft = (self.pos[0] + 10, self.pos[1] + self.size[1] - 20)

    def update_image(self):
        direction_map = self.move_direction_map if self.is_moving else self.idle_direction_map
        frame_idx = self.frame // self.frame_rate if self.is_moving else 0
        direction_index = direction_map[self.direction]
        self.image = self.frames[direction_index][frame_idx % 10]

    def draw(self, screen, camera_x, camera_y, zoom):
        scaled_image = pygame.transform.scale(self.image, (int(self.size[0] * zoom), int(self.size[1] * zoom)))
        screen.blit(scaled_image, (int((self.rect.x - camera_x) * zoom), int((self.rect.y - camera_y) * zoom)))

        # Scale and adjust the mask coordinates
        scaled_mask = pygame.mask.from_surface(scaled_image)
        mask_rect = scaled_mask.get_rect()
        mask_rect.topleft = (int((self.rect.x - camera_x) * zoom), int((self.rect.y - camera_y) * zoom))
        
        return scaled_mask, mask_rect
