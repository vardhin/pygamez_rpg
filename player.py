import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, tile_pos, size, frame_rate=4):
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
        self.speed = 3.5
        self.idle_direction_map = {'down': 0, 'left': 1, 'up': 2, 'right': 3}
        self.move_direction_map = {'up': 6, 'down': 4, 'left': 5, 'right': 7}

        self.rect = pygame.Rect(self.pixel_pos[0], self.pixel_pos[1], size[0], size[1])
        self.collision_rect = pygame.Rect(self.pixel_pos[0], self.pixel_pos[1] + size[1] - 10, size[0] - 15, 10)
        self.true_collide_rect = pygame.Rect(self.pixel_pos[0] + 10, self.pixel_pos[1] + size[1] - 20, size[0] - 20, 20)

        self.image = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.update_image()
        self.bullet_image = pygame.Surface((10, 5))  # Example surface for bullet image
        self.bullets = pygame.sprite.Group()

    def extract_frames(self, sheet, width, height):
        frames = []
        for y in range(8):
            row_frames = []
            for x in range(10):
                frame = sheet.subsurface(pygame.Rect(x * width, y * height, width, height))
                row_frames.append(frame)
            frames.append(row_frames)
        return frames

    def handle_movement(self, keys, obstacles, camera_x, camera_y, zoom):
        speed = self.speed
        diagonal_speed = speed / (2 ** 0.5)
        self.is_moving = False
        new_pos = self.pixel_pos[:]

        if keys[pygame.K_w] and keys[pygame.K_a]:
            new_pos[0] -= diagonal_speed
            new_pos[1] -= diagonal_speed
            self.direction = 'left'
            self.is_moving = True
        elif keys[pygame.K_w] and keys[pygame.K_d]:
            new_pos[0] += diagonal_speed
            new_pos[1] -= diagonal_speed
            self.direction = 'right'
            self.is_moving = True
        elif keys[pygame.K_s] and keys[pygame.K_a]:
            new_pos[0] -= diagonal_speed
            new_pos[1] += diagonal_speed
            self.direction = 'left'
            self.is_moving = True
        elif keys[pygame.K_s] and keys[pygame.K_d]:
            new_pos[0] += diagonal_speed
            new_pos[1] += diagonal_speed
            self.direction = 'right'
            self.is_moving = True
        elif keys[pygame.K_w]:
            new_pos[1] -= speed
            self.direction = 'up'
            self.is_moving = True
        elif keys[pygame.K_s]:
            new_pos[1] += speed
            self.direction = 'down'
            self.is_moving = True
        elif keys[pygame.K_a]:
            new_pos[0] -= speed
            self.direction = 'left'
            self.is_moving = True
        elif keys[pygame.K_d]:
            new_pos[0] += speed
            self.direction = 'right'
            self.is_moving = True

        new_true_collide_rect = pygame.Rect(new_pos[0] + 10, new_pos[1] + self.size[1] - 20, self.size[0] - 20, 20)

        if not any(new_true_collide_rect.colliderect(obstacle.true_collide_rect) for obstacle in obstacles):
            self.pixel_pos = new_pos
            self.tile_pos = [self.pixel_pos[0] // TILE_SIZE, self.pixel_pos[1] // TILE_SIZE]

        self.frame = (self.frame + 1) % (10 * self.frame_rate) if self.is_moving else 0
        self.update_rects()
        self.update_image()

        # Smooth camera centering
        target_camera_x = self.rect.centerx - WIDTH / (2 * zoom)
        target_camera_y = self.rect.centery - HEIGHT / (2 * zoom)
        camera_x += (target_camera_x - camera_x) * 0.35  # Adjust 0.1 for smoother transition
        camera_y += (target_camera_y - camera_y) * 0.35  # Adjust 0.1 for smoother transition

        return camera_x, camera_y


    def move(self, direction, obstacles):
        speed = self.speed  # Player movement speed, can be adjusted
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

    def draw(self, screen, camera_x, camera_y, zoom):
        scaled_image = pygame.transform.scale(self.image, (int(self.size[0] * zoom), int(self.size[1] * zoom)))
        screen.blit(scaled_image, (int((self.rect.x - camera_x) * zoom), int((self.rect.y - camera_y) * zoom)))

        # Scale and adjust the mask coordinates
        scaled_mask = pygame.mask.from_surface(scaled_image)
        mask_rect = scaled_mask.get_rect()
        mask_rect.topleft = (int((self.rect.x - camera_x) * zoom), int((self.rect.y - camera_y) * zoom))

        return scaled_mask, mask_rect

