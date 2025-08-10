"""
Take It Easy - GUI Version (tkinter)
"""
import tkinter as tk
import random

class Tile:
    def __init__(self, vertical, diag_left, diag_right):
        self.vertical = vertical
        self.diag_left = diag_left
        self.diag_right = diag_right
    def __repr__(self):
        return f"({self.vertical},{self.diag_left},{self.diag_right})"


import math




class BoardGUI:
    def __init__(self, root):
        # Take It Easy board setup: 1-2-3-2-3-2-3-2-1 (hexagon, 19 spaces)
        self.rows = [1,2,3,2,3,2,3,2,1]
        self.root = root
        self.tiles = self.generate_tiles(sum(self.rows))
        self.current_tile_idx = 0
        self.grid = self.create_hex_grid()
        self.info_label = tk.Label(root, text="Take It Easy - Place the tiles!")
        self.info_label.pack()
        self.tile_label = tk.Label(root, text="")
        self.tile_label.pack()
        self.tile_canvas = tk.Canvas(root, width=100, height=100, bg="white", highlightthickness=0)
        self.tile_canvas.pack()
    self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
    self.canvas.pack()
    self.hex_size = 40
    self.hex_centers = self.calculate_hex_centers()
    self.draw_board()
    self.update_tile_label()
    self.draw_current_tile()
    self.canvas.bind("<Button-1>", self.on_canvas_click)
    self.score_button = tk.Button(root, text="Show Score", command=self.show_score)
    self.score_button.pack()
    self.score_label = tk.Label(root, text="Score: 0")
    self.score_label.pack()
    def show_score(self):
        score = self.calculate_score()
        self.score_label.config(text=f"Score: {score}")

    def calculate_score(self):
        # Helper to get tile or None
        def get_tile(r, c):
            if 0 <= r < len(self.grid) and 0 <= c < len(self.grid[r]):
                return self.grid[r][c]
            return None

        score = 0
        # Vertical lines (columns)
        for col in range(5):
            line = []
            for row in range(len(self.grid)):
                # Calculate column index for each row
                offset = row - 2
                c = col - max(0, offset)
                if 0 <= c < len(self.grid[row]):
                    tile = get_tile(row, c)
                    if tile:
                        line.append(tile.vertical)
                    else:
                        line.append(None)
            if all(x == line[0] and x is not None for x in line):
                score += sum(line)

        # Diagonal lines (top-left to bottom-right)
        for d in range(-2, 3):
            line = []
            for row in range(len(self.grid)):
                c = row + d
                if 0 <= c < len(self.grid[row]):
                    tile = get_tile(row, c)
                    if tile:
                        line.append(tile.diag_left)
                    else:
                        line.append(None)
            if all(x == line[0] and x is not None for x in line):
                score += sum(line)

        # Diagonal lines (top-right to bottom-left)
        for d in range(-2, 3):
            line = []
            for row in range(len(self.grid)):
                c = (len(self.grid[row]) - 1) - (row + d)
                if 0 <= c < len(self.grid[row]):
                    tile = get_tile(row, c)
                    if tile:
                        line.append(tile.diag_right)
                    else:
                        line.append(None)
            if all(x == line[0] and x is not None for x in line):
                score += sum(line)

        return score

    def create_hex_grid(self):
        grid = []
        for count in self.rows:
            grid.append([None for _ in range(count)])
        return grid

    def generate_tiles(self, num_tiles):
        # Correct sets for Take It Easy
        verticals = [1, 5, 9]
        diag_lefts = [2, 4, 8]
        diag_rights = [3, 6, 7]
        # All unique combinations
        all_tiles = []
        for v in verticals:
            for dl in diag_lefts:
                for dr in diag_rights:
                    all_tiles.append(Tile(v, dl, dr))
        random.shuffle(all_tiles)
        return all_tiles[:num_tiles]

    def calculate_hex_centers(self):
        centers = []
        dx = self.hex_size * 3 # horizontal distance: edge-to-edge
        dy = self.hex_size * 0.9 # vertical overlap
        canvas_width = int(self.canvas['width'])
        canvas_height = int(self.canvas['height'])
        total_rows = len(self.rows)
        board_height = total_rows * dy
        offset_y = (canvas_height - board_height) / 2 + self.hex_size
        for r, count in enumerate(self.rows):
            row = []
            board_width = count * dx
            offset_x = (canvas_width - board_width) / 2 + self.hex_size
            # Offset only the 2nd and 4th rows (index 1 and 3)
            for c in range(count):
                x = offset_x + c * dx
                y = offset_y + r * dy
                row.append((x, y))
            centers.append(row)
        return centers

    def draw_board(self):
        self.canvas.delete("all")
        for r, row in enumerate(self.grid):
            for c, _ in enumerate(row):
                x, y = self.hex_centers[r][c]
                self.draw_hex(x, y, r, c)

    def draw_hex(self, x, y, row, col):
        size = self.hex_size
        points = []
        for i in range(6):
            angle = math.pi / 3 * i
            px = x + size * math.cos(angle)
            py = y + size * math.sin(angle)
            points.extend([px, py])
        fill_color = "#e0e0e0" if self.grid[row][col] is None else "#aee1f9"
        self.canvas.create_polygon(points, outline="black", fill=fill_color, width=2, tags=f"hex_{row}_{col}")
        tile = self.grid[row][col]
        if tile:
            self.canvas.create_text(x, y, text=str(tile.vertical), font=("Arial", 14, "bold"))
            self.canvas.create_text(x - size/2.2, y - size/2.2, text=str(tile.diag_left), font=("Arial", 10))
            self.canvas.create_text(x + size/2.2, y - size/2.2, text=str(tile.diag_right), font=("Arial", 10))

    def update_tile_label(self):
        if self.current_tile_idx < len(self.tiles):
            self.tile_label.config(text=f"Current Tile: {self.tiles[self.current_tile_idx]}")
        else:
            self.tile_label.config(text="Game Over!")
        self.draw_current_tile()

    def draw_current_tile(self):
        self.tile_canvas.delete("all")
        if self.current_tile_idx < len(self.tiles):
            tile = self.tiles[self.current_tile_idx]
            x, y = 50, 50
            size = 35
            points = []
            for i in range(6):
                angle = math.pi / 3 * i
                px = x + size * math.cos(angle)
                py = y + size * math.sin(angle)
                points.extend([px, py])
            self.tile_canvas.create_polygon(points, outline="black", fill="#aee1f9", width=2)
            self.tile_canvas.create_text(x, y, text=str(tile.vertical), font=("Arial", 14, "bold"))
            self.tile_canvas.create_text(x - size/2.2, y - size/2.2, text=str(tile.diag_left), font=("Arial", 10))
            self.tile_canvas.create_text(x + size/2.2, y - size/2.2, text=str(tile.diag_right), font=("Arial", 10))

    def on_canvas_click(self, event):
        if self.current_tile_idx >= len(self.tiles):
            return
        # Find which hex was clicked
        for r, row in enumerate(self.grid):
            for c, _ in enumerate(row):
                x, y = self.hex_centers[r][c]
                if self.point_in_hex(event.x, event.y, x, y, self.hex_size):
                    self.place_tile(r, c)
                    return

    def point_in_hex(self, px, py, hx, hy, size):
        # Simple circle check for click
        return (px - hx)**2 + (py - hy)**2 < (size * 0.95)**2

    def place_tile(self, row, col):
        if self.grid[row][col] is None:
            tile = self.tiles[self.current_tile_idx]
            self.grid[row][col] = tile
            self.current_tile_idx += 1
            self.draw_board()
            self.update_tile_label()
        else:
            self.info_label.config(text="Position already occupied!")

def main():
    root = tk.Tk()
    root.title("Take It Easy - Python GUI")
    BoardGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
