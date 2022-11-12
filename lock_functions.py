import random
import string
import os
import json
from math_functions import modinv


def lock(message, lock_file_name):

    # Declare and Initialize key file dictionary
    key_dict = {
        'm_value': 0,
        'lock_file': lock_file_name,
        'lock_file_seq_key': None,
        'mult_inverse': 0
    }

    m_value = 10 ** 100
    key_dict['m_value'] = m_value

    # print(f'm value: {m_value}')
    with open(lock_file_name, 'r') as lock_fileIO:
        # use these values to hash out the message letters
        lock_file_line_list = lock_fileIO.readlines()
        # print(f'lock_file_line_list: {lock_file_line_list}')
        rand_index_list = [i for i in range(len(lock_file_line_list))]
        # print(f'init_index_list: {rand_index_list}')
        random.shuffle(rand_index_list)
        # WRITE shuffled index list to the KEY FILE
        # print(f'shuffled_indices: {rand_index_list}')
        key_dict['lock_file_seq_key'] = rand_index_list

    # generate random hash value
    rand_y_value_str = ''
    for _ in range(9):
        rand_y_value_str += str(random.choice(range(0, 10)))
    rand_y_value_str += '9'
    rand_y_value = int(rand_y_value_str)
    # print(f'hash y-val: {rand_y_value}')
    # get multiplicative inverse of rand_y_value
    mult_inverse = modinv(rand_y_value, m_value)
    # WRITE this number to the KEY FILE
    key_dict['mult_inverse'] = mult_inverse
    # print(f'mult_inv: {mult_inverse}')

    encrypt_message = ''
    for char in message:
        # start with the ascii value of a character in the plain text message
        ascii_value = ord(char)
        # loop through lock file hash values
        for hash_val_str in lock_file_line_list:
            # strip \n from lock file num
            hash_val_str_strip = hash_val_str.strip()
            # change the lock file num to a string
            hash_val_str_strip_int = int(hash_val_str_strip)
            # run a cumulative XOR operation
            ascii_value ^= hash_val_str_strip_int
        # modulo hash ascii value
        locked_ascii_value = ascii_value * rand_y_value % m_value
        # print(locked_ascii_value)
        encrypt_message = encrypt_message + str(locked_ascii_value) + ' '
        # strip the space character from the end of the encrypt_message string
    encrypt_message_clean = encrypt_message[:-1]

    # break clean encrypted string into a list of encrypted character ints
    split_encrypt_clean = encrypt_message_clean.split(' ')
    # put the encrypted character ints back into a string - also chnage the ints to hex digits with 0x hex notation
    # prefix
    clean_string = ' '.join([hex(int(i)) for i in split_encrypt_clean])
    print(f'\nEncrypted Message:\n{clean_string}\n')

    # overwrite lock file with scrambled and hashed values -> *IF LOCK FILE HAS MORE THAN 1 VALUE*
    # to determine how many values (lines) the lock file has, check the length of the rand_index_list
    # NOTE: 'random_index_list' is a list of randomized index numbers based on the list made from the lock file values
    # for example, if the lock file values make up a list of four elements, the randomized index list might look
    # something like this: [4, 1, 3, 2]
    hashed_scrambled_lock_list = []
    with open(lock_file_name, 'w') as lock_fileIO:
        # loop through every number
        for pt in range(len(rand_index_list)):
            # get random index element
            rand_index_element = rand_index_list[pt]
            strip_line_list_item = lock_file_line_list[rand_index_element].strip()
            # test = int(strip_line_list_item)
            hashed_value = (int(strip_line_list_item) * rand_y_value) % m_value
            # test_unhash = (hashed_value * mult_inverse) % m_value
            hashed_scrambled_lock_list.append(hashed_value)
            # if the pt pointer variable is pointing to the last element in the list, write the line to the lock
            # file without a '\n' at the end. Otherwise, use a print to file statement to print a line with a trailing
            # '\n'
            if pt == (len(rand_index_list) - 1):
                lock_fileIO.write(f'{hashed_value}')
            else:
                print(f'{hashed_value}', file=lock_fileIO)
    # print(f'hashed_scrambled_lock_list: {hashed_scrambled_lock_list}')

    # generate random key file name: XXXXXXXX_key.txt (X = random letter char)
    files_in_dir = os.listdir()
    # this loop will run until a UNIQUE key file name is generated (VERY unlikely that a duplicate key file name
    # is generated)
    while True:
        random_key_file_name = '_key.txt'
        for _ in range(8):
            random_letter = random.choice(string.ascii_letters)
            random_key_file_name = random_letter + random_key_file_name
        # check to see if the randomly generated key file name already exists
        if random_key_file_name not in files_in_dir:
            break
    # WRITE key data to XXXXXXXX_key.txt file
    with open(random_key_file_name, 'w') as key_fileIO:
        key_dict_string = json.dumps(key_dict, indent=4)
        key_fileIO.write(f'{key_dict_string}')

    encrypt_message_dict = {
        'encrypted_message': clean_string,
        'key_file': random_key_file_name,
    }

    # generate encrypted msg file name: XXXX_encrypted_msg.txt (X = random letter char)
    files_in_dir = os.listdir()
    while True:
        random_encrypt_file_name = '_encrypted_msg.txt'
        for _ in range(4):
            random_letter = random.choice(string.ascii_letters)
            random_encrypt_file_name = random_letter + random_encrypt_file_name
        if random_encrypt_file_name not in files_in_dir:
            break

    # WRITE encrypted msg to XXXX_encrypted_msg.txt file
    with open(random_encrypt_file_name, 'w') as encrypt_message_fileIO:
        encrypt_message_dict_string = json.dumps(encrypt_message_dict, indent=4)
        encrypt_message_fileIO.write(f'{encrypt_message_dict_string}')

    return random_encrypt_file_name
