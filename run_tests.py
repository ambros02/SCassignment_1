import os
import time
import file_manager



def setup(location):
    """use setup to create needed files with name and optional content"""

    #dictionary with filename as key and content as value
    #files to be read in the tests
    f_read = {
        "read_test_file": "content_for_test_file",
        "read_empty_test_file": ""
    }
    #files to be written to in the tests
    f_write = {
        "write_test_file": "old_content_for_write_test_file",
        "write_empty_content_test_file": "",
        "write_special_char_test_file": "$£!?%&ç*"
    }
    #files to delete during the test
    f_delete = {
        "delete_existing_test_file": "content_to_delete",
        "delete_empty_test_file": ""
    }

    #create all the files
    file_types = [f_read, f_write, f_delete]
    for files in file_types:
        for name, content in files.items():
            file_path = os.path.join(location,name)
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
    file_name = "create_empty_file.txt"
    result = file_manager.create_file(file_name)
    assert result is True  # Creating an empty file should return True
    # Check if the file is empty
    file_content = file_manager.read_file(file_name)
    assert file_content == ""


def test_create_existing_file():
    # Test creating a file with a name that already exists
    file_name = "existing_file"
    initial_content = "initial_content"
    file_manager.create_file(file_name, initial_content)
    new_content = "new_content"
    result = file_manager.create_file(file_name, new_content)
    assert result is True  # Creating a file with an existing name should return True
    # Check if the file was overwritten with the new content
    file_content = file_manager.read_file(file_name)
    assert file_content == new_content


"""test functions for write_file"""


def test_write_file():
    # Overwrite existing test file
    file_manager.write_file("write_test_file", "new_content_for_write_test_file")
    assert file_manager.read_file("write_test_file") == "new_content_for_write_test_file"

def test_write_empty_content():
    # Test writing empty content to an existing file
    file_manager.write_file("write_empty_content_test_file", "")
    assert file_manager.read_file("write_empty_content_test_file") == ""


def test_write_non_existing_file():
    # Test writing to a non-existing file
    result = file_manager.write_file("non_existing_file", "content_to_be_written")
    assert result is True  # Writing to a non-existing file should create the file and return True

def test_write_special_char():
    # Test writing content with special characters to a file
    content = "Special characters: $£?!*ç%&"
    file_manager.write_file("write_special_char_test_file", content)
    assert file_manager.read_file("write_special_char_test_file") == content


"""test functions for delete_file"""


def test_delete_existing_file():
    result = file_manager.delete_file("delete_existing_test_file")
    assert result is True  # Deleting an existing file should return True
    assert file_manager.read_file("delete_existing_test_file") is None


def test_delete_non_existing_file():
    result = file_manager.delete_file("non_existing_file")
    assert result is False  # Deleting a non-existing file should return False


def test_delete_empty_file():
    result = file_manager.delete_file("delete_empty_test_file")
    assert result is True  # Deleting an empty file should return True
    assert file_manager.read_file("delete_empty_test_file") is None
    
def tests():
    total_start_time = time.time()
    res = {"total": 0, "pass": 0, "fail": 0, "error": 0}
    for(name, test) in globals().items():
        if not name.startswith("test_"):
            continue
        test_start_time = time.time()
        try:
            test()
            res["pass"] += 1
            test_end_time = time.time()
            test_time = test_end_time - test_start_time
            print(f"Test: {name}, Pass, Time: {test_time}s")
        except AssertionError:
            res["fail"] += 1
            test_end_time = time.time()
            test_time = test_end_time - test_start_time
            print(f"Test: {name}, Fail, Time: {test_time}s")
        except Exception:
            res["error"] += 1
            test_end_time = time.time()
            test_time = test_end_time - test_start_time
            print(f"Test: {name}, Error, Time: {test_time}s")
        finally:
            res["total"] += 1

    total_end_time = time.time()
    total_time = total_end_time - total_start_time
    print(f"Total Tests: {res['total']}, Passed: {res['pass']}, Failed: {res['fail']}, Errors: {res['error']}, Time: {total_time}s")


def find_tests():

    return None

def teardown(location, existing_start):
    """remove all files that were generated in the testing: more precicely all the files which were not in this folder in the beginning"""
    
    #files which exist after the program has been run
    files_end = os.listdir(location)

    #deleting of the files if they were not part of the original program
    for file in files_end:
        if file not in existing_start:
            file_path = os.path.join(location, file)
            os.remove(file_path)

    return None



def main():
    """main function for the flow control of the program"""

    #get a stamp of which files exists before execution, so we can delete the ones that were generated in the test
    files_location = os.path.dirname(os.path.abspath(__file__))
    files_start = os.listdir(files_location)


    setup(files_location)

    tests()

    teardown(files_location, files_start)


    return None



if __name__ == "__main__":
    """run the main function if this is the main file"""
    main()


