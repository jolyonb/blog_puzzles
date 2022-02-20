"""
output.py

Contains definitions for outputting results to a terminal.
"""

from typing import List, Dict, Union

# Box characters
# '─',  # u2500
# '│',  # u2502
# '┌',  # u250C
# '├',  # u251C
# '┬',  # u252C
# '┼',  # u253C
# '┐',  # u2510
# '┤',  # u2524
# '┴',  # u2534
# '└',  # u2514
# '┘',  # u2518
# '═',  # u2550
# '║',  # u2551


# Map tuples of characters around a cell to figure out what connective entry is needed
box_mapping = {
    # (above, below, left, right)
    (' ', '│', ' ', '─'): '┌',
    ('│', '│', ' ', '─'): '├',
    (' ', '│', '─', '─'): '┬',
    ('│', '│', '─', '─'): '┼',
    (' ', '│', '─', ' '): '┐',
    ('│', '│', '─', ' '): '┤',
    ('│', ' ', '─', '─'): '┴',
    ('│', ' ', ' ', '─'): '└',
    ('│', ' ', '─', ' '): '┘',
    ('│', '│', ' ', ' '): '│',
    (' ', ' ', '─', '─'): '─',
    (' ', ' ', ' ', ' '): ' ',
}

loop_directions = {
    'ew': '─',
    'ns': '│',
    'se': '┌',
    'sw': '┐',
    'ne': '└',
    'nw': '┘'
}


class Colors:
    BLACK = '\u001b[30m'
    RED = '\u001b[31m'
    GREEN = '\u001b[32m'
    YELLOW = '\u001b[33m'
    BLUE = '\u001b[34m'
    MAGENTA = '\u001b[35m'
    CYAN = '\u001b[36m'
    WHITE = '\u001b[37m'
    RESET = '\u001b[0m'


def print_chars_with_color(chars: Union[List[str], List[List[str]]],
                           colors: Dict[str, str] = None,
                           tabbed: bool = False):
    """
    Take in a list of strings. Print them a single character at a time, using the colors dict to color
    individual characters. If tabbed is True, outputs a tab between each character.
    """
    endchar = '\t' if tabbed else ''
    for row in chars:
        for char in row:
            if char in colors:
                print(colors[char], end='')
        
            print(char, end=endchar)
        
            # Reset colors
            print(Colors.RESET, end='')
        print()


def buffer_grid(grid: Union[List[str], List[List[str]]]) -> List[List[str]]:
    """Takes in a grid of characters, and inserts extra columns and rows between every character"""
    rows = len(grid)
    cols = len(grid[0])

    newgrid = [[' ' for _ in range(2 * cols + 1)] for _ in range(2 * rows + 1)]

    for row_idx, line in enumerate(grid):
        for col_idx, char in enumerate(line):
            newgrid[2 * row_idx + 1][2 * col_idx + 1] = char

    return newgrid


def print_chars_with_color_and_region(chars: Union[List[str], List[List[str]]],
                                      regions: Union[List[str], List[List[str]]],
                                      colors: Dict[str, str] = None,
                                      outside_region_char: str = ''):
    """
    Take in a list of strings, where each character lives in a region as defined by the regions list.
    Print boxes around all regions, and print characters in their region, using the colors dict to
    color individual characters.
    
    Does not work with tabbed mode!
    """

    rows = len(chars)
    cols = len(chars[0])

    def out_of_box(row, col) -> bool:
        """Returns True if the requested cell is out of the grid, or False if it's in the grid."""
        return row < 0 or col < 0 or row >= rows or col >= cols
        
    def regions_different(r1, c1, r2, c2) -> bool:
        """
        Compare two cells. If they are in different regions, return True. Else, return False.
        If a cell is outside the grid, use the outside_region_char for that cell's region.
        """
        cell1 = outside_region_char if out_of_box(r1, c1) else regions[r1][c1]
        cell2 = outside_region_char if out_of_box(r2, c2) else regions[r2][c2]
        return cell1 != cell2

    def get_entry(grid, row, col):
        """Returns the requested grid entry, returning a space if out of bounds"""
        if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]):
            return ' '
        return grid[row][col]

    # Take our old grid of characters (r, c) and turn it into a new grid (2r+1, 2c+1)
    newgrid = buffer_grid(chars)

    # Use region comparison to fill in (odd, even) and (even, odd) cells
    for row_idx, line in enumerate(newgrid):
        for col_idx, _ in enumerate(line):
            if row_idx % 2 == 1 and col_idx % 2 == 0:
                # Row is odd, column is even
                # If the spots left and right are in different regions, add a "|"
                cell_row = (row_idx - 1) // 2
                cell_col1 = col_idx // 2
                cell_col2 = col_idx // 2 - 1
                if regions_different(cell_row, cell_col1, cell_row, cell_col2):
                    newgrid[row_idx][col_idx] = '│'
            elif row_idx % 2 == 0 and col_idx % 2 == 1:
                # Row is even, column is odd
                # If the spots above and below are in different regions, add a "-"
                cell_row1 = row_idx // 2
                cell_row2 = row_idx // 2 - 1
                cell_col = (col_idx - 1) // 2
                if regions_different(cell_row1, cell_col, cell_row2, cell_col):
                    newgrid[row_idx][col_idx] = '─'

    # Look at all even-even gridpoints and figure out what connection is needed
    for row_idx, line in enumerate(newgrid):
        if row_idx % 2 == 1:
            continue
        for col_idx, _ in enumerate(line):
            if col_idx % 2 == 1:
                continue
            # Get points above, below, left and right
            above = get_entry(newgrid, row_idx - 1, col_idx)
            below = get_entry(newgrid, row_idx + 1, col_idx)
            left = get_entry(newgrid, row_idx, col_idx - 1)
            right = get_entry(newgrid, row_idx, col_idx + 1)
            # Assign the appropriate connective piece
            newgrid[row_idx][col_idx] = box_mapping[(above, below, left, right)]

    # Print the resulting grid
    print_chars_with_color(newgrid, colors, False)
