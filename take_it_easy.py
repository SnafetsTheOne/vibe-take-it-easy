"""
Take It Easy - Python Implementation
A simplified version of the tile-laying game.
"""
import random
from typing import List, Tuple

# Each tile has three numbers: vertical, diagonal left, diagonal right
class Tile:
    def __init__(self, vertical: int, diag_left: int, diag_right: int):
        self.vertical = vertical
        self.diag_left = diag_left
        self.diag_right = diag_right
    def __repr__(self):
        return f"({self.vertical},{self.diag_left},{self.diag_right})"

# Board is a 2D grid (simplified for demo)
class Board:
    def __init__(self, size: int = 5):
        self.size = size
        self.grid: List[List[Tile or None]] = [[None for _ in range(size)] for _ in range(size)]
    def place_tile(self, row: int, col: int, tile: Tile):
        if self.grid[row][col] is None:
            self.grid[row][col] = tile
            return True
        return False
    def display(self):
        for row in self.grid:
            print(' '.join(str(tile) if tile else "___" for tile in row))

# Generate a set of random tiles
def generate_tiles(num_tiles: int) -> List[Tile]:
    tiles = []
    for _ in range(num_tiles):
        tiles.append(Tile(random.randint(1,9), random.randint(1,9), random.randint(1,9)))
    return tiles

def main():
    board = Board(size=5)
    tiles = generate_tiles(25)
    print("Welcome to Take It Easy!")
    for idx, tile in enumerate(tiles):
        board.display()
        print(f"Tile {idx+1}: {tile}")
        pos = input("Enter row,col to place tile (e.g., 0,0): ")
        try:
            row, col = map(int, pos.split(','))
            if not board.place_tile(row, col, tile):
                print("Position already occupied. Try again.")
        except Exception:
            print("Invalid input. Try again.")
    print("Final Board:")
    board.display()
    # Scoring logic can be added here

if __name__ == "__main__":
    main()
