import os


def setup(location):
    """use setup to create needed files with name and optional content"""

    #dictionary with filename as key and content as value
    #files to be read in the tests
    f_read = {
        "first.txt":"this is a text"

    }
    #files to be written to in the tests
    f_write={

    }
    #files to delete during the test
    f_delete={

    }

    #create all the files
    file_types = [f_read, f_write, f_delete]
    for files in file_types:
        for name, content in files.items():
            file_path = os.path.join(location,name)
            with open(file_path, 'w') as test_file:
                test_file.write(content)
            

    return None


def tests():

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


