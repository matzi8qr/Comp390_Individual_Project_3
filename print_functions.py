"""
print_functions.py contains the long multiline strings printed to terminal for user convenience and understanding.
"""

import json


def print_welcome():
    """
    Prints the welcome message
    :return: None
    """
    print('\n\tWelcome to JLOCK!\n'
          '\tby J. Matta\n'
          '\t(c) November 2022\n'
          '\n\tType \'jlock.py -h\' or \'jlock.py -help\' for a list of available commands.\n')


def print_help():
    """
    Prints the help command to terminal
    :return: None
    """
    separation_str = '=' * 50
    print(f'\n\t{separation_str}\n')
    print('\t\t', 'JLOCK Help')
    print('\t\t', '(c)2022 J. Matta ')
    print(f'\n\t{separation_str}\n')
    print_lock_help()
    print(f'\n\t{separation_str}\n')
    print_unlock_help()
    print(f'\n\t{separation_str}\n')
    print('\t-msg'
          '\n\n\t\tUse this command to print a list of PLAINTEXT message files in the current directory.\n'
          '\n\t\tThese files contain messages that have been decoded. The files\' contents consist of only\n'
          '\t\tthe decoded message.\n'
          '\n\t\tSample output:\n\n'
          '\t\t\tfziW_decrypted_msg.txt -> BobIsHere!\n'
          '\t\t\tkvnE_decrypted_msg.txt -> ThisMessageHasBeenDecoded\n'
          '\t\t\ttHhw_decrypted_msg.txt -> Password123abc\n')
    print(f'\n\t{separation_str}\n')
    print('\t-locked'
          '\n\n\t\tUse this command to print a list of ENCRYPTED message files in the current directory.\n'
          '\n\t\tThese files contain encoded (locked) messages. Encoded messaages will be printed below\n'
          '\t\teach file name.\n'
          '\n\t\tSample output:\n'
          '\n\t\t\tEZIQ_encrypted_msg.txt\n'
          '\t\t\t0x11bcea833149d7dc08eb6a73 0x11bcea833149d7db47ad0240 0x11bcea833149d7dcca29d2a6\n'
          '\n\t\t\tIOuI_encrypted_msg.txt\n'
          '\t\t\t0x10002ab80be7bf94b64129ec 0x10002ab80be7bf97c584415b 0x10002ab80be7bf973052e78f '
          '0x10002ab80be7bf985ab59b27\n'
          '\n\t\t\tJZmg_encrypted_msg.txt\n'
          '\t\t\t0x4d9c9771492f4c79ee2d424 0x4d9c9771492f4c84b664555 0x4d9c9771492f4c79ee2d424\n')
    print(f'\n\t{separation_str}\n')
    print('\t-clear'
          '\n\n\t\tUse this command to delete all \'lock\', \'key\', \'encrypted message\', and'
          '\n\t\t\'decrypted message\' text files the current directory.\n'
          '\n\t\tThis will reset the \'jlock\' directory and clear all resulting text files from previous\n'
          '\t\t-lock and -unlock commands.\n'
          '\n\t\tA confirmation message will be printed to the terminal.\n')
    print(f'\n\t{separation_str}\n')


def print_unlock_help():
    """
    Prints the usage of the -unlock command to terminal
    :return: None
    """
    print('\t-unlock'
          '\n\n\t\tUse this command to unlock/decrypt a message.\n'
          '\n\t\tsyntax: jlock.py -unlock <encrypted_message_filename (with file extension)>\n'
          '\n\t\t\t(encrypted message file must be in the same folder as jlock.py)\n'
          '\n\t\texample: jlock.py -unlock uRtq_encrypted_msg.txt\n'
          '\n\t\t\tA decrypted message file will be generated in the current working directory.\n'
          '\t\t\tThe decrypted message will also be printed to the terminal along with the\n'
          '\t\t\tgenerated decrypted message filename.\n')


def print_lock_help():
    """
    Prints the usage of the -lock command to terminal
    :return: None
    """
    print('\t-lock'
          '\n\n\t\tUse this command to lock/encrypt a message.\n'
          '\n\t\tsyntax: jlock.py -lock <lock depth (int > 0)> <message (no spaces)>\n'
          '\n\t\t\t(Lock depth sets the complexity of the Lock. Higher numbers make the\n'
          '\t\t\tlock more robust. Note: larger locks require more processing time to\n'
          '\t\t\tencrypt/decrypt messages.)\n'
          '\n\t\texample: jlock.py -lock 20 ThisIsASecretMessage\n'
          '\n\t\t\tA \'XXXX_encrypted_msg.txt\' file will be generated in the current folder.\n'
          '\t\t\t\'X\' represents a random ascii letter character.\n'
          '\t\t\tThe encrypted message will also be printed to the terminal along with the\n'
          '\t\t\tgenerated encrypted message filename.\n')


def extract_msg_file_content(filename):
    """
    Extracts the contents of a file into a string format
    :param filename: Name of the file to extract from
    :return: None
    """
    with open(filename, 'r') as msg_fileIO:
        print(f' -> {msg_fileIO.readline()}')


def print_msg_file_info(filename):
    """
    Prints the content of a file to the terminal
    :param filename: Name of the file to print the contents of
    :return: None
    """
    print(f'\t{filename}', end='')
    try:
        extract_msg_file_content(filename)
    except OSError as file_read_error:
        print(f'There was an error trying to read the file: {filename}: {file_read_error}')


def extract_locked_file_content(filename):
    """
    Extracts the contents of an encrypted file into a string format
    :param filename: Name of the file to extract from
    :return: None
    """
    with open(filename, 'r') as encrypt_msg_fileIO:
        json_obj = json.loads(encrypt_msg_fileIO.read())
        print(f'\t\t{json_obj["encrypted_message"]}\n')


def print_locked_file_info(filename: str):
    """
    Prints the content of an encrypted file to the terminal
    :param filename: Name of the file to print the contents of
    :return: None
    """
    print(f'\t{filename}')
    try:
        extract_locked_file_content(filename)
    except OSError as file_read_error:
        print(f'There was an error trying to read the file: {filename}: {file_read_error}')
