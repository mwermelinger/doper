#!/usr/bin/env python
"""
hide.py - remove solution code and execute generated notebook
"""

import subprocess
import sys
import os

if sys.argv[1] == '-h':
    print("""\
Usage: hide file.sol.md

Removes comments and solutions (code between two pass statements)
Generates file.ex.ipynb and executes it
""")
    sys.exit()

infile = sys.argv[1]
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

command = 'jupytext --to notebook --execute'    # convert to .ipynb and run it
subprocess.run(f'{command} {outfile}', shell=True)
