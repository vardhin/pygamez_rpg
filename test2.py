import pygame
import sys
from settings import *
from maps import *
from player import Player

# Initialize Pygame
pygame.init()

# Create the main display surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tileset Test')

# Load tileset image
tileset_image = pygame.image.load('assets/TilesetGrass.png').convert_alpha()

# Calculate number of tiles horizontally and vertically
num_tiles_x = tileset_image.get_width() // TILE_SIZE
num_tiles_y = tileset_image.get_height() // TILE_SIZE

# Create a sprite group for tiles
tile_group = pygame.sprite.Group()

# Define Tile class
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

# Create tiles and add them to the sprite group
for y in range(num_tiles_y):
    for x in range(num_tiles_x):
        tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        tile_image = tileset_image.subsurface(tile_rect)
        tile = Tile(tile_image, x * TILE_SIZE, y * TILE_SIZE)
        tile_group.add(tile)

# Create the player
player = Player(sprite_sheet_path='assets/player.png', pos=[WIDTH // 2, HEIGHT // 2], size=[64, 64])

# Camera variables
camera_x, camera_y = player.rect.x - WIDTH // 2, player.rect.y - HEIGHT // 2
zoom = 1.0

# Function to draw a single tile
def draw_tile(tile, map_pos_x, map_pos_y, camera_x, camera_y, zoom):
    tile_pos_x = (map_pos_x - camera_x) * zoom
    tile_pos_y = (map_pos_y - camera_y) * zoom
    scaled_tile = pygame.transform.scale(tile.image, (int(TILE_SIZE * zoom) + 1, int(TILE_SIZE * zoom) + 1))
    screen.blit(scaled_tile, (int(tile_pos_x), int(tile_pos_y)))

def draw_map(x):
    map = Matrix(x)
    Tmap = map.transpose()
    # Calculate the visible area
    start_col = max(int(camera_x // TILE_SIZE) - 1, 0)
    end_col = min(int((camera_x + WIDTH / zoom) // TILE_SIZE) + 2, len(Tmap))
    start_row = max(int(camera_y // TILE_SIZE) - 1, 0)
    end_row = min(int((camera_y + HEIGHT / zoom) // TILE_SIZE) + 2, len(Tmap[0]))

    for i in range(start_col, end_col):
        for j in range(start_row, end_row):
            element = int(Tmap[i][j])
            draw_tile(list(tile_group)[element], i * TILE_SIZE, j * TILE_SIZE, camera_x, camera_y, zoom)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player.handle_movement(keys)

    # Camera Zoom logic
    if keys[pygame.K_EQUALS] or keys[pygame.K_PLUS]:  # Zoom in
        zoom = min(zoom + ZOOM_STEP, MAX_ZOOM)
    if keys[pygame.K_MINUS]:  # Zoom out
        zoom = max(zoom - ZOOM_STEP, MIN_ZOOM)

    # Camera buffer logic
    if player.rect.x < camera_x + CAMERA_BUFFER:
        camera_x = player.rect.x - CAMERA_BUFFER
    elif player.rect.x + player.rect.width > camera_x + WIDTH / zoom - CAMERA_BUFFER:
        camera_x = player.rect.x + player.rect.width - WIDTH / zoom + CAMERA_BUFFER
    if player.rect.y < camera_y + CAMERA_BUFFER:
        camera_y = player.rect.y - CAMERA_BUFFER
    elif player.rect.y + player.rect.height > camera_y + HEIGHT / zoom - CAMERA_BUFFER:
        camera_y = player.rect.y + player.rect.height - HEIGHT / zoom + CAMERA_BUFFER

    screen.fill(BLACK)
    draw_map(MAP)
    player.draw(screen, camera_x, camera_y, zoom)

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
