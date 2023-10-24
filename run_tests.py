import file_manager
import os
import random
import sys
import time



def setup(location):
    """use setup to create needed files with name and optional content"""

    # dictionary with filename as key and content as value, one for each type of testing excluding create tests
    read_files = {
        "read_test_file": "content_for_test_file",
        "read_empty_test_file": ""
    }
    write_files = {
        "write_test_file": "old_content_for_write_test_file",
        "write_empty_content_test_file": "",
        "write_special_char_test_file": "$£!?%&ç*"
    }
    delete_files = {
        "delete_existing_test_file": "content_to_delete",
        "delete_empty_test_file": ""
    }

    # create all the files used by the tests
    file_types = [read_files, write_files, delete_files]
    for files in file_types:
        for name, content in files.items():
            file_path = os.path.join(location, name)
            with open(file_path, 'w') as test_file:
                test_file.write(content)

    return None


"""test functions for read_file"""


def test_read_file(path_t):
    assert file_manager.read_file(path_t) == "content_for_test_file"


def test_read_empty_file(path_t):
    assert file_manager.read_file(path_t) == ""


def test_read_none_existent_file(path_t):
    assert file_manager.read_file(path_t) is None, "the program failed to return None if the file does not exist"


"""test functions for create_file"""


def test_create_empty_file(path_t):
    # Test creating an empty file
    assert file_manager.create_file(path_t) is True, "the program failed to return True after creating the file"  # Creating an empty file should return True
    # Check if the file is empty
    assert file_manager.read_file(path_t) == "", "the content of the file is not empty"


def test_create_existing_file(path_t):
    # Test creating a file with a name that already exists
    file_manager.create_file(path_t, "initial_content")
    assert file_manager.create_file(path_t, "new_content") is True , "the program failed to return True after creating the file" # Creating a file with an existing name should return True
    # Check if the file was overwritten with the new content
    assert file_manager.read_file(path_t) == "new_content", "the content of the file does not match"
    
def test_create_false_file(path_t):
    #test if the create file function can handle wrong filenames
    assert file_manager.create_file("\\33/kdwa") is False, "the program failed to return False after receiving an invalid file name"

"""test functions for write_file"""



def test_write_file(path_t):
    # Write in existing test file
    file_manager.write_file(path_t, "new_content_for_write_test_file")
    assert file_manager.read_file(path_t) == "new_content_for_write_test_file"


def test_write_empty_content(path_t):
    # Test writing empty content to an existing file
    file_manager.write_file(path_t, "")
    assert file_manager.read_file(path_t) == ""


def test_write_non_existing_file(path_t):
    # Test writing to a non-existing file
    assert file_manager.write_file(path_t, "content_to_be_written") is True  # Writing to a non-existing file should create the file and return True


def test_write_special_char(path_t):
    # Test writing content with special characters to a file
    file_manager.write_file(path_t, "Special characters: $£?!*ç%&")
    assert file_manager.read_file(path_t) == "Special characters: $£?!*ç%&"

def test_write_false_file(path_t):
    #test if the function returns False for an invalid filename
    assert file_manager.write_file("\\33/kdwa","some content") is False, "the progran failed to return False after receiving an invalid file name"

"""test functions for delete_file"""


def test_delete_existing_file(path_t):
    assert file_manager.delete_file(path_t) is True, "file manager did not return True"  # Deleting an existing file should return True
    assert file_manager.read_file(path_t) is None, "the 'deleted' file does still exist"


def test_delete_non_existing_file(path_t):
    assert file_manager.delete_file(path_t) is False, "the program failed return False when the file does not exist"  # Deleting a non-existing file should return False


def test_delete_empty_file(path_t):
    assert file_manager.delete_file(path_t) is True, "file manager did not return True"  # Deleting an empty file should return True
    assert file_manager.read_file(path_t) is None, "the 'deleted' file does still exist"


def tests(pattern, path_parent):
    total_start_time = time.time()
    res = {"total": 0, "pass": 0, "fail": 0, "error": 0}

    #dictionary with function names as keys and file names which are used in test as value
    file_names={"test_read_file":"read_test_file",
                "test_read_empty_file":"read_empty_test_file",
                "test_read_none_existent_file":"read_none_existent_test_file",
                "test_create_empty_file":"create_empty_file",
                "test_create_existing_file":"existing_file",
                "test_write_file":"write_test_file",
                "test_write_empty_content":"write_empty_content_test_file",
                "test_write_non_existing_file":"non_existing_file",
                "test_write_special_char":"write_special_char_test_file",
                "test_delete_existing_file":"delete_existing_test_file",
                "test_delete_non_existing_file":"non_existing_test_file",
                "test_delete_empty_file":"delete_empty_test_file"
                }

    #names of the tests and functions in a list to randomize the order
    names_functions = []

    for(name, test) in globals().items():
        if name.startswith("test_") and (pattern == None or pattern in test.__name__):
            names_functions.append((name,test))
    random.shuffle(names_functions)
    for t_name,t_function in names_functions:
            #get the absolute path for the file
            try:
                file_name = file_names[t_name]
            except:
                file_name = "foo"
            path_test = os.path.join(path_parent,file_name)

            test_start_time = time.time()
            try:
                t_function(path_test)
                res["pass"] += 1
                test_end_time = time.time()
                test_time = test_end_time-test_start_time
                print(f"\033[0;32m")
                print(f"[{res['total']+1}]".center(80,"="))
                print(f"Test: {t_name}:\n\t [+] Status: Pass\n\t [+] Time: {test_time:.8f}s")
            except AssertionError as err_msg:
                res["fail"] += 1
                test_end_time = time.time()
                test_time = test_end_time-test_start_time
                print(f"\033[0;33m")
                print(f"[{res['total']+1}]".center(80,"="))
                print(f"Test: {t_name}:\n\t [-] Status Fail\n\t [-] Time: {test_time:.8f}s")
                print(f"\t Info: {err_msg}")
            except Exception:
                res["error"] += 1
                test_end_time = time.time()
                test_time = test_end_time-test_start_time
                print(f"\033[0;31m")
                print(f"[{res['total']+1}]".center(80,"="))
                print(f"Test: {t_name}:\n\t [*] Status: Error\n\t [*] Time: {test_time:.8f}s")
            finally:
                res["total"] += 1
                print(f"\033[0;0m")


    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    print(f"[total]".center(80,"="))
    print(f"\t[!]Total Tests: {res['total']}\n\t\033[0;32m[!] Passed: {res['pass']}\n\t\033[0;33m[!] Failed: {res['fail']}\n\t\033[0;31m[!] Errors: {res['error']}\n\t\033[0m[!] Time: {total_time:.8f}s")



def teardown(location, existing_start):
    """remove all files that were generated in the testing: more precisely all the files which were not in this folder in the beginning"""
    
    # files which exist after the program has been run
    files_end = os.listdir(location)

    # deleting of the files if they were not part of the original program
    for file in files_end:
        if file not in existing_start:
            file_path = os.path.join(location, file)
            os.remove(file_path)

    return None


def main():
    """main function for the flow control of the program"""

    # get a stamp of which files exists before execution, so the ones that were generated in the test can be deleted
    files_location = os.path.dirname(os.path.abspath(__file__))
    files_start = os.listdir(files_location)

    setup(files_location)

    pattern = None
    if len(sys.argv) > 1 and sys.argv[1] == "--select":
        pattern = sys.argv[2]
    tests(pattern, files_location)

    teardown(files_location, files_start)
    return None


if __name__ == "__main__":
    """run the main function if this is the main file"""
    main()
