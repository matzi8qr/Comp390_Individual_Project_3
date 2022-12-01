"""
A toolbox of utility functions
"""

import random
import string
import sys
import os


def generate_lock_file(size):
    """
    Generates the lock for a file to be encrypted under
    :param size: the lock depth of a given encryption
    :return: None
    """
    random_file_name = generate_unique_lock_file_name()
    try:
        return write_to_lock_file(random_file_name, size)
    except Exception as file_error:
        print(f'\n\tAn error occurred while trying to write to {random_file_name}: {file_error}\n')


def generate_unique_lock_file_name():
    """
    Handles the randomness of generating an encryption lock
    :return: random_file_name, the full name of the lock file.
    """
    # generate random lock file name: [random]_lock.txt
    files_in_dir = os.listdir()
    random_file_name = '_lock.txt'
    for _ in range(8):
        random_letter = random.choice(string.ascii_letters)
        random_file_name = random_letter + random_file_name
    for i in range(256):
        if random_file_name not in files_in_dir:
            return random_file_name
        random_letter = random.choice(string.ascii_letters)
        random_file_name[i % 8] = random_letter


def write_to_lock_file(file_name, size):
    """
    Encodes the lock into the file
    :param file_name: The generated lock file passed
    :param size: The lock depth
    :return: The file_name after the lock has been written
    """
    with open(file_name, 'w') as text_file:
        write_lock_values_to_file(size, text_file)
        return file_name


def write_lock_values_to_file(size, file_obj):
    """
    Writes the lock values to the file
    :param size: The depth of the lock
    :param file_obj: The _lock file to write to
    :return: None
    """
    for line_ct in range(int(size)):
        rand_int1 = random.randint(0, sys.maxsize)
        if line_ct < int(size) - 1:
            print(f'{rand_int1}', file=file_obj)
            continue
        file_obj.write(f'{rand_int1}')


def validate_lock_depth(depth):
    """
    Validates the user input for lock_depth
    :param depth: The list of arguments passed to validate depth from
    :raises: IndexError if no depth argument is passed
    :raises: ValueError if lock depth is passed as a negative integer or if it's not an integer at all
    :return: None
    """
    try:
        lock_depth = int(depth[0])
    except ValueError as exc:
        print(f'\n\tInvalid lock depth: \'{depth[0]}\'. Must be an integer greater than 0 (zero).\n')
        raise exc
    except IndexError as exc:
        print(f'\n\tNo lock depth given: Please pass an integer greater than 0 (zero).\n')
        raise exc
    # check if lock depth is greater than zero
    if lock_depth <= 0:
        print(f'\n\tInvalid lock depth: \'{depth[0]}\'. Must be an integer greater than 0 (zero).\n')
        raise ValueError
