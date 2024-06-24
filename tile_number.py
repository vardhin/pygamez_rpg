"""
    The function of this code:
    ~put in a tile set
    ~it will determine the index of each tile
    ~can also give you position of the tile based on index
"""

import pygame
pygame.init()

# Constants for screen dimensions and tile size
WIDTH = 800
HEIGHT = 600
TILE_SIZE = 32

# Define colors (optional)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create the main display surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tileset Test')

# Load tileset image
tileset_image = pygame.image.load('assets/TilesetGrass.png').convert_alpha()

# Calculate number of tiles horizontally and vertically
num_tiles_x = tileset_image.get_width() // TILE_SIZE
num_tiles_y = tileset_image.get_height() // TILE_SIZE

# Create a list to hold tile images
tiles = []
for y in range(num_tiles_y):
    for x in range(num_tiles_x):
        tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        tile_image = tileset_image.subsurface(tile_rect)
        tiles.append(tile_image)

# Function to get tile position based on index
def get_tile_position(index):
    x = (index % num_tiles_x) * TILE_SIZE
    y = (index // num_tiles_x) * TILE_SIZE
    return (x, y)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(BLACK)

    # Draw tiles on the screen
    for index, tile in enumerate(tiles):
        x, y = get_tile_position(index)
        screen.blit(tile, (x, y))

        # Render index number in the center of each tile
        font = pygame.font.Font(None, 20)  # Default font, size 20
        text_surface = font.render(str(index), True, WHITE)
        text_rect = text_surface.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        screen.blit(text_surface, text_rect)
    
    print(get_tile_position(455))
    # Update display
    pygame.display.flip()

pygame.quit()
