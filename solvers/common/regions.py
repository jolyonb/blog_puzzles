"""
regions.py

Contains routines to assist with handling regions.
"""

from typing import List, Tuple

def map_cells(regions: List[str], excluded: str = '') -> List[Tuple[int, int, int]]:
    """
    Take in a list of strings representing a grid, where each cell is assigned a unique character.
    Return a list of tuples (row, column, region_number), all 0-indexed.
    If excluded is provided, any cell with a character in excluded if ignored.
    """
    regionmap = {}
    regioncount = -1
    cells = []
    for row_idx, line in enumerate(regions):
        for col_idx, char in enumerate(line):
            if char in excluded:
                continue
            if char not in regionmap:
                regioncount += 1
                regionmap[char] = regioncount
            cells.append((row_idx, col_idx, regionmap[char]))

    return cells
