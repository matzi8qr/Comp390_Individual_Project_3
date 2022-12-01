"""
Test functions to be ran under pytest
"""

import pytest
from testfixtures import TempDirectory
from print_functions import *
from util_funcs import validate_lock_depth


def test_extract_msg_file_content(capfd):
    """
    Tests if extract_msg_file_content accurately extracts.
    :param capfd: Reads print strings
    :return: None
    """
    with TempDirectory() as tempDir:
        temp_filename = 'test.txt'
        tempDir.write(temp_filename, b'Testing 1 2 3')
        file_path = tempDir.path + '\\' + temp_filename
        extract_msg_file_content(file_path)
    assert capfd.readouterr()[0] == ' -> Testing 1 2 3\n'

    with pytest.raises(FileNotFoundError) as exc:
        extract_msg_file_content('DNE.txt')
    assert exc.type is FileNotFoundError


def test_validate_lock_depth():
    """
    Tests if validate_lock_depth successfully validates user input before trying to use it.
    :return: None
    """
    with pytest.raises(Exception) as exc:
        validate_lock_depth([])
        validate_lock_depth(-1)
        validate_lock_depth('Fred')
    assert exc is IndexError or ValueError

    assert validate_lock_depth([1]) is None
