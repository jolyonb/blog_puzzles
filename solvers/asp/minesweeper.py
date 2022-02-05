"""
minesweeper.py

Solves a solitaire minesweeper puzzle, such as presented here:
https://puzzlemadness.co.uk/minesweeper/

Capable of solving with or without a mine count constraint.

File format:
The first block describes the grid as specified in the puzzle.
Allowed characters include 0-8 for clues, period (.) for unknown cells,
* for mines, and # for excluded cells (if you have a non-rectangular
grid).
All lines in the grid must have the same length.

After the grid, you can include an empty line to begin the second block.
The lines that follow allow for comments (starting with a #) as well as
the following optional setting:
mine_count=#
This implements a global mine count constraint in the solver.
"""

from jinja2 import Template

from solvers.asp.common import Puzzle
from solvers.common.loaders import load_grid
from solvers.common.output import Colors, print_chars_with_color


template = """
% Puzzle Definition
% Numeric entries in the puzzle
% number(col, row, #).
{% for row, col, num in numbers %}
number({{ col }}, {{ row }}, {{ num }}).
{% endfor %}

{% if mines|length %}
% Mines in the puzzle
% mine(col, row).
{% for row, col in mines %}
mine({{ col }}, {{ row }}).
{% endfor %}
{% endif %}

{% if excluded|length %}
% Cells that are excluded from the puzzle grid
% excluded(col, row).
{% for row, col in excluded %}
excluded({{ col }}, {{ row }}).
{% endfor %}
{% endif %}

% Define our grid size
#const r={{ rows }}.
#const c={{ cols }}.

{% if mine_count > 0 %}
% Add in a mine count constraint
#const mine_count={{ mine_count }}.
:- #count{C, R: mine(C, R)} != mine_count.
{% endif %}
"""


class MineSweeper(Puzzle):
    """
    Class to handle MineSweeper puzzles.
    """

    puzzletype = 'minesweeper'
    
    def __init__(self):
        """
        Initialize storage for class variables.
        """
        super().__init__()
        self.grid = None
        self.settings = None
        self.rows = None
        self.cols = None
        self.mine_count = None
        self.numbers = None
        self.mines = None
        self.excluded = None

    def load_file(self, filename: str):
        """
        This method is called to load a puzzle from a given file. It should save the results to class variables
        defined in the class' __init__ method.
        """
        grid, settings = load_grid(filename, allowed_chars='012345678*#.', allowed_settings=['mine_count'])
        self.grid = grid
        self.settings = settings

        # Extract values from the grid and settings
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.mine_count = int(self.settings.get('mine_count', 0))
        self.numbers = []
        self.mines = []
        self.excluded = []
        for row, line in enumerate(self.grid):
            for col, char in enumerate(line):
                if char == '#':
                    self.excluded.append((row, col))
                elif char == '*':
                    self.mines.append((row, col))
                elif char in '012345678':
                    self.numbers.append((row, col, char))

    def construct_puzzle_defs(self) -> str:
        """
        This method is called to construct and return the clingo program to specify the puzzle definition.
        """
        renderer = Template(template, trim_blocks=True)
        return renderer.render(rows=self.rows,
                               cols=self.cols,
                               mine_count=self.mine_count,
                               numbers=self.numbers,
                               mines=self.mines,
                               excluded=self.excluded).strip()

    def solution_handler(self, model):
        """
        Function that is called whenever a solution is found.
        """
        # Construct an empty grid as a list of lists
        grid = [['.' for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Fill in the hint numbers and excluded cells
        for row, col, num in self.numbers:
            grid[row - 1][col - 1] = str(num)
        for row, col in self.excluded:
            grid[row - 1][col - 1] = '#'

        # Go and grab all the mines from the solution
        for entry in model:
            if entry.name == 'mine':
                col, row = entry.arguments
                grid[row.number][col.number] = '*'
                
        # Print the grid
        colors = {
            '*': Colors.YELLOW,
            '1': Colors.BLUE,
            '2': Colors.GREEN,
            '3': Colors.RED,
            '4': Colors.MAGENTA,
            '5': Colors.WHITE,
            '6': Colors.CYAN,
        }
        print_chars_with_color(grid, colors, self.args.tabbed)


if __name__ == '__main__':
    solver = MineSweeper()
    solver.solve()
