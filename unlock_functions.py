import json
import random
import string
import os


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
        dehashed_char = int(encrypt_char[2:], 16) * mult_inverse % m_val
        for lock_val in reassembled_lock_list:
            dehashed_char ^= lock_val
        decrypted_msg = decrypted_msg + chr(dehashed_char)
    print(f'\nDecrypted Message: {decrypted_msg}\n')

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
