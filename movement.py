import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Top Down Player Movement")

# Set up the clock for a decent frame rate
clock = pygame.time.Clock()

# Load the sprite sheet
sprite_sheet = pygame.image.load('assets/player.png').convert_alpha()

# Sprite sheet dimensions
sprite_width = sprite_sheet.get_width() // 10  # 10 columns
sprite_height = sprite_sheet.get_height() // 8  # 8 rows 

def extract_frames(sheet, width, height):
    frames = []
    for y in range(8):  # 8 rows
        row_frames = []
        for x in range(10):  # 10 columns
            frame = sheet.subsurface(pygame.Rect(x * width, y * height, width, height))
            row_frames.append(frame)
        frames.append(row_frames)
    return frames

player_sprites = extract_frames(sprite_sheet, sprite_width, sprite_height)

# Initial player settings
player_pos = [screen_width // 2, screen_height // 2]
player_direction = 'down'
player_frame = 0
frame_rate = 5  # Control animation speed

# Map directions to sprite sheet rows
direction_map = {'up': 6, 'down': 4, 'left': 5, 'right': 7}

def handle_movement(keys, player_pos, player_direction, player_frame):
    speed = 5
    if keys[pygame.K_UP]:
        player_pos[1] -= speed
        player_direction = 'up'
    elif keys[pygame.K_DOWN]:
        player_pos[1] += speed
        player_direction = 'down'
    elif keys[pygame.K_LEFT]:
        player_pos[0] -= speed
        player_direction = 'left'
    elif keys[pygame.K_RIGHT]:
        player_pos[0] += speed
        player_direction = 'right'
    else:
        player_frame = 0  # Reset to first frame if no key is pressed
    
    player_frame += 1
    if player_frame >= 10 * frame_rate:  # 10 frames per direction
        player_frame = 0

    return player_pos, player_direction, player_frame

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    player_pos, player_direction, player_frame = handle_movement(keys, player_pos, player_direction, player_frame)
    
    screen.fill((0, 0, 0))  # Clear the screen with a black color
    
    # Draw the player sprite
    current_frame = player_frame // frame_rate
    direction_index = direction_map[player_direction]
    player_image = player_sprites[direction_index][current_frame % 10]  # 10 frames per direction
    screen.blit(player_image, player_pos)
    
    pygame.display.flip()  # Update the display
    clock.tick(60)  # Maintain a decent frame rate

pygame.quit()
sys.exit()
