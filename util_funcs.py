import random
import string
import sys
import os


def generate_lock_file(size):
    # generate random lock file name: [random]_lock.txt
    files_in_dir = os.listdir()
    while True:
        random_file_name = '_lock.txt'
        for _ in range(8):
            random_letter = random.choice(string.ascii_letters)
            random_file_name = random_letter + random_file_name
        if random_file_name not in files_in_dir:
            break

    with open(random_file_name, 'w') as text_file:
        for line_ct in range(int(size)):
            rand_int1 = random.randint(0, sys.maxsize)
            if line_ct < int(size) - 1:
                print(f'{rand_int1}', file=text_file)
                continue
            text_file.write(f'{rand_int1}')

    return random_file_name
