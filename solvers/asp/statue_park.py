"""
statue_park.py

Solves a StatuePark puzzle, such as presented here:
https://www.gmpuzzles.com/blog/statue-park-rules-and-info/

File format:
The first block describes the grid as specified in the puzzle. In the grid,
period (.) indicates an empty cell, X indicates a black circle, and O
indicates a white circle. All lines in the grid must be the same length.

After the grid, include an empty line to begin the second block.
The lines that follow allow for comments (starting with a #), as well as
the following required settings:
tetrominos=LITSO
pentominos=FILNPTUVWXYZ
reflections=True
Include the letters that are available as tetrominos or pentominos. If
a letter is available multiple times, include it multiple times.
If reflections=False, then tetrominos also have JZ available, while
pentominos also ave QSJF'N'Y' available.
"""

from jinja2 import Template
from typing import List

from solvers.asp.common import Puzzle
from solvers.asp.shapes import get_clingo_definitions
from solvers.common.loaders import load_grid
from solvers.common.output import Colors, print_chars_with_color, print_chars_with_color_and_region
from solvers.common.regions import map_cells


class Chars(object):
    EMPTY = '.'
    UNKNOWN = '?'


char_colors = {
    # Tetrominos
    'L': Colors.RED,
    'I': Colors.YELLOW,
    'T': Colors.CYAN,
    'S': Colors.MAGENTA,
    'O': Colors.BLUE,
    'J': Colors.GREEN,
    'Z': Colors.WHITE,
    # Pentominos (extras needed)
    'F': Colors.RED,
    'N': Colors.YELLOW,
    'P': Colors.CYAN,
    'U': Colors.MAGENTA,
    'V': Colors.BLUE,
    'W': Colors.GREEN,
    'X': Colors.WHITE,
    'Y': Colors.RED,
    'Q': Colors.YELLOW,
    # Empty space
    Chars.EMPTY: Colors.WHITE,
}

template = """
% Puzzle Definitions
% Define our grid size
#const rows={{ rows }}.
#const cols={{ cols }}.

{% if black_circs|length %}
% Black circles
% black_circ(col, row).
{% for row, col in black_circs %}
black_circ({{ col }}, {{ row }}).
{% endfor %}
{% endif %}

{% if white_circs|length %}
% White circles
% white_circ(col, row).
{% for row, col in white_circs %}
white_circ({{ col }}, {{ row }}).
{% endfor %}
{% endif %}

% Shape definitions
{{ tetr_defs }}{{ pent_defs }}

% Each available shape must have a unique number.
% shape_entry(shape_num,shape_name).
{% for s in shape_names %}
shape_entry({{ loop.index }},{{ s }}). 
{% endfor %}
"""


class StatuePark(Puzzle):
    """
    Class to handle Statue Park puzzles.
    """

    puzzletype = 'statue_park'
    
    def __init__(self):
        """
        Initialize storage for class variables.
        """
        super().__init__()
        self.settings = None
        self.grid = None
        self.reflections = None
        self.tetrominos = None
        self.pentominos = None
        self.rows = None
        self.cols = None
        self.white_circs = None
        self.black_circs = None

    def load_file(self, filename: str):
        """
        This method is called to load a puzzle from a given file. It should save the results to class variables
        defined in the class' __init__ method.
        """
        allowed = '.XO'
        grid, settings = load_grid(filename, allowed_chars=allowed, allowed_settings=['reflections', 'tetrominos', 'pentominos'])
        self.grid = grid
        self.settings = settings
        self.reflections = settings.get('reflections', True)
        # Convert reflections from a string to a boolean
        if isinstance(self.reflections, str):
            self.reflections = self.reflections.lower() in ['1', 'true', 't', 'y', 'yes']
        self.tetrominos = settings['tetrominos'].upper()
        # Handle pentominos to catch reflections properly
        self.pentominos = []
        for c in settings['pentominos'].upper():
            if c != "'":
                self.pentominos.append(c)
            else:
                self.pentominos[-1] += "r"

        # Extract values from the grid and settings
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.black_circs = []
        self.white_circs = []
        for row, line in enumerate(self.grid):
            for col, char in enumerate(line):
                if char == 'X':
                    self.black_circs.append((row, col))
                elif char == 'O':
                    self.white_circs.append((row, col))

    def construct_puzzle_defs(self) -> str:
        """
        This method is called to construct and return the clingo program to specify the puzzle definition.
        """
        tetr_defs = get_clingo_definitions(self.tetrominos, self.reflections, category='tetr')
        pent_defs = get_clingo_definitions(self.pentominos, self.reflections, category='pent')
        shape_names = list(self.tetrominos) + [f'pent_{s}' for s in self.pentominos]
        shape_names = [x.lower() for x in shape_names]
        renderer = Template(template, trim_blocks=True)
        return renderer.render(white_circs=self.white_circs,
                               black_circs=self.black_circs,
                               tetr_defs=tetr_defs,
                               pent_defs=pent_defs,
                               rows=self.rows,
                               cols=self.cols,
                               shape_names=shape_names).strip()

    def base_grid(self) -> List[List[str]]:
        """Constructs a list of lists of characters reflected the puzzle definition."""
        # Construct an empty grid as a list of lists
        return [[Chars.UNKNOWN for _ in range(self.cols)] for _ in range(self.rows)]

    def solution_handler(self, model):
        """
        Function that is called whenever a solution is found.
        """
        # Get the base grid
        grid = self.base_grid()

        # Process the model
        for entry in model:
            if entry.name == 'black':
                col, row, _, shape = entry.arguments
                s = shape.name.upper()
                # Handle pentominos, including reflections
                s = s.removeprefix('PENT_')[0]
                grid[row.number][col.number] = s
            elif entry.name == 'white':
                col, row = entry.arguments
                grid[row.number][col.number] = Chars.EMPTY

        # Add in white o's
        for row, col in self.white_circs:
            grid[row][col] = 'o'

        # Print the grid
        print_chars_with_color(grid, char_colors, self.args.tabbed)


if __name__ == '__main__':
    solver = StatuePark()
    solver.solve()
