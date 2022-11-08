import json
import random
import string
import sys
import os


# https://rosettacode.org/wiki/Modular_inverse#Python
def extended_gcd(aa, bb):
    lastremainder, remainder = abs(aa), abs(bb)
    x, lastx, y, lasty = 0, 1, 1, 0
    while remainder:
        lastremainder, (quotient, remainder) = remainder, divmod(lastremainder, remainder)
        x, lastx = lastx - quotient * x, x
        y, lasty = lasty - quotient * y, y
    return lastremainder, lastx * (-1 if aa < 0 else 1), lasty * (-1 if bb < 0 else 1)


# https://rosettacode.org/wiki/Modular_inverse#Python
def modinv(a, m):
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError
    return x % m


def lock(message, lock_file_name):

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
        line_list = lock_fileIO.readlines()
        # print(f'lock_file_line_list: {line_list}')
        rand_index_list = [i for i in range(len(line_list))]
        # print(f'init_index_list: {rand_index_list}')
        random.shuffle(rand_index_list)
        # WRITE shuffled index list to the KEY FILE
        # print(f'shuffled_indices: {rand_index_list}')
        key_dict['lock_file_seq_key'] = rand_index_list

    # generate random hash value
    rand_y_value_str = ''
    for _ in range(8):
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
        for hash_val_str in line_list:
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
    encrypt_message_clean = encrypt_message[:-1]

    split_encrypt_clean = encrypt_message_clean.split(' ')
    clean_string = ' '.join([hex(int(i)) for i in split_encrypt_clean])
    print(f'\nEncrypted Message:\n{clean_string}')

    # overwrite lock file with scrambled and hashed values
    hashed_scrambled_lock_list = []
    with open(lock_file_name, 'w') as lock_fileIO:
        for pt in range(len(rand_index_list) - 1):
            # get random index element
            rand_index_element = rand_index_list[pt]
            strip_line_list_item = line_list[rand_index_element].strip()
            # test = int(strip_line_list_item)
            hashed_value = (int(strip_line_list_item) * rand_y_value) % m_value
            # test_unhash = (hashed_value * mult_inverse) % m_value
            hashed_scrambled_lock_list.append(hashed_value)
            print(f'{hashed_value}', file=lock_fileIO)
        # must do the last line separately to account for striping the \n at the end
        rand_index_element = rand_index_list[pt + 1]
        strip_line_list_item = line_list[rand_index_element].strip()
        hashed_value = int(strip_line_list_item) * rand_y_value % m_value
        hashed_scrambled_lock_list.append(hashed_value)
        lock_fileIO.write(f'{hashed_value}')
    # print(f'hashed_scrambled_lock_list: {hashed_scrambled_lock_list}')

    # generate random key file name: XXXXXXXX_key.txt (X = random letter char)
    files_in_dir = os.listdir()
    while True:
        random_key_file_name = '_key.txt'
        for _ in range(8):
            random_letter = random.choice(string.ascii_letters)
            random_key_file_name = random_letter + random_key_file_name
        if random_key_file_name not in files_in_dir:
            break
    # WRITE key data to XXXXXXXX_key.txt file
    with open(random_key_file_name, 'w') as key_fileIO:
        key_dict_string = json.dumps(key_dict, indent=4)
        key_fileIO.write(f'{key_dict_string}')

    encrypt_message_dict = {
        'encrypted_message': encrypt_message_clean,
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


def unlock(encrypted_msg_file):

    # get json object from file contents
    with open(encrypted_msg_file, 'r') as encrypt_msg_fileIO:
        msg_file_contents = encrypt_msg_fileIO.read()
    # print(msg_file_contents)
    decrypt_msg_dict = json.loads(msg_file_contents)
    # print(decrypt_msg_dict)
    encrypt_msg = decrypt_msg_dict['encrypted_message']
    # print(f'encrypted_msg: {encrypt_msg}')
    split_msg_list = encrypt_msg.split(' ')
    # print(f'split_encrypt_msg: {split_msg_list}')
    key_file_name = decrypt_msg_dict['key_file']
    # print(f'key_file: {key_file_name}')

    with open(key_file_name, 'r') as key_fileIO:
        key_file_contents = key_fileIO.read()
    # print(f'key file contents: {key_file_contents}')
    key_dict = json.loads(key_file_contents)
    # gather key data
    m_val = key_dict['m_value']
    lock_file_0 = key_dict['lock_file']
    lock_file_seq_key = key_dict['lock_file_seq_key']
    mult_inverse = key_dict['mult_inverse']

    # extract the lock number list from the lock file
    lock_file_scrambled_num_list = []
    with open(lock_file_0, 'r') as lock_fileIO:
        for line in lock_fileIO:
            lock_file_scrambled_num_list.append(int(line))
    # print(f'scrambled_lock_contents: {lock_file_scrambled_num_list}')

    # set up a holding list to reassemble the lock numbers
    reassembled_lock_list = [0] * len(lock_file_scrambled_num_list)
    # reassemble lock list based on seq. list from key (not un-hashed yet)
    for pointer in range(len(lock_file_scrambled_num_list)):
        correct_lock_seq_location = lock_file_seq_key[pointer]
        reassembled_lock_list[correct_lock_seq_location] = lock_file_scrambled_num_list[pointer]
    # print(f'reassembled_lock_list: {reassembled_lock_list}')

    # un-hash all lock values
    for i in range(len(reassembled_lock_list)):
        reassembled_lock_list[i] = reassembled_lock_list[i] * mult_inverse % m_val
    # print(f'unhashed_reassembled_lock_list: {reassembled_lock_list}')
    # reverse reassembled lock list to undo hash
    reassembled_lock_list.reverse()
    # print(f'reversed_unhashed_reassembled_lock_list: {reassembled_lock_list}')

    # un-encrypt message by cumulative XOR back through reversed lock list for each encrypted character in the
    # encrypted messages
    decrypted_msg = ''
    for encrypt_char in split_msg_list:
        # dehash char:
        dehashed_char = int(encrypt_char) * mult_inverse % m_val
        for lock_val in reassembled_lock_list:
            dehashed_char ^= lock_val
        decrypted_msg = decrypted_msg + chr(dehashed_char)
    print(f'\nDecrypted Message: {decrypted_msg}')

    # generate random lock file name: [random]_lock.txt
    files_in_dir = os.listdir()
    while True:
        random_file_name = '_decrypted_msg.txt'
        for _ in range(4):
            random_letter = random.choice(string.ascii_letters)
            random_file_name = random_letter + random_file_name
        if random_file_name not in files_in_dir:
            break

    with open(random_file_name, 'w') as decrypted_msg_fileIO:
        decrypted_msg_fileIO.write(decrypted_msg)

    # delete lock, key, encrypted message files
    os.remove(lock_file_0)
    os.remove(key_file_name)
    os.remove(encrypted_msg_file)

    return decrypted_msg


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
        for line_ct in range(size):
            rand_int1 = random.randint(0, sys.maxsize)
            if line_ct < size - 1:
                print(f'{rand_int1}', file=text_file)
                continue
            text_file.write(f'{rand_int1}')

    return random_file_name


# test function calls
# lock_file = generate_lock_file(20)
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
# test ascii conversion

