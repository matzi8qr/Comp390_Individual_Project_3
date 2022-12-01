"""
command_functions.py contains all the commands callable from jlock and handles them here.
"""

import os
import util_funcs
import print_functions
import lock_functions
import unlock_functions


def msg():
    """
    Displays list of decrypted, plain text message files.
    :return: None
    """
    decrypted_file_list = [file for file in os.listdir() if file.endswith('_decrypted_msg.txt')]
    if len(decrypted_file_list) == 0:
        print('\n\tNo plaintext message files available.\n')
        return
    print('\n\tPlaintext message files:\n')
    for file_name in decrypted_file_list:
        print_functions.extract_msg_file_content(file_name)


def locked():
    """
    Displays list of encrypted files
    :return: None
    """
    encrypted_file_list = [file for file in os.listdir() if file.endswith('_encrypted_msg.txt')]
    if len(encrypted_file_list) == 0:
        print('\n\tNo encrypted message files available.\n')
        return
    print('\n\tEncrypted message files:\n')
    for file_name in encrypted_file_list:
        print_functions.extract_locked_file_content(file_name)


def clear():
    """
    Gathers and deletes all locks, keys, encrypted_msgs, and decrypted_msgs.
    :return: None
    """
    # gather all text files from current directory (use list comprehension)
    lock_file_list = [file for file in os.listdir() if file.endswith('_lock.txt')]
    key_file_list = [file for file in os.listdir() if file.endswith('_key.txt')]
    encrypted_file_list = [file for file in os.listdir() if file.endswith('_encrypted_msg.txt')]
    decrypted_file_list = [file for file in os.listdir() if file.endswith('_decrypted_msg.txt')]

    # assemble ALL text file list
    master_text_file_list = lock_file_list + key_file_list + encrypted_file_list + decrypted_file_list
    for text_file in master_text_file_list:
        os.remove(text_file)

    print('\n\n\tAll \'lock\', \'key\', \'encrypted message\', and \'decrypted message\' text files removed.\n')


def unlock(target_encrypted_file):
    """
    Unlocks an encrypted file, then deletes the encryption, lock, and key.
    :param target_encrypted_file: name of the file you wish to decrypt
    :return: None
    """
    file_list = os.listdir()
    if (target_encrypted_file in file_list) and (len(target_encrypted_file) == 22) and \
            (target_encrypted_file[4:] == '_encrypted_msg.txt'):
        unlock_functions.unlock(target_encrypted_file)
    else:
        print(f'\n\t{target_encrypted_file} does not exist or is invalid\n')


def lock(args: list):
    """
    Locks a file, generating an encryption, lock, and key.
    :param args: A list containing first, an int > 0  lock depth, and second, the message to be encrypted.
    :return: None
    """
    # check if an int is passed as the lock depth
    try:
        util_funcs.validate_lock_depth(args)
    except IndexError or ValueError:
        return

    lock_file = util_funcs.generate_lock_file(args[0])
    try:
        lock_functions.lock(args[1], lock_file)
    except IndexError:
        print_functions.print_lock_help()
