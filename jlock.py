import sys
import util_funcs
import os
import json
from lock_functions import lock
from unlock_functions import unlock


def jlock_main():
    # get command line arguments
    arg_list = sys.argv
    arg_list_len = len(arg_list)

    if arg_list_len == 1:
        print('\n\tWelcome to JLOCK!\n'
              '\tby J. Matta\n'
              '\t(c) November 2022\n'
              '\n\tType \'jlock.py -h\' or \'jlock.py -help\' for a list of available commands.\n')

    elif arg_list_len == 2:
        command = arg_list[1]
        if command == '-help' or command == '-h':
            separation_str = '=' * 50
            print(f'\n\t{separation_str}\n')
            print('\t\t', 'JLOCK Help')
            print('\t\t', '(c)2022 J. Matta ')
            print(f'\n\t{separation_str}\n')
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
            print(f'\n\t{separation_str}\n')
            print('\t-unlock'
                  '\n\n\t\tUse this command to unlock/decrypt a message.\n'
                  '\n\t\tsyntax: jlock.py -unlock <encrypted_message_filename (with file extension)>\n'
                  '\n\t\t\t(encrypted message file must be in the same folder as jlock.py)\n'
                  '\n\t\texample: jlock.py -unlock uRtq_encrypted_msg.txt\n'
                  '\n\t\t\tA decrypted message file will be generated in the current working directory.\n'
                  '\t\t\tThe decrypted message will also be printed to the terminal along with the\n'
                  '\t\t\tgenerated decrypted message filename.\n')
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

        elif command == '-msg':
            # displays list of decrypted plain text message files
            decrypted_file_list = [file for file in os.listdir() if file.endswith('_decrypted_msg.txt')]
            if len(decrypted_file_list) == 0:
                print('\n\tNo plaintext message files available.\n')
            else:
                print('\n\tPlaintext message files:\n')
                for file_name in decrypted_file_list:
                    print(f'\t{file_name}', end='')
                    with open(file_name, 'r') as msg_fileIO:
                        print(f' -> {msg_fileIO.readline()}')

        elif command == '-locked':
            # displays list of encrypted (locked) files
            encrypted_file_list = [file for file in os.listdir() if file.endswith('_encrypted_msg.txt')]
            if len(encrypted_file_list) == 0:
                print('\n\tNo encrypted message files available.\n')
            else:
                print('\n\tEncrypted message files:\n')
                for file_name in encrypted_file_list:
                    print(f'\t{file_name}')
                    with open(file_name, 'r') as encrypt_msg_fileIO:
                        json_obj = json.loads(encrypt_msg_fileIO.read())
                        print(f'\t\t{json_obj["encrypted_message"]}\n')

        elif command == '-clear':
            # gather all text files from current directory (use list comprehension)
            lock_file_list = [file for file in os.listdir() if file.endswith('_lock.txt')]
            key_file_list = [file for file in os.listdir() if file.endswith('_key.txt')]
            encrypted_file_list = [file for file in os.listdir() if file.endswith('_encrypted_msg.txt')]
            decrypted_file_list = [file for file in os.listdir() if file.endswith('_decrypted_msg.txt')]

            # assemble ALL text file list
            master_text_file_list = lock_file_list + key_file_list + encrypted_file_list + decrypted_file_list
            # print(master_text_file_list)
            for text_file in master_text_file_list:
                os.remove(text_file)

            print('\n\n\tAll \'lock\', \'key\', \'encrypted message\', and \'decrypted message\' text files removed.\n')

        else:
            print('Error: invalid command')

    elif arg_list_len == 3:
        if arg_list[1] == '-unlock':
            target_encrypted_file = arg_list[2]
            file_list = os.listdir()
            if target_encrypted_file in file_list:
                unlock(target_encrypted_file)
            else:
                print(f'\n\t{target_encrypted_file} does not exist\n')
        else:
            print('Error: invalid command')

    elif arg_list_len == 4:
        if arg_list[1] == '-lock':
            # check if an int is passed as the lock depth
            try:
                lock_depth = int(arg_list[2])
            except ValueError:
                print(f'\n\tInvalid lock depth: \'{arg_list[2]}\'. Must be an integer greater than 0 (zero).\n')
                return
            # check if lock depth is greater than zero
            if lock_depth <= 0:
                print(f'\n\tInvalid lock depth: \'{arg_list[2]}\'. Must be an integer greater than 0 (zero).\n')
                return

            lock_file = util_funcs.generate_lock_file(arg_list[2])
            lock(arg_list[3], lock_file)
        else:
            print('Error: invalid command')

    else:
        print('Error: invalid command')


if __name__ == '__main__':
    jlock_main()

    # test function calls

    # a lock depth of 10,000,000 seems to be the reasonable limit for processing time

    # lock_file = generate_lock_file(10)
    # encrypt_msg_file = lock('Bob_is_cool', lock_file)
    # unlock(encrypt_msg_file)
    #
    # lock_file = generate_lock_file(20)
    # encrypt_msg_file1 = lock('Decoded_Message', lock_file)
    # unlock(encrypt_msg_file1)
    #
    # lock_file = generate_lock_file(20)
    # encrypt_msg_file2 = lock('Password123abc', lock_file)
    # unlock(encrypt_msg_file2)
