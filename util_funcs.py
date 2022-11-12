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


# test function calls

# a lock depth of 10,000,000 seems to be the reasonable limit for processing time

# lock_file = generate_lock_file(10000000)
# encrypt_msg_file = lock('Bob', lock_file)
# unlock(encrypt_msg_file)
#
# lock_file = generate_lock_file(20)
# encrypt_msg_file1 = lock('Decoded_Message', lock_file)
# unlock(encrypt_msg_file1)
#
# lock_file = generate_lock_file(20)
# encrypt_msg_file2 = lock('Password123abc', lock_file)
# unlock(encrypt_msg_file2)
