#!/usr/bin/env python
"""
hide.py - remove solution code and execute generated notebook
"""

import jupytext
import os
import re
import subprocess
import sys

def delete_first(infile: str) -> None:
    """Remove solutions before running the code."""
    outfile = infile.replace('.sol', '')
    hide = False
    with open(infile, 'r') as solutions:
        with open(outfile, 'w') as exercises:
            for line in solutions:
                if line.endswith('pass\n'):
                    hide = not hide
                elif '<!--' in line:
                    hide = True
                if not hide:
                    exercises.write(line)
                if hide and '-->' in line:
                    hide = False
    subprocess.run(f'jupytext --to ipynb --execute {outfile}', shell=True)

def run_first(infile: str) -> None:
    """Remove solutions after running the code."""
    outfile = infile.replace('.sol', '')
    hide = False
    with open(infile, 'r') as solutions:
        with open(outfile, 'w') as exercises:
            for line in solutions:
                if '<!--' in line:
                    hide = True
                if not hide:
                    exercises.write(line)
                if hide and '-->' in line:
                    hide = False
    subprocess.run(f'jupytext --to ipynb --execute {outfile}', shell=True)
    nbfile = outfile.replace('.md', '.ipynb')
    nb = jupytext.read(nbfile)
    solution = re.compile(r'pass\n.*?pass', flags=re.DOTALL)
    for cell in nb.cells:
        if cell.cell_type == 'code' and 'pass' in cell.source:
            cell.source = solution.sub('pass', cell.source)
            print(cell.source)
    jupytext.write(nb, nbfile)

if sys.argv[1] == '-d':
    delete_first(sys.argv[2])
elif sys.argv[1] == '-r':
    run_first(sys.argv[2])
else:
    print("""\
Usage: hide -d|-r file.sol.md

Removes comments and solutions (code between two pass statements)
Generates file.ipynb and executes it

-d  first delete solutions, then run code
-r  first run code, then delete solutions
""")
