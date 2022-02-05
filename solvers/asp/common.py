"""
common.py

Contains routines common to clingo solvers.
"""

import time
import os
import argparse
from abc import ABC, abstractmethod
import clingo

from solvers.common.loaders import get_example_file


class Puzzle(ABC):
    """
    This is an abstract base class for a generic puzzle to be solved using Answer Set Programming.
    There are a few abstract methods to be implemented by subclasses.
    """
    
    def __init__(self):
        """
        Initialize storage for class variables.
        """
        self.args = None
    
    def solve(self):
        """
        This is the workhorse routine, which calls all other routines in turn. It is intended as the one-stop-shop
        for performing a solve.
        """
        # Handle command line arguments
        self.handle_args()
        if self.args.verbose:
            print(f'Analyzing {self.puzzletype} puzzle')
        
        # Construct the filename to load the puzzle from
        filename = self.args.filename or get_example_file(self.puzzletype)
        if self.args.verbose:
            print(f'Loading puzzle from {filename}')
        
        # Load puzzle file
        self.load_file(filename)
        
        # Load puzzle logic from file
        logic = self.get_logic()
        
        # Construct the puzzle definition
        puzzle_def = self.construct_puzzle_defs()
        
        # Combine scripts to get the full program
        program = (logic + '\n\n' + puzzle_def + '\n')
        if self.args.verbose:
            print(program)
        
        # Solve the system
        print('Beginning solve...')
        print()
        tic = time.perf_counter()
        self.clingo_solve(program)
        toc = time.perf_counter()
        print(f"Completed solving in {toc - tic:0.4f} seconds.")
    
    def handle_args(self):
        """
        Handle command line arguments.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('filename', nargs='?', help="Filename to read puzzle from", type=str, default=None)
        parser.add_argument("-t", "--tabbed",
                            help="Output grid using tabs instead of pretty printing",
                            action="store_true")
        parser.add_argument("-v", "--verbose",
                            help="Print verbose output (includes clingo script)",
                            action="store_true")
        parser.add_argument("-n", "--num", help="Number of solutions to search for (0=all)", type=int, default=0)
        self.args = parser.parse_args()
    
    def get_logic(self) -> str:
        """
        Returns the program in the puzzle logic (.pl) file for this class.
        """
        module_path = os.path.dirname(__file__)
        filename = os.path.join(module_path, 'clingo', f'{self.puzzletype}.pl')
        with open(filename) as f:
            logic = f.read()
        return logic.strip()
    
    def clingo_solve(self, program: str):
        """
        Run clingo over the given program, searching for the requested number of solutions.
        When a solution is found, the class' solution_handler function is called with the model.
        """
        # Set up the clingo solver
        control = clingo.Control()
        control.configuration.solve.models = self.args.num
        control.add("base", [], program)
        control.ground([("base", [])])

        # Iterate through solutions
        solutions = 0
        overlap = None
        with control.solve(yield_=True) as handler:
            for model in handler:
                solutions += 1
                print(f'Solution {solutions}:')
                atoms = model.symbols(shown=True)
                self.solution_handler(atoms)
                overlap = set(atoms) if overlap is None else overlap.intersection(set(atoms))
                print()
                
            if solutions > 1:
                print('Overlap of solutions:')
                self.overlap_handler(list(overlap))
                print()

            print('Search complete. ', end='')

            result = handler.get()
            if result.exhausted:
                if result.satisfiable:
                    if solutions == 1:
                        print('A single unique solution was found.')
                    else:
                        print(f'{solutions} solutions found (exhausted).')
                elif result.unsatisfiable:
                    print('No solutions possible.')
            else:
                print(f'{solutions}+ solutions found (not exhausted).')
            
    # Abstract methods

    @property
    @abstractmethod
    def puzzletype(self) -> str:
        """
        The name of the puzzle type. This corresponds to the filename for the example and the clingo logic files.
        This should be implemented as "puzzletype = '[insert name here]'".
        """
        raise NotImplementedError()
    
    @abstractmethod
    def construct_puzzle_defs(self) -> str:
        """
        This method is called to construct and return the clingo program to specify the puzzle definition.
        """
        raise NotImplementedError()
    
    @abstractmethod
    def load_file(self, filename: str):
        """
        This method is called to load a puzzle from a given file. It should save the results to class variables
        defined in the class' __init__ method.
        """
        raise NotImplementedError()

    def solution_handler(self, model):
        """
        Function that is called whenever a solution is found. This is intended to be subclassed.
        """
        for entry in model:
            print(entry.name, entry.arguments)

    def overlap_handler(self, model):
        """
        Function that is called whenever multiple solutions are found. This is intended to be subclassed.
        """
        for entry in model:
            print(entry.name, entry.arguments)
