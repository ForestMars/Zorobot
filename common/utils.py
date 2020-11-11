# utils.py - Commonly used helper functions.
__version__ = '0.1'
#__all__ = []

import os
import csv

try:
    import cPickle as pickle
except ImportError:
    import pickle

#import logger
#logger = logging.getLogger(__name__)

class HaltException(Exception): pass

def get_reg_files(dir: str, ext: str='csv') -> list:
    """ Decrator for all filesystem fetching operations. Returns list of entries for given directory, excuding hidden files. """
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.abspath(os.path.join(dir, f))) and not f.startswith('.')]
    return files

def file_util(file: str, dir: str='.'):
    """ Placeholder for file utility """
    pass

def read_file(file: str, dir: str='.'):
    f = open(file, "r")
    return f.read()

def write_file(contents, file: str, dir: str='.'):
    f = open(file, "rw")
    f.write(contents)
    f.close()

def append_file(contents, file: str, dir: str='.'):
    f = open(file, "a")
    f.write(contents)
    f.close()
