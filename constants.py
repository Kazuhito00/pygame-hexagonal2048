import pygame

# Screen dimensions
WIDTH, HEIGHT = 450, 450
# Grid dimensions
HEX_RADIUS = 40
GRID_ROWS = 5
GRID_COLS = 5

GRID_ROWS_SMALL = 3
GRID_COLS_SMALL = 3

# Colors
BACKGROUND_COLOR = (187, 173, 160)
GRID_COLOR = (205, 193, 180)
FONT_COLOR = (119, 110, 101)

TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

# Fonts
pygame.font.init()
FONT = pygame.font.Font(None, 55)
SCORE_FONT = pygame.font.Font(None, 36)

# Directions for hexagonal grid
DIRECTIONS = {
    "up": (0, -1, 1),
    "down": (0, 1, -1),
    "up_left": (-1, 0, 1),
    "up_right": (1, -1, 0),
    "down_left": (-1, 1, 0),
    "down_right": (1, 0, -1),
}
