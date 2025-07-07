import asyncio
import pygame
from board import Board
from renderer import Renderer
from animation import Animation
from constants import (
    WIDTH,
    HEIGHT,
    DIRECTIONS,
    GRID_ROWS,
    GRID_COLS,
    GRID_ROWS_SMALL,
    GRID_COLS_SMALL,
)


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.current_rows = GRID_ROWS_SMALL
        self.current_cols = GRID_COLS_SMALL
        self.board = Board(self.current_rows, self.current_cols)
        self.renderer = Renderer(screen)
        self.animation = Animation()
        self.running = True
        self.game_over = False
        self.needs_render = True  # Flag to control rendering
        self.renderer.create_background(self.board)  # Initial background creation
        self.renderer.update_static_tiles(self.board)  # Initial static tiles update

    async def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()

            # Only draw if there are active animations or a render has been explicitly requested
            if self.animation.is_animating or self.needs_render:
                self.draw()
                self.needs_render = False  # Reset the flag after rendering

            clock.tick(60)  # Limit frame rate
            await asyncio.sleep(0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # Toggle map size
                    self.toggle_map_size()
                    self.needs_render = True
                    return  # Skip other key handling for this frame

                if not self.game_over and not self.animation.is_animating:
                    moved = False
                    animations = []
                    if event.key == pygame.K_w:
                        moved, animations = self.board.move("up")
                    elif event.key == pygame.K_e:
                        moved, animations = self.board.move("up_right")
                    elif event.key == pygame.K_a:
                        moved, animations = self.board.move("up_left")
                    elif event.key == pygame.K_x:
                        moved, animations = self.board.move("down")
                    elif event.key == pygame.K_d:
                        moved, animations = self.board.move("down_right")
                    elif event.key == pygame.K_z:
                        moved, animations = self.board.move("down_left")

                    if moved:
                        self.start_animations(animations)
                        if not self.board.can_move():
                            self.game_over = True
                        self.needs_render = True

    def toggle_map_size(self):
        if self.current_rows == GRID_ROWS:
            self.current_rows = GRID_ROWS_SMALL
            self.current_cols = GRID_COLS_SMALL
        else:
            self.current_rows = GRID_ROWS
            self.current_cols = GRID_COLS

        # Reinitialize board and renderer for new map size
        self.board = Board(self.current_rows, self.current_cols)
        self.renderer = Renderer(
            self.screen
        )  # Recreate renderer to clear cached background
        self.animation = Animation()  # Reset animations
        self.game_over = False  # Reset game over state
        self.renderer.create_background(
            self.board
        )  # Create new background for new board
        self.renderer.update_static_tiles(
            self.board
        )  # Update static tiles for new board

    def start_animations(self, animation_data):
        for anim_info in animation_data:
            if anim_info["type"] == "move":
                self.animation.add_move(
                    anim_info["value"],
                    anim_info["from"],
                    anim_info["to"],
                    is_merge=anim_info.get("is_merge", False),
                )
            elif anim_info["type"] == "appear":
                self.animation.add_appear(
                    anim_info["value"],
                    anim_info["at"],
                    is_merge=anim_info.get("is_merge", False),
                )

    def update(self):
        was_animating = self.animation.is_animating
        self.animation.update()
        # If animation just finished, update the static tile surface and request one final render
        if was_animating and not self.animation.is_animating:
            self.renderer.update_static_tiles(self.board)
            self.needs_render = True

    def draw(self):
        self.renderer.draw(self.board, self.board.score, self.animation)
        if self.game_over:
            self.renderer.draw_game_over()
