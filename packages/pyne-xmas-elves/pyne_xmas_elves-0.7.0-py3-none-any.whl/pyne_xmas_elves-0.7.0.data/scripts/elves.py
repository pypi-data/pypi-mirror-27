#!python
import os
import sys

from argparse import ArgumentParser
from importlib import import_module


parser = ArgumentParser(description='Run the elves game.')
parser.add_argument('module', type=str, help='The module name to load.')
args = parser.parse_args()

current_dir = os.path.abspath(os.path.curdir)
sys.path.append(current_dir)
module = import_module(args.module)
game = module.Game()
game.run()
