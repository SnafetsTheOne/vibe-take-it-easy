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




class Board:
    def __init__(self, rows):
        self.rows = rows
        self.grid = self.create_hex_grid()

    def create_hex_grid(self):
        grid = []
        for count in self.rows:
            grid.append([None for _ in range(count)])
        return grid

    def place_tile(self, row, col, tile):
        if self.grid[row][col] is None:
            self.grid[row][col] = tile
            return True
        return False

    def get_tile(self, r, c):
        if 0 <= r < len(self.grid) and 0 <= c < len(self.grid[r]):
            return self.grid[r][c]
        return None

    def get_vertical_lines(self):
        # Always return 5 vertical lines for a hexagonal board
        lines = [[] for _ in range(5)]
        center_row = len(self.rows) // 2
        for row, count in enumerate(self.rows):
            offset = (max(self.rows) - count) // 2
            for col in range(count):
                # The vertical line index for this tile
                line_idx = col - offset
                if 0 <= line_idx < 5:
                    lines[line_idx].append((row, col))
        return lines

    def get_diagonal_left_lines(self):
        lines = []
        max_cols = max(self.rows)
        for d in range(-max_cols+1, max_cols):
            line = []
            for row, count in enumerate(self.rows):
                offset = (max_cols - count) // 2
                c = row + d - offset
                if 0 <= c < count:
                    line.append((row, c))
            if line:
                lines.append(line)
        return lines

    def get_diagonal_right_lines(self):
        lines = []
        max_cols = max(self.rows)
        for d in range(-max_cols+1, max_cols):
            line = []
            for row, count in enumerate(self.rows):
                offset = (max_cols - count) // 2
                c = (count - 1) - (row + d - offset)
                if 0 <= c < count:
                    line.append((row, c))
            if line:
                lines.append(line)
        return lines

class BoardGUI:
    def __init__(self, root):
        self.rows = [1,2,3,2,3,2,3,2,1]
        self.root = root
        self.tiles = self.generate_tiles(sum(self.rows))
        self.current_tile_idx = 0
        self.board = Board(self.rows)
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
        score = 0
        # Vertical lines
        for line in self.board.get_vertical_lines():
            values = [self.board.get_tile(r, c).vertical if self.board.get_tile(r, c) else None for r, c in line]
            if all(x == values[0] and x is not None for x in values):
                score += sum(values)
        # Diagonal left lines
        for line in self.board.get_diagonal_left_lines():
            values = [self.board.get_tile(r, c).diag_left if self.board.get_tile(r, c) else None for r, c in line]
            if all(x == values[0] and x is not None for x in values):
                score += sum(values)
        # Diagonal right lines
        for line in self.board.get_diagonal_right_lines():
            values = [self.board.get_tile(r, c).diag_right if self.board.get_tile(r, c) else None for r, c in line]
            if all(x == values[0] and x is not None for x in values):
                score += sum(values)
        return score

    def generate_tiles(self, num_tiles):
        verticals = [1, 5, 9]
        diag_lefts = [2, 4, 8]
        diag_rights = [3, 6, 7]
        all_tiles = []
        for v in verticals:
            for dl in diag_lefts:
                for dr in diag_rights:
                    all_tiles.append(Tile(v, dl, dr))
        random.shuffle(all_tiles)
        return all_tiles[:num_tiles]

    def calculate_hex_centers(self):
        centers = []
        dx = self.hex_size * 3
        dy = self.hex_size * 0.9
        canvas_width = int(self.canvas['width'])
        canvas_height = int(self.canvas['height'])
        total_rows = len(self.rows)
        board_height = total_rows * dy
        offset_y = (canvas_height - board_height) / 2 + self.hex_size
        for r, count in enumerate(self.rows):
            row = []
            board_width = count * dx
            offset_x = (canvas_width - board_width) / 2 + self.hex_size
            for c in range(count):
                x = offset_x + c * dx
                y = offset_y + r * dy
                row.append((x, y))
            centers.append(row)
        return centers

    def draw_board(self):
        self.canvas.delete("all")
        for r, row in enumerate(self.board.grid):
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
        fill_color = "#f7f7f7"  # very light gray for all tiles
        self.canvas.create_polygon(points, outline="black", fill=fill_color, width=2, tags=f"hex_{row}_{col}")
        tile = self.board.grid[row][col]
        if tile:
            # Color maps
            vertical_colors = {1: "#888888", 5: "#0099ff", 9: "#ffe600"}
            diag_left_colors = {2: "#ffb6c1", 7: "#90ee90", 6: "#ff0000"}
            diag_right_colors = {3: "#ff69b4", 8: "#ffa500", 4: "#00cfff"}
            # Draw vertical line
            v_color = vertical_colors.get(tile.vertical, "#888888")
            self.canvas.create_line(x, y-size*0.8, x, y+size*0.8, fill=v_color, width=5)
            # Draw diagonal left line
            dl_color = diag_left_colors.get(tile.diag_left, "#ffb6c1")
            self.canvas.create_line(x-size*0.7, y-size*0.4, x+size*0.7, y+size*0.4, fill=dl_color, width=5)
            # Draw diagonal right line
            dr_color = diag_right_colors.get(tile.diag_right, "#ff69b4")
            self.canvas.create_line(x+size*0.7, y-size*0.4, x-size*0.7, y+size*0.4, fill=dr_color, width=5)
            # Draw numbers in matching colors
            font = ("Arial", 16, "bold")
            # Center positions for numbers
            self.canvas.create_text(x, y - size * 0.65, text=str(tile.vertical), font=font, fill="black")
            # Diagonal left: center between top left and bottom right
            dl_x = x - size * 0.45
            dl_y = y + size * 0.45
            self.canvas.create_text(dl_x, dl_y, text=str(tile.diag_left), font=font, fill="black")
            # Diagonal right: center between top right and bottom left
            dr_x = x + size * 0.45
            dr_y = y + size * 0.45
            self.canvas.create_text(dr_x, dr_y, text=str(tile.diag_right), font=font, fill="black")

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
        for r, row in enumerate(self.board.grid):
            for c, _ in enumerate(row):
                x, y = self.hex_centers[r][c]
                if self.point_in_hex(event.x, event.y, x, y, self.hex_size):
                    self.place_tile(r, c)
                    return

    def point_in_hex(self, px, py, hx, hy, size):
        # Simple circle check for click
        return (px - hx)**2 + (py - hy)**2 < (size * 0.95)**2

    def place_tile(self, row, col):
        tile = self.tiles[self.current_tile_idx]
        if self.board.place_tile(row, col, tile):
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
