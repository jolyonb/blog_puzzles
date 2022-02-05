"""
loaders.py

Contains routines common to loading files from disk.
"""

import os
from typing import List, Tuple, Dict


def get_example_file(puzzletype: str) -> str:
    """
    Returns the example filename for the given puzzle type.
    """
    module_path = os.path.dirname(__file__)
    return os.path.join(module_path, '..', '..', 'examples', f'{puzzletype}.txt')


def load_grid(filename: str,
              allowed_chars: str,
              allowed_settings: List[str] = None
              ) -> Tuple[List[str], Dict[str, str]]:
    """
    Loads a square grid from the given filename.
    
    After the grid, optional settings are allowed. Leave an empty line after the grid, then include settings as
    "setting_name=value". Any line starting with # in the settings section is treated as a comment and ignored.
    """
    with open(filename) as f:
        lines = f.readlines()
        # Remove newline characters
        lines = [line.rstrip('\n') for line in lines]
    
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
            for c in line:
                if c not in allowed_chars:
                    raise ValueError(f'Invalid character in grid: "{c}"')
            grid.append(line)
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
