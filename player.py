import pygame

class Player:
    def __init__(self, sprite_sheet_path, pos, size, frame_rate=5):
        # Load the sprite sheet
        self.sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        
        # Sprite sheet dimensions
        self.sprite_width = self.sprite_sheet.get_width() // 10  # 10 columns
        self.sprite_height = self.sprite_sheet.get_height() // 8  # 8 rows

        # Desired size of the player
        self.size = size
        
        # Extract frames from the sprite sheet
        self.frames = self.extract_frames(self.sprite_sheet, self.sprite_width, self.sprite_height)
        
        # Initial player settings
        self.pos = pos
        self.direction = 'down'
        self.frame = 0
        self.frame_rate = frame_rate  # Control animation speed
        self.is_moving = False
        
        # Map directions to sprite sheet rows
        self.idle_direction_map = {'down': 0, 'left': 1, 'up': 2, 'right': 3}
        self.move_direction_map = {'up': 6, 'down': 4, 'left': 5, 'right': 7}

        # Create the player's rect
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
    
    def extract_frames(self, sheet, width, height):
        frames = []
        for y in range(8):  # 8 rows
            row_frames = []
            for x in range(10):  # 10 columns
                frame = sheet.subsurface(pygame.Rect(x * width, y * height, width, height))
                row_frames.append(frame)
            frames.append(row_frames)
        return frames
    
    def handle_movement(self, keys):
        speed = 5
        self.is_moving = False
        if keys[pygame.K_UP]:
            self.pos[1] -= speed
            self.direction = 'up'
            self.is_moving = True
        elif keys[pygame.K_DOWN]:
            self.pos[1] += speed
            self.direction = 'down'
            self.is_moving = True
        elif keys[pygame.K_LEFT]:
            self.pos[0] -= speed
            self.direction = 'left'
            self.is_moving = True
        elif keys[pygame.K_RIGHT]:
            self.pos[0] += speed
            self.direction = 'right'
            self.is_moving = True
        
        if self.is_moving:
            self.frame += 1
            if self.frame >= 10 * self.frame_rate:  # 10 frames per direction
                self.frame = 0
        else:
            self.frame = 0  # Reset to first frame if no key is pressed
        
        # Update the player's rect position
        self.rect.topleft = self.pos
    
    def draw(self, screen, camera_x, camera_y, zoom):
        if self.is_moving:
            current_frame = self.frame // self.frame_rate
            direction_index = self.move_direction_map[self.direction]
            player_image = self.frames[direction_index][current_frame % 10]  # 10 frames per direction
        else:
            direction_index = self.idle_direction_map[self.direction]
            player_image = self.frames[direction_index][0]  # Use the first frame for idle
        
        scaled_image = pygame.transform.scale(player_image, (int(self.size[0] * zoom), int(self.size[1] * zoom)))
        screen.blit(scaled_image, (int((self.rect.x - camera_x) * zoom), int((self.rect.y - camera_y) * zoom)))
