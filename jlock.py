import sys
import print_functions
import command_functions


def jlock_main():
    parse_command()


def parse_command():
    """
    Takes the command line arguments and handles them for intended effects
    :return: None
    """
    arg_list = sys.argv
    try:  # Tries to define str command to the first command line argument, sends welcome message if no args passed.
        command = arg_list[1]
    except IndexError:
        print_functions.print_welcome()
        return

    if command == '-help' or command == '-h':
        print_functions.print_help()
    elif command == '-msg':
        command_functions.msg()
    elif command == '-locked':
        command_functions.locked()
    elif command == '-clear':
        command_functions.clear()
    elif command == '-unlock':
        try:
            command_functions.unlock(arg_list[2])
        except IndexError:
            print_functions.print_unlock_help()
    elif command == '-lock':
        try:
            command_functions.lock(arg_list[2:])
        except IndexError:
            print_functions.print_lock_help()
    else:
        print("Error: invalid command. Type 'jlock.py -h' for options")


if __name__ == '__main__':
    jlock_main()
