"""
tents.py

Solves a "Tents" or "Trees and Tents" puzzle, such as presented here:
https://www.puzzle-tents.com/

File format:
The first block describes the grid as specified in the puzzle.
Allowed characters include T for trees, period (.) for unknown cells,
and # for excluded cells (if you have a non-rectangular grid).
All lines in the grid must have the same length.

After the grid, include an empty line to begin the second block.
The lines that follow allow for comments (starting with a #) as well as
the following two required settings:
col_clues=a,b,c,d
row_clues=e,f,g,h
Each clue must be a number or null (empty). The number of column/row clues
must match the number of columns/rows in the grid.
"""

from jinja2 import Template
from typing import List

from solvers.asp.common import Puzzle
from solvers.common.loaders import load_grid
from solvers.common.output import Colors, print_chars_with_color

class Chars(object):
    TREE = 'T'
    TENT = 't'
    EMPTY = '.'
    UNKNOWN = '?'
    EXCLUDED = '#'

char_colors = {
    Chars.TREE: Colors.GREEN,
    Chars.TENT: Colors.YELLOW,
    Chars.EMPTY: Colors.WHITE,
}

template = """
% Puzzle Definition
% Define our grid size
#const r={{ rows }}.
#const c={{ cols }}.

% Place our trees
% tree(col, row).
{% for row, col in trees %}
tree({{ col }}, {{ row }}).
{% endfor %}

{% if tents|length %}
% Place our pre-placed tents
% tent(col, row).
{% for row, col in tents %}
tent({{ col }}, {{ row }}).
{% endfor %}
{% endif %}

{% if excluded|length %}
% Cells that are excluded from the puzzle grid
% excluded(col, row).
{% for row, col in excluded %}
excluded({{ col }}, {{ row }}).
{% endfor %}
{% endif %}

% Define our clues
% row_clues(col, row). and col_clues(col, row).
{% for clue in row_clues %}
{% if clue is not none %}
row_clues({{ loop.index - 1 }}, {{ clue }}).
{% endif %}
{% endfor %}
{% for clue in col_clues %}
{% if clue is not none %}
col_clues({{ loop.index - 1 }}, {{ clue }}).
{% endif %}
{% endfor %}
"""


class Tent(Puzzle):
    """
    Class to handle Tent puzzles.
    """

    puzzletype = 'tent'
    
    def __init__(self):
        """
        Initialize storage for class variables.
        """
        super().__init__()
        self.grid = None
        self.settings = None
        self.rows = None
        self.cols = None
        self.row_clues = None
        self.col_clues = None
        self.trees = None
        self.tents = None
        self.excluded = None

    def load_file(self, filename: str):
        """
        This method is called to load a puzzle from a given file. It should save the results to class variables
        defined in the class' __init__ method.
        """
        allowed = Chars.TREE + Chars.TENT + Chars.EMPTY + Chars.EXCLUDED
        grid, settings = load_grid(filename, allowed_chars=allowed, allowed_settings=['row_clues', 'col_clues'])
        self.grid = grid
        self.settings = settings
        if 'row_clues' not in settings:
            raise ValueError('The row_clues setting is missing from the puzzle definition.')
        if 'col_clues' not in settings:
            raise ValueError('The col_clues setting is missing from the puzzle definition.')

        # Extract values from the grid and settings
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        parser = lambda x: int(x) if x.isdigit() else None
        self.row_clues = [parser(x) for x in settings['row_clues'].split(',')]
        self.col_clues = [parser(x) for x in settings['col_clues'].split(',')]
        if len(self.row_clues) != self.rows:
            msg = f'The number of row clues ({len(self.row_clues)}) does not match the number of rows ({self.rows}).'
            raise ValueError(msg)
        if len(self.col_clues) != self.cols:
            msg = f'The number of column clues ({len(self.col_clues)}) does not match the number of columns ({self.cols}).'
            raise ValueError(msg)

        self.trees = []
        self.tents = []
        self.excluded = []
        for row, line in enumerate(self.grid):
            for col, char in enumerate(line):
                if char == Chars.EXCLUDED:
                    self.excluded.append((row, col))
                elif char == Chars.TREE:
                    self.trees.append((row, col))
                elif char == Chars.TENT:
                    self.tents.append((row, col))

    def construct_puzzle_defs(self) -> str:
        """
        This method is called to construct and return the clingo program to specify the puzzle definition.
        """
        renderer = Template(template, trim_blocks=True)
        return renderer.render(rows=self.rows,
                               cols=self.cols,
                               trees=self.trees,
                               tents=self.tents,
                               row_clues=self.row_clues,
                               col_clues=self.col_clues,
                               excluded=self.excluded).strip()

    def base_grid(self) -> List[List[str]]:
        """Constructs a list of lists of characters reflected the puzzle definition."""
        # Construct an empty grid as a list of lists
        grid = [[Chars.UNKNOWN for _ in range(self.cols)] for _ in range(self.rows)]

        # Fill in the trees
        for row, col in self.trees:
            grid[row][col] = Chars.TREE

        # Fill in excluded cells
        for row, col in self.excluded:
            grid[row][col] = Chars.EXCLUDED

        return grid

    def solution_handler(self, model):
        """
        Function that is called whenever a solution is found.
        """
        # Get the base grid
        grid = self.base_grid()

        # Process the model
        for entry in model:
            if entry.name == 'tent':
                col, row = entry.arguments
                grid[row.number][col.number] = Chars.TENT
            elif entry.name == 'empty':
                col, row = entry.arguments
                grid[row.number][col.number] = Chars.EMPTY

        # Print the grid
        print_chars_with_color(grid, char_colors, self.args.tabbed)

    def overlap_handler(self, model):
        """
        Function that is called whenever multiple solutions are found.
        """
        self.solution_handler(model)


if __name__ == '__main__':
    solver = Tent()
    solver.solve()
