import sys
import util_funcs
import os
import json


def main():
    # get command line arguments
    arg_list = sys.argv[:]

    if len(arg_list) == 1:
        print('\n\tWelcome to JLOCK!\n'
              '\tby J. Matta\n'
              '\t(c) November 2022\n'
              '\n\tType \'jlock.py -h\' or \'jlock.py -help\' for a list of available commands.\n')

    elif len(arg_list) == 2:
        command = arg_list[1]
        if command == '-help' or command == '-h':
            separation_str = '=' * 50
            print(f'\n\t{separation_str}\n')
            print('\t\t', 'JLOCK Help')
            print('\t\t', '(c)2022 J. Matta ')
            print(f'\n\t{separation_str}\n')
            print('\t-lock'
                  '\n\n\t\tuse this command to lock/encrypt a message\n'
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
                  '\n\n\t\tuse this command to unlock/decrypt a message\n'
                  '\n\t\tsyntax: jlock.py -unlock <encrypted_message_filename (with file extension)>\n'
                  '\n\t\t\t(encrypted message file must be in the same folder as jlock.py)\n'
                  '\n\t\texample: jlock.py -unlock uRtq_encrypted_msg.txt\n'
                  '\n\t\t\tA decrypted message file will be generated in the current working directory.\n'
                  '\t\t\tThe decrypted message will also be printed to the terminal along with the\n'
                  '\t\t\tgenerated decrypted message filename.\n')
            print(f'\n\t{separation_str}\n')
            print('\t-msg'
                  '\n\n\t\tuse this command to print a list of PLAINTEXT message files in the current directory\n'
                  '\n\t\tThese files contain messages that have been decoded. The files\' contents consist of only\n'
                  '\t\tthe decoded message.\n'
                  '\n\t\tSample output:\n\n'
                  '\t\t\tfziW_decrypted_msg.txt -> BobIsHere!\n'
                  '\t\t\tkvnE_decrypted_msg.txt -> ThisMessageHasBeenDecoded\n'
                  '\t\t\ttHhw_decrypted_msg.txt -> Password123abc\n')
            print(f'\n\t{separation_str}\n')
            print('\t-locked'
                  '\n\n\t\tuse this command to print a list of ENCRYPTED message files in the current directory.\n'
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

        elif arg_list[1] == '-msg':
            # displays list of decrypted plain text message files
            file_list = os.listdir()
            if len(file_list) == 0:
                print('\t\nNo plaintext message files available.\n')
            else:
                print('\t\nPlaintext message files:\n')
                for file_name in file_list:
                    if file_name[-18:] == '_decrypted_msg.txt':
                        print(f'\t{file_name}', end='')
                        with open(file_name, 'r') as msg_fileIO:
                            print(f' -> {msg_fileIO.readline()}')

        elif arg_list[1] == '-locked':
            # displays list of encrypted (locked) files
            file_list = os.listdir()
            if len(file_list) == 0:
                print('\t\nNo encrypted message files available.\n')
            else:
                print('\t\nEncrypted message files:\n')
                for file_name in file_list:
                    if file_name[-18:] == '_encrypted_msg.txt':
                        print(f'\t{file_name}')
                        with open(file_name, 'r') as encrypt_msg_fileIO:
                            json_obj = json.loads(encrypt_msg_fileIO.read())
                            print(f'\t\t{json_obj["encrypted_message"]}')

        else:
            print('Error: invalid command')

    elif len(arg_list) == 3:
        if arg_list[1] == '-unlock':
            target_encrypted_file = arg_list[2]
            file_list = os.listdir()
            if target_encrypted_file in file_list:
                util_funcs.unlock(target_encrypted_file)
            else:
                print(f'{target_encrypted_file} does not exist')
        else:
            print('Error: invalid command')

    elif len(arg_list) == 4:
        if arg_list[1] == '-lock':
            try:
                lock_depth = int(arg_list[2])
            except ValueError:
                print(f'Invalid lock depth: \'{arg_list[2]}\'. Must be an integer greater than 0 (zero).')
                return
            if lock_depth <= 0:
                print(f'Invalid lock depth: \'{arg_list[2]}\'. Must be an integer greater than 0 (zero).')
                return
            lock_file = util_funcs.generate_lock_file(arg_list[2])
            util_funcs.lock(arg_list[3], lock_file)
        else:
            print('Error: invalid command')

    else:
        print('Error: invalid command')

    # elif a[1] == '-lock':
    #     lock_depth = int(sys.argv[2])
    #     lock_file = util_funcs.generate_lock_file(lock_depth)
    #     message = sys.argv[3]
    #     util_funcs.lock(message, lock_file)
    # elif a[1] == '-unlock':
    #     encrypted_msg_file = a[2]
    #     util_funcs.unlock(encrypted_msg_file)
    # elif a[1] == '-keys':
    #     # displays list of key files
    #     if a[2] == '-v': # verbose option
    #         pass
    # elif a[1] == '-locks':
    #     # displays list of lock files
    #     pass
    # else:
    #     error_message = 'Error: invalid command and/or flag.'
    #     print(f'\n\t{error_message}\n')

    # elif a[0] == '-r':
    #     pass
    # print report all info (options - print)

    # generate lock key files


if __name__ == '__main__':
    main()
