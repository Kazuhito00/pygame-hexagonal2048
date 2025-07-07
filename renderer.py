import pygame
import math
from constants import (
    WIDTH, HEIGHT, HEX_RADIUS, GRID_COLOR, BACKGROUND_COLOR, 
    TILE_COLORS, FONT, FONT_COLOR, SCORE_FONT
)

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.background_surface = None
        self.static_tiles_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    def create_background(self, board):
        """Draws the static background and grid onto a surface for caching."""
        self.background_surface = pygame.Surface((WIDTH, HEIGHT))
        self.background_surface.fill(BACKGROUND_COLOR)
        for q, r, s in board.get_all_cells():
            self.draw_hexagon(self.background_surface, self.axial_to_pixel(q, r), GRID_COLOR, border_color=(0,0,0))

    def update_static_tiles(self, board):
        """Draws all current tiles onto a separate surface for caching."""
        self.static_tiles_surface.fill((0, 0, 0, 0)) # Clear the surface
        for cell, value in board.grid.items():
            if value > 0:
                pixel_pos = self.axial_to_pixel(*cell[:2])
                self.draw_tile(self.static_tiles_surface, pixel_pos, value)

    def draw(self, board, score, animation):
        """Main draw call. Blits cached surfaces and draws animations on top."""
        if self.background_surface is None:
            self.create_background(board)
            self.update_static_tiles(board)
        
        # Blit the pre-rendered layers
        self.screen.blit(self.background_surface, (0, 0))
        self.screen.blit(self.static_tiles_surface, (0, 0))

        # Draw animations on top of the static layers
        if animation.is_animating:
            self.draw_animations(animation)

        self.draw_score(self.screen, score)
        pygame.display.flip()

    def draw_animations(self, animation):
        for anim in animation.animations:
            progress = anim["frame"] / anim["duration"]
            
            if anim["type"] == "move":
                from_pixel = self.axial_to_pixel(*anim["from_pos"][:2])
                to_pixel = self.axial_to_pixel(*anim["to_pos"][:2])
                curr_x = from_pixel[0] + (to_pixel[0] - from_pixel[0]) * progress
                curr_y = from_pixel[1] + (to_pixel[1] - from_pixel[1]) * progress
                self.draw_tile(self.screen, (curr_x, curr_y), anim["value"])

            elif anim["type"] == "appear":
                pixel_pos = self.axial_to_pixel(*anim["pos"][:2])
                if anim.get("is_merge"):
                    base_scale = 1.0
                    pop_scale = 1.2
                    current_scale = base_scale + (pop_scale - base_scale) * math.sin(progress * math.pi)
                    self.draw_tile(self.screen, pixel_pos, anim["value"], scale=current_scale)
                else:
                    self.draw_tile(self.screen, pixel_pos, anim["value"], scale=progress)

    def draw_tile(self, surface, position, value, scale=1.0):
        color = TILE_COLORS.get(value, (0, 0, 0))
        radius = HEX_RADIUS * scale
        self.draw_hexagon(surface, position, color, radius=radius, border_color=(0,0,0))

        if scale > 0.8:
            try:
                scaled_font_size = int(55 * scale)
                if scaled_font_size > 1:
                    scaled_font = pygame.font.Font(None, scaled_font_size)
                    text_surface = scaled_font.render(str(value), True, FONT_COLOR)
                    text_rect = text_surface.get_rect(center=position)
                    surface.blit(text_surface, text_rect)
            except pygame.error:
                pass

    def draw_score(self, surface, score):
        score_text = f"Score: {score}"
        text_surface = SCORE_FONT.render(score_text, True, FONT_COLOR)
        text_rect = text_surface.get_rect(center=(WIDTH // 2, 40))
        surface.blit(text_surface, text_rect)

    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 128))
        self.screen.blit(overlay, (0, 0))
        text_surface = FONT.render("Game Over!", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def axial_to_pixel(self, q, r):
        x = HEX_RADIUS * (math.sqrt(3) * q + math.sqrt(3)/2 * r)
        y = HEX_RADIUS * (3/2 * r)
        return x + WIDTH // 2, y + HEIGHT // 2

    def draw_hexagon(self, surface, position, color, radius=HEX_RADIUS, border_color=None):
        points = []
        for i in range(6):
            angle_deg = 60 * i + 30
            angle_rad = math.pi / 180 * angle_deg
            points.append(
                (position[0] + radius * math.cos(angle_rad),
                 position[1] + radius * math.sin(angle_rad)))
        pygame.draw.polygon(surface, color, points)
        if border_color:
            pygame.draw.polygon(surface, border_color, points, 2)