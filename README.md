# Logic Puzzle Solvers

I've been interested for a while in writing a collection of programs to solve logic puzzles. In this repository, I'm finally taking a stab at this goal. I'm planning on writing about each of these solvers on [my blog](https://blog.dodgyfysix.com), if you're curious to read more about them.

Solvers are divided into three categories:
* Answer Set Programming (ASP) solvers. These solvers code the rules for a puzzle in the language of ASP, and use `clingo` to solve them. These puzzles have a light python wrapper around them for reading puzzles from file and outputting the solutions nicely. These solvers will either solve the puzzle completely, or give up and produce nothing.
* Brute force solvers. These are just python programs that try every possibility to find the solution. There's usually nothing elegant about these, but they're sometimes all that you need. Again, these solvers will either solve the puzzle completely, or give up and produce nothing.
* Logic solvers. These are python programs that attempt to solve puzzles the same way a human does. When human heuristics break down, they will tend to resort to Ariadne's thread to break through the barriers. These solvers can typically be requested to stop if they run out of heuristics to try, which makes them particularly useful when solving a composite puzzle.

Each solver is coded in Python 3.10; the environment used in the coding is stored in conda.yml (intended to be loaded with anaconda).

The solvers are standalone python scripts, although they are in a package structure so as to allow for simple code reuse on common functionality. You can learn more about each script by reading the docstring at the top of the file. You may also like to run the file with a `-h` argument to see the available command line arguments.

## List of Solvers

The below links are to the rules for the puzzle as implemented in the solvers here.

### ASP Solvers

* [Minesweeper](rules/minesweeper.md) ([Blog post 1](https://blog.dodgyfysix.com/2022/02/02/minesweeper-solver-in-asp/), [Blog post 2](https://blog.dodgyfysix.com/2022/02/05/minesweeper-in-asp-part-ii/))
* [Tent (Tents and Trees)](rules/tent.md) ([Blog post](https://blog.dodgyfysix.com/2022/02/06/tent-puzzles-in-asp/))
* [Star Battle](rules/starbattle.md) (including shapeless variant) ([Blog post](https://blog.dodgyfysix.com/2022/02/20/star-battle-puzzles-in-asp/))
* [Slitherlink (Fences, Loop the Loop, Loop)](rules/slitherlink.md) ([Blog post](https://blog.dodgyfysix.com/2022/02/09/slitherlink-puzzles-in-asp/))
* [Hashi (Bridges)](rules/hashi.md) ([Blog post](https://blog.dodgyfysix.com/2022/02/20/hashi-puzzles-in-asp/))
* [Yajilin (Arrow Ring)](rules/yajilin.md) (including a number of variants) ([Blog post](https://blog.dodgyfysix.com/2022/02/20/yajilin-puzzles-in-asp/))
* [Hitori (Alone/One Person/Leave Me Alone)](rules/hitori.md) ([Blog post](https://blog.dodgyfysix.com/2022/02/26/hitori-puzzles-in-asp/))
* [LITS (Nuruomino)](rules/lits.md) ([Blog post](https://blog.dodgyfysix.com/2022/02/26/lits-puzzles-in-asp/))
* [Statue Park](rules/statue_park.md)

Other ASP solvers without a python wrapper are documented [here](other%20asp%20solvers/README.md).

### Brute Force Solvers

* Coming Soon!

### Logic Solvers

* Coming Soon!


## List of puzzle types I'd like to write a solver for

* Battleships/Bimaru
* Shakura
* Nurikabe
* Shakashaka
* Nonogram
* Sudoku + variants
* Ripple Effect
* Hidato/numberlink
* Skyscraper
* Masyu
* Corral/cave/bag
* Heyawake
* Akari
* Kakuro
* Tapa
