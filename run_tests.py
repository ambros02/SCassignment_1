import os
import sys
import time
import file_manager



def setup(location):
    """use setup to create needed files with name and optional content"""

    # dictionary with filename as key and content as value
    # files to be read in the tests
    f_read = {
        "read_test_file": "content_for_test_file",
        "read_empty_test_file": ""
    }
    # files to be written to in the tests
    f_write = {
        "write_test_file": "old_content_for_write_test_file",
        "write_empty_content_test_file": "",
        "write_special_char_test_file": "$£!?%&ç*"
    }
    # files to delete during the test
    f_delete = {
        "delete_existing_test_file": "content_to_delete",
        "delete_empty_test_file": ""
    }

    # create all the files
    file_types = [f_read, f_write, f_delete]
    for files in file_types:
        for name, content in files.items():
            file_path = os.path.join(location, name)
            with open(file_path, 'w') as test_file:
                test_file.write(content)

    return None


"""test functions for read_file"""


def test_read_file():
    assert file_manager.read_file("read_test_file") == "content_for_test_file", "the program failed to read a file with some content"


def test_read_empty_file():
    assert file_manager.read_file("read_empty_test_file") == "", "the program failed to read a empty file correctly"


def test_read_none_existent_file():
    assert file_manager.read_file("read_none_existent_test_file") is None, "the program failed to return None if the file does not exist"


"""test functions for create_file"""


def test_create_empty_file():
    # Test creating an empty file
    assert file_manager.create_file("create_empty_file") is True, "the program failed to return True after creating the file"  # Creating an empty file should return True
    # Check if the file is empty
    assert file_manager.read_file("create_empty_file") == "", "the program did not create the file with the right contents"


def test_create_existing_file():
    # Test creating a file with a name that already exists
    file_manager.create_file("existing_file", "initial_content")
    assert file_manager.create_file("existing_file", "new_content") is True , "the program failed to return True after creating the file" # Creating a file with an existing name should return True
    # Check if the file was overwritten with the new content
    assert file_manager.read_file("existing_file") == "new_content", "the program did not create the file with the right contents"


"""test functions for write_file"""


def test_write_file():
    # Write in existing test file
    file_manager.write_file("write_test_file", "new_content_for_write_test_file")
    assert file_manager.read_file("write_test_file") == "new_content_for_write_test_file", "the program failed to write the correct content to the existing file"


def test_write_empty_content():
    # Test writing empty content to an existing file
    file_manager.write_file("write_empty_content_test_file", "")
    assert file_manager.read_file("write_empty_content_test_file") == "", "the program failed to write empty content to an existing file"


def test_write_non_existing_file():
    # Test writing to a non-existing file
    assert file_manager.write_file("non_existing_file", "content_to_be_written") is True, "the program failed to create a new file and write the content (the file specified did not yet exist)"  # Writing to a non-existing file should create the file and return True


def test_write_special_char():
    # Test writing content with special characters to a file
    file_manager.write_file("write_special_char_test_file", "Special characters: $£?!*ç%&")
    assert file_manager.read_file("write_special_char_test_file") == "Special characters: $£?!*ç%&", "the programm failed to write special characters"


"""test functions for delete_file"""


def test_delete_existing_file():
    assert file_manager.delete_file("delete_existing_test_file") is True, "the program failed to delete the file"  # Deleting an existing file should return True
    assert file_manager.read_file("delete_existing_test_file") is None, "the 'deleted' file does still exist"


def test_delete_non_existing_file():
    assert file_manager.delete_file("non_existing_test_file") is False, "the program failed return false when the file does not exist"  # Deleting a non-existing file should return False


def test_delete_empty_file():
    assert file_manager.delete_file("delete_empty_test_file") is True, "the program failed to delete the file"  # Deleting an empty file should return True
    assert file_manager.read_file("delete_empty_test_file") is None, "the 'deleted' file does still exist"


def tests(pattern):
    total_start_time = time.time()
    res = {"total": 0, "pass": 0, "fail": 0, "error": 0}

    for(name, test) in globals().items():
        if name.startswith("test_") and (pattern == None or pattern in test.__name__):
            test_start_time = time.time()
            try:
                test()
                res["pass"] += 1
                test_end_time = time.time()
                test_time = test_end_time-test_start_time
                print(f"\033[0;32m")
                print(f"[{res['total']+1}]".center(80,"="))
                print(f"Test: {name}:\n\t [+] Status: Pass\n\t [+] Time: {test_time:.8f}s")
            except AssertionError as err_msg:
                res["fail"] += 1
                test_end_time = time.time()
                test_time = test_end_time-test_start_time
                print(f"\033[0;33m")
                print(f"[{res['total']+1}]".center(80,"="))
                print(f"Test: {name}:\n\t [-] Status Fail\n\t [-] Time: {test_time:.8f}s")
                print(f"\t Info: {err_msg}")
            except Exception:
                res["error"] += 1
                test_end_time = time.time()
                test_time = test_end_time-test_start_time
                print(f"\033[0;31m")
                print(f"[{res['total']+1}]".center(80,"="))
                print(f"Test: {name}:\n\t [*] Status: Error\n\t [*] Time: {test_time:.8f}s")
            finally:
                res["total"] += 1
                print(f"\033[0;0m")
        else:
            continue

    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    print(f"[total]".center(80,"="))
    print(f"\t[!]Total Tests: {res['total']}\n\t\033[0;32m[!] Passed: {res['pass']}\n\t\033[0;33m[!] Failed: {res['fail']}\n\t\033[0;31m[!] Errors: {res['error']}\n\t\033[0m[!] Time: {total_time:.8f}s")


def teardown(location, existing_start):
    """remove all files that were generated in the testing: more precisely all the files which were not in this folder in the beginning"""
    
    #list with files created during the run
    created = ["create_empty_file","existing_file","write_test_file","write_empty_content_test_file","non_existing_file","write_special_char_test_file"]
    # files which exist after the program has been run
    files_end = os.listdir(location)

    # deleting of the files if they were not part of the original program
    for file in files_end:
        if file not in existing_start:
            file_path = os.path.join(location, file)
            os.remove(file_path)
    #deleting of the files created by file_manager.py during the running of the tesets
    for file in created:
        try:
            os.remove(file)
        except:
            continue   

    return None


def main():
    """main function for the flow control of the program"""
    print("hello world")
    # get a stamp of which files exists before execution, so we can delete the ones that were generated in the test
    files_location = os.path.dirname(os.path.abspath(__file__))
    files_start = os.listdir(files_location)

    setup(files_location)

    pattern = None
    if len(sys.argv) > 1 and sys.argv[1] == "--select":
        pattern = sys.argv[2]
    tests(pattern)

    teardown(files_location, files_start)

    return None


if __name__ == "__main__":
    """run the main function if this is the main file"""
    main()
