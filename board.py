
import random
from collections import defaultdict
from constants import DIRECTIONS, GRID_ROWS, GRID_COLS

class Board:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = defaultdict(int)
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()

    def get_all_cells(self):
        # Helper to define the hexagonal grid shape
        cells = []
        for q in range(-self.cols // 2 + 1, self.cols // 2 + 2):
             for r in range(-self.rows // 2 + 1, self.rows // 2 + 2):
                 s = -q - r
                 if abs(q) <= self.cols // 2 and abs(r) <= self.rows // 2 and abs(s) <= self.cols //2:
                    cells.append((q, r, s))
        return cells


    def get_empty_cells(self):
        all_cells = self.get_all_cells()
        return [cell for cell in all_cells if self.grid[cell] == 0]

    def add_random_tile(self):
        empty_cells = self.get_empty_cells()
        if not empty_cells:
            return None
        cell = random.choice(empty_cells)
        value = 2 if random.random() < 0.9 else 4
        self.grid[cell] = value
        return {"cell": cell, "value": value}

    def move(self, direction_name):
        direction = DIRECTIONS[direction_name]
        moved = False
        merged_this_move = set()
        animations = []

        # Get cells sorted for traversal
        cells = self.get_all_cells()
        
        # Sort cells to process them from the edge of movement
        cells.sort(key=lambda cell: -(cell[0] * direction[0] + cell[1] * direction[1] + cell[2] * direction[2]))

        for q, r, s in cells:
            if self.grid[(q, r, s)] == 0:
                continue

            current_pos = (q, r, s)
            current_val = self.grid[current_pos]

            # Find the furthest position the tile can move
            farthest_pos = current_pos
            while True:
                next_q = farthest_pos[0] + direction[0]
                next_r = farthest_pos[1] + direction[1]
                next_s = -next_q - next_r
                next_pos = (next_q, next_r, next_s)
                
                if next_pos not in self.get_all_cells() or self.grid[next_pos] != 0:
                    break
                farthest_pos = next_pos

            # If the tile moves, record the animation
            if farthest_pos != current_pos:
                animations.append({"type": "move", "value": current_val, "from": current_pos, "to": farthest_pos})
                self.grid[farthest_pos] = current_val
                self.grid[current_pos] = 0
                moved = True
            
            # Check for merge
            neighbor_q = farthest_pos[0] + direction[0]
            neighbor_r = farthest_pos[1] + direction[1]
            neighbor_s = -neighbor_q - neighbor_r
            neighbor_pos = (neighbor_q, neighbor_r, neighbor_s)

            if (neighbor_pos in self.get_all_cells() and
                    self.grid[neighbor_pos] == current_val and
                    neighbor_pos not in merged_this_move and
                    farthest_pos not in merged_this_move):
                
                # Animate the merge
                animations.append({"type": "move", "value": current_val, "from": farthest_pos, "to": neighbor_pos, "is_merge": True})
                
                self.grid[neighbor_pos] *= 2
                self.score += self.grid[neighbor_pos]
                self.grid[farthest_pos] = 0
                merged_this_move.add(neighbor_pos)
                moved = True
                # Add a "pop" animation for the merge
                animations.append({"type": "appear", "value": self.grid[neighbor_pos], "at": neighbor_pos, "is_merge": True})


        if moved:
            new_tile_info = self.add_random_tile()
            if new_tile_info:
                animations.append({"type": "appear", "value": new_tile_info["value"], "at": new_tile_info["cell"]})

        return moved, animations

    def can_move(self):
        if self.get_empty_cells():
            return True
        for q, r, s in self.get_all_cells():
            if self.grid[(q, r, s)] == 0:
                continue
            for direction in DIRECTIONS.values():
                neighbor_q = q + direction[0]
                neighbor_r = r + direction[1]
                neighbor_s = -neighbor_q - neighbor_r
                neighbor_pos = (neighbor_q, neighbor_r, neighbor_s)
                if neighbor_pos in self.get_all_cells() and self.grid[neighbor_pos] == self.grid[(q, r, s)]:
                    return True
        return False
