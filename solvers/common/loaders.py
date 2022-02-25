"""
loaders.py

Contains routines common to loading files from disk.
"""

from typing import List, Tuple, Dict
from pathlib import Path


def get_example_file(puzzletype: str) -> str:
    """
    Returns the example filename for the given puzzle type.
    """
    file_path = Path(__file__).parents[2] / 'examples' / f'{puzzletype}.txt'
    return str(file_path)


def load_grid(filename: str,
              allowed_chars: str,
              allowed_settings: List[str] = None,
              allowed_delimiters: str = None,
              ) -> Tuple[List[str], Dict[str, str]]:
    """
    Loads a square grid from the given filename.

    If allowed_delimiters is set (typically to ',\t'), then if one of those characters is detected in the first
    row, it will be treated as the delimiter between all cells.
    
    After the grid, optional settings are allowed. Leave an empty line after the grid, then include settings as
    "setting_name=value". Any line starting with # in the settings section is treated as a comment and ignored.
    """
    with open(filename) as f:
        lines = f.readlines()
        # Remove newline characters
        lines = [line.rstrip('\n') for line in lines]

    # Identify if a delimiter is used
    delimiter = None
    if allowed_delimiters:
        for x in allowed_delimiters:
            if x in lines[0]:
                delimiter = x
                break

    allowed_settings = allowed_settings or []
    in_grid = True
    grid = []
    settings = {}
    for line in lines:
        # Check if we're done with the grid
        if in_grid and line == '':
            in_grid = False
        
        if in_grid:
            # Append to the grid
            clean_line = line.split(delimiter) if delimiter else line
            for entry in clean_line:
                for c in entry:
                    if c not in allowed_chars:
                        raise ValueError(f'Invalid character in grid: "{c}"')
            grid.append(clean_line)
        elif line != '':
            # Handle setting
            if line.startswith('#'):
                # Treat as a comment
                continue
            if '=' not in line:
                raise ValueError(f'Error reading line: "{line}"; expected = to appear in setting')
            key, val = line.split('=', 1)
            if key not in allowed_settings:
                raise ValueError(f'Unknown setting: "{key}')
            if key in settings:
                raise ValueError(f'Duplicate setting: "{key}')
            settings[key] = val
    
    # Check that all grid entries have the same length
    count = len(grid[0])
    for line in grid:
        if len(line) != count:
            raise ValueError(f'Bad line in grid: "{line}"; was expecting length {count} but found length {len(line)}')
    
    return grid, settings


def load_2grids(filename: str,
                allowed_chars1: str,
                allowed_chars2: str,
                allowed_settings: List[str] = None
                ) -> Tuple[List[str], List[str], Dict[str, str]]:
    """
    Loads two square grids from the given filename, separated by a blank line. The two grids just have the same shape.

    After the grids, optional settings are allowed. Leave an empty line after the grid, then include settings as
    "setting_name=value". Any line starting with # in the settings section is treated as a comment and ignored.
    """
    with open(filename) as f:
        lines = f.readlines()
        # Remove newline characters
        lines = [line.rstrip('\n') for line in lines]

    allowed_settings = allowed_settings or []
    grids = ([], [])
    allowed_chars = (allowed_chars1, allowed_chars2)
    current_grid = 0
    settings = {}
    for line in lines:
        # Check if we're done with the current grid
        if current_grid < 2 and line == '':
            current_grid += 1
            continue

        if current_grid < 2:
            # Append to the grid
            for c in line:
                if c not in allowed_chars[current_grid]:
                    raise ValueError(f'Invalid character in grid: "{c}"')
            grids[current_grid].append(line)
        elif line != '':
            # Handle setting
            if line.startswith('#'):
                # Treat as a comment
                continue
            if '=' not in line:
                raise ValueError(f'Error reading line: "{line}"; expected = to appear in setting')
            key, val = line.split('=', 1)
            if key not in allowed_settings:
                raise ValueError(f'Unknown setting: "{key}')
            if key in settings:
                raise ValueError(f'Duplicate setting: "{key}')
            settings[key] = val

    # Check that all grids have the same rectangular shape
    rows = len(grids[0])
    cols = len(grids[0][0])
    for grid in grids:
        if len(grid) != rows:
            raise ValueError(f'Grids have different row counts. Was expecting {rows} but found {len(grid)}.')
        for line in grid:
            if len(line) != cols:
                raise ValueError(f'Bad line in grid: "{line}"; was expecting length {cols} but found length {len(line)}')

    return grids[0], grids[1], settings
