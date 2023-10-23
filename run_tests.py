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
    assert file_manager.read_file("read_test_file") == "content_for_test_file"


def test_read_empty_file():
    assert file_manager.read_file("read_empty_test_file") == ""


def test_read_none_existent_file():
    assert file_manager.read_file("read_none_existent_test_file") is None


"""test functions for create_file"""


def test_create_empty_file():
    # Test creating an empty file
    assert file_manager.create_file("create_empty_file") is True  # Creating an empty file should return True
    # Check if the file is empty
    assert file_manager.read_file("create_empty_file") == ""


def test_create_existing_file():
    # Test creating a file with a name that already exists
    file_manager.create_file("existing_file", "initial_content")
    assert file_manager.create_file("existing_file", "new_content") is True  # Creating a file with an existing name should return True
    # Check if the file was overwritten with the new content
    assert file_manager.read_file("existing_file") == "new_content"


"""test functions for write_file"""


def test_write_file():
    # Write in existing test file
    file_manager.write_file("write_test_file", "new_content_for_write_test_file")
    assert file_manager.read_file("write_test_file") == "new_content_for_write_test_file"


def test_write_empty_content():
    # Test writing empty content to an existing file
    file_manager.write_file("write_empty_content_test_file", "")
    assert file_manager.read_file("write_empty_content_test_file") == ""


def test_write_non_existing_file():
    # Test writing to a non-existing file
    assert file_manager.write_file("non_existing_file", "content_to_be_written") is True  # Writing to a non-existing file should create the file and return True


def test_write_special_char():
    # Test writing content with special characters to a file
    file_manager.write_file("write_special_char_test_file", "Special characters: $£?!*ç%&")
    assert file_manager.read_file("write_special_char_test_file") == "Special characters: $£?!*ç%&"


"""test functions for delete_file"""


def test_delete_existing_file():
    assert file_manager.delete_file("delete_existing_test_file") is True  # Deleting an existing file should return True
    assert file_manager.read_file("delete_existing_test_file") is None


def test_delete_non_existing_file():
    assert file_manager.delete_file("non_existing_test_file") is False  # Deleting a non-existing file should return False


def test_delete_empty_file():
    assert file_manager.delete_file("delete_empty_test_file") is True  # Deleting an empty file should return True
    assert file_manager.read_file("delete_empty_test_file") is None


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
                print(f"Test: {name}, Pass, Time: {test_time:.8f}s")
            except AssertionError:
                res["fail"] += 1
                test_end_time = time.time()
                test_time = test_end_time-test_start_time
                print(f"Test: {name}, Fail, Time: {test_time:.8f}s")
            except Exception:
                res["error"] += 1
                test_end_time = time.time()
                test_time = test_end_time-test_start_time
                print(f"Test: {name}, Error, Time: {test_time:.8f}s")
            finally:
                res["total"] += 1
        else:
            continue

    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    print(f"Total Tests: {res['total']}, Passed: {res['pass']}, Failed: {res['fail']}, Errors: {res['error']}, Time: {total_time:.8f}s")


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
