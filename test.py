import pygame
import sys
from settings import *
from maps import *
from player import Player
from npc import NPC
from objects import Object

# Initialize Pygame
pygame.init()

# Create the main display surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption('Tileset Test')

# Load tileset image
tileset_image = pygame.image.load('assets/tiles2.png').convert_alpha()

# Create a sprite group for tiles
tile_group = pygame.sprite.Group()

# Create tiles and add them to the sprite group
num_tiles_x = tileset_image.get_width() // TILE_SIZE
num_tiles_y = tileset_image.get_height() // TILE_SIZE

for y in range(num_tiles_y):
    for x in range(num_tiles_x):
        tile_rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        tile_image = tileset_image.subsurface(tile_rect)
        tile = Tile(tile_image, x * TILE_SIZE, y * TILE_SIZE)
        tile_group.add(tile)

# Create the player
player = Player(sprite_sheet_path='assets/player.png', tile_pos=[20, 20], size=[32, 32])

# Create the NPC
#npc = NPC(sprite_sheet_path='assets/player.png', tile_pos=[30, 30], size=[32, 32])

# Create the tree or other objects
tree = Object(
    sprite_sheet_path='assets/Plant.png',  # Path to the sprite sheet
    sprite_pos=[30, 0],  # Position of the specific tree in the sprite sheet (x, y)
    sprite_size=[120, 150],  # Size of the specific tree in the sprite sheet (width, height)
    tile_pos=[170, 55],  # Position of the tree on the map (x, y)
    size=[256, 256] # Size of the tree when rendered (width, height)
)

mapi = read_csv_to_2d_array("maps/hihihi.csv", 50, 50)

# Camera variables
camera_x, camera_y = player.rect.x - WIDTH // 2, player.rect.y - HEIGHT // 2
zoom = 1.0

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    camera_x, camera_y = player.handle_movement(keys, [tree], camera_x, camera_y, zoom)

    # NPC movement logic
    #npc.move_towards_player(player, [tree])

    # Camera Zoom logic
    if keys[pygame.K_EQUALS] or keys[pygame.K_PLUS]:  # Zoom in
        zoom = min(zoom + ZOOM_STEP, MAX_ZOOM)
    if keys[pygame.K_MINUS]:  # Zoom out
        zoom = max(zoom - ZOOM_STEP, MIN_ZOOM)

    screen.fill(BLACK)
    draw_map(mapi, tileset_image, tile_group, camera_x, camera_y, zoom, screen)

    # Sort by y-position (bottom of collision rect)
    objects = [tree, player]
    objects.sort(key=lambda obj: obj.collision_rect.bottom)
    for obj in objects:
        if obj == player:
            player_mask, player_mask_rect = obj.draw(screen, camera_x, camera_y, zoom)
        #elif obj == npc:
        #    npc_mask, npc_mask_rect = obj.draw(screen, camera_x, camera_y, zoom)
        else:
            obj.draw(screen, camera_x, camera_y, zoom, isDebug=False)

    bullet = pygame.Surface((10, 10))
    bullet.fill(RED)
    bullet_rect = bullet.get_rect(topleft=pygame.mouse.get_pos())
    screen.blit(bullet, bullet_rect.topleft)

    bullet_mask = pygame.mask.from_surface(bullet)
    offset = (bullet_rect.left - player_mask_rect.left, bullet_rect.top - player_mask_rect.top)
    if player_mask.overlap(bullet_mask, offset):
        print("collided with player")
    '''
    offset = (bullet_rect.left - npc_mask_rect.left, bullet_rect.top - npc_mask_rect.top)
    if npc_mask.overlap(bullet_mask, offset):
        print("collided with npc")
    '''
    # Update display
    pygame.display.flip()
    fps = clock.tick(60)
    pygame.display.set_caption(f"{fps}")

pygame.quit()
sys.exit()
