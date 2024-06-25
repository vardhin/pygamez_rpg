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

class Object(pygame.sprite.Sprite):
    def __init__(self, sprite_sheet_path, sprite_pos, sprite_size, pos, size):
        super().__init__()
        sprite_sheet = pygame.image.load(sprite_sheet_path).convert_alpha()
        self.image = sprite_sheet.subsurface(pygame.Rect(sprite_pos[0], sprite_pos[1], sprite_size[0], sprite_size[1])).copy()
        self.rect = self.image.get_rect(topleft=pos)
        self.collision_rect = pygame.Rect(pos[0], pos[1] + size[1] + 12, size[0] - 15, 10)
        self.true_collide_rect = pygame.Rect(pos[0] + 45, pos[1] + size[1] + 12, size[0] - 119, 10)

    def draw(self, screen, camera_x, camera_y, zoom):
        scaled_image = pygame.transform.scale(self.image, (int(self.rect.width * zoom), int(self.rect.height * zoom)))
        screen.blit(scaled_image, (int((self.rect.x - camera_x) * zoom), int((self.rect.y - camera_y) * zoom)))
        
        '''
        collision_rect_scaled = self.scale_rect(self.collision_rect, camera_x, camera_y, zoom)
        pygame.draw.rect(screen, (255, 0, 0), collision_rect_scaled, 2)

        true_collide_rect_scaled = self.scale_rect(self.true_collide_rect, camera_x, camera_y, zoom)
        pygame.draw.rect(screen, (0, 0, 255), true_collide_rect_scaled, 2)
        '''

    def scale_rect(self, rect, camera_x, camera_y, zoom):
        return pygame.Rect(
            (rect.x - camera_x) * zoom,
            (rect.y - camera_y) * zoom,
            rect.width * zoom,
            rect.height * zoom
        )


# Create tiles and add them to the sprite group
for y in range(num_tiles_y):
    for x in range(num_tiles_x):
        tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        tile_image = tileset_image.subsurface(tile_rect)
        tile = Tile(tile_image, x * TILE_SIZE, y * TILE_SIZE)
        tile_group.add(tile)

# Create the player
player = Player(sprite_sheet_path='assets/player.png', pos=[WIDTH // 2, HEIGHT // 2], size=[64, 64])

# Create the tree or other objects
tree = Object(
    sprite_sheet_path='assets/Plant.png',  # Path to the sprite sheet
    sprite_pos=[30, 0],  # Position of the specific tree in the sprite sheet (x, y)
    sprite_size=[120, 150],  # Size of the specific tree in the sprite sheet (width, height)
    pos=[40, 40],  # Position of the tree on the map (x, y)
    size=[128, 128]  # Size of the tree when rendered (width, height)
)

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
    player.handle_movement(keys, [tree])

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
    draw_map(MAP3)

    # Sort by y-position (bottom of collision rect)
    objects = [tree, player]
    objects.sort(key=lambda obj: obj.collision_rect.bottom)
    for obj in objects:
        if obj == player:
            player_mask = obj.draw(screen,camera_x,camera_y,zoom)
        obj.draw(screen, camera_x, camera_y, zoom)
    
    bullet = pygame.Surface((10, 10))
    bullet.fill(RED)
    bullet_rect = bullet.get_rect(topleft=pygame.mouse.get_pos())
    screen.blit(player_mask.to_surface(),(player.rect.left,player.rect.top))
    screen.blit(bullet, bullet_rect.topleft)
    
    bullet_mask = pygame.mask.from_surface(bullet)
    offset = (bullet_rect.left - player.rect.left, bullet_rect.top - player.rect.top)
        
    if player_mask.overlap(bullet_mask, offset):
        print("collided")

    # Update display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
