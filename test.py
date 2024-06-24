import pygame
import sys
from settings import *
from maps import *

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

# Create the rect
rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, RECT_SIZE, RECT_SIZE)

# Camera variables
camera_x, camera_y = rect.x - WIDTH // 2, rect.y - HEIGHT // 2
zoom = 1.0

# Function to draw a single tile
def draw_tile(tile, map_pos_x, map_pos_y, camera_x, camera_y, zoom):
    tile_pos_x = map_pos_x - camera_x
    tile_pos_y = map_pos_y - camera_y
    scaled_tile = pygame.transform.scale(tile.image, (int(TILE_SIZE * zoom), int(TILE_SIZE * zoom)))
    screen.blit(scaled_tile, (int(tile_pos_x * zoom), int(tile_pos_y * zoom)))

def draw_map(x):
    map = Matrix(x)
    Tmap = map.transpose()
    for i in range(len(Tmap)):
        for j in range(len(Tmap[i])):
            element = int(Tmap[i][j])
            draw_tile(list(tile_group)[element], i*32, j*32, camera_x, camera_y, zoom)

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rect.x -= RECT_SPEED
    if keys[pygame.K_RIGHT]:
        rect.x += RECT_SPEED
    if keys[pygame.K_UP]:
        rect.y -= RECT_SPEED
    if keys[pygame.K_DOWN]:
        rect.y += RECT_SPEED

    # Camera Zoom logic
    if keys[pygame.K_EQUALS] or keys[pygame.K_PLUS]:  # Zoom in
        zoom = min(zoom + ZOOM_STEP, MAX_ZOOM)
    if keys[pygame.K_MINUS]:  # Zoom out
        zoom = max(zoom - ZOOM_STEP, MIN_ZOOM)

    # Camera buffer logic
    if rect.x < camera_x + CAMERA_BUFFER:
        camera_x = rect.x - CAMERA_BUFFER
    elif rect.x + RECT_SIZE > camera_x + WIDTH / zoom - CAMERA_BUFFER:
        camera_x = rect.x + RECT_SIZE - WIDTH / zoom + CAMERA_BUFFER
    if rect.y < camera_y + CAMERA_BUFFER:
        camera_y = rect.y - CAMERA_BUFFER
    elif rect.y + RECT_SIZE > camera_y + HEIGHT / zoom - CAMERA_BUFFER:
        camera_y = rect.y + RECT_SIZE - HEIGHT / zoom + CAMERA_BUFFER

    screen.fill(BLACK)
    draw_map(MAP)
    pygame.draw.rect(screen, RED, (int((rect.x - camera_x) * zoom), int((rect.y - camera_y) * zoom), int(RECT_SIZE * zoom), int(RECT_SIZE * zoom)))

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()