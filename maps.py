import numpy as np
import pygame
from settings import *
import csv

def read_csv_to_2d_array(file_path, rows=None, columns=None):
    result = []

    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        
        if rows is not None:
            for i, row in enumerate(csv_reader):
                if i >= rows:
                    break
                if columns is not None:
                    result.append(row[:columns])
                else:
                    result.append(row)
        else:
            for row in csv_reader:
                if columns is not None:
                    result.append(row[:columns])
                else:
                    result.append(row)

    return result

def save_array_to_csv(data, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for row in data:
            csvwriter.writerow(row)

class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix  # Do not convert to np.array to preserve irregular shapes

    def get_rows(self):
        return self.matrix
    
    def get_columns(self):
        max_cols = max(len(row) for row in self.matrix)
        columns = []
        for col_index in range(max_cols):
            column = []
            for row in self.matrix:
                if col_index < len(row):
                    column.append(row[col_index])
                else:
                    column.append(None)  # Placeholder for missing values
            columns.append(column)
        return columns

    def transpose(self):
        return self.get_columns()

# Tile class
class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

# Draw a single tile
def draw_tile(tile, map_pos_x, map_pos_y, camera_x, camera_y, zoom, screen):
    tile_pos_x = (map_pos_x - camera_x) * zoom
    tile_pos_y = (map_pos_y - camera_y) * zoom
    scaled_tile = pygame.transform.scale(tile.image, (int(TILE_SIZE * zoom) + 1, int(TILE_SIZE * zoom) + 1))
    screen.blit(scaled_tile, (int(tile_pos_x), int(tile_pos_y)))

# Draw the map
def draw_map(matrix, tileset_image, tile_group, camera_x, camera_y, zoom, screen):
    num_tiles_x = tileset_image.get_width() // TILE_SIZE
    num_tiles_y = tileset_image.get_height() // TILE_SIZE

    map_matrix = Matrix(matrix)
    transposed_map = map_matrix.transpose()

    # Calculate visible area based on camera position
    screen_tiles_x = int(WIDTH // (TILE_SIZE * zoom)) + 3  # Add some margin
    screen_tiles_y = int(HEIGHT // (TILE_SIZE * zoom)) + 3  # Add some margin

    start_col = max(int(camera_x // TILE_SIZE) - 1, 0)
    end_col = min(start_col + screen_tiles_x, len(transposed_map))
    start_row = max(int(camera_y // TILE_SIZE) - 1, 0)
    end_row = min(start_row + screen_tiles_y, max(len(row) for row in transposed_map))

    for i in range(start_col, end_col):
        for j in range(start_row, end_row):
            if j < len(transposed_map[i]) and transposed_map[i][j] is not None and transposed_map[i][j] != '':
                try:
                    element = int(transposed_map[i][j])
                    draw_tile(list(tile_group)[element], i * TILE_SIZE, j * TILE_SIZE, camera_x, camera_y, zoom, screen)
                except ValueError:
                    print(f"Skipping invalid tile value at {i},{j}: {transposed_map[i][j]}")
