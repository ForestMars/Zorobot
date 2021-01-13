# init.py - initialize zorobot installation settings.
# To be run during initial installation.

# import csv

from common import utils
from config.redis import *


def prefix_number(number):
    numba = str(number)

    if len(numba) == 10 and not numba.startswith('1'):

        return '+1' + numba

    elif len(numba) == 11 and numba.startswith('1'):

        return '+' + numba

    elif len(numba) == 12 and numba.startswith('+1'):
        return numba


def load_contacts():
    contacts = utils.csv_to_dict('assets/contacts.csv')
    for name, numba in contacts.items():
        numba = prefix_number(numba)
        r.set("contact:" + numba, name)


if __name__ == '__main__':
    load_contacts()
