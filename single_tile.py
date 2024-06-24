#assets/Tilesets/Tileset-Terrain2.png

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

# Function to draw a tile on the screen based on its index
def draw_tile(index, tile_pos):
    if 0 <= index < len(tiles):
        tile = tiles[index]
        screen.blit(tile, (x, y))
    else:
        print(f"Invalid tile index: {index}")

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(BLACK)

    # Example usage: draw tile at index 3 at position (100, 100)
    draw_tile(455, 0, 0)
    # Update display
    pygame.display.flip()

pygame.quit()

