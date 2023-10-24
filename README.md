# DOCUMENTATION

- (Yannik 11.10.2023)
    opened documentation
- (Wassim 11.10.2023)
    opened documentation
- (Ambros 11.10.2023)
    opened documentation



-----------------------------------------------------------------**Main**----------------------------------------------------------------
- (Ambros 16.10.2023)
    <p> In the main function the flow of the program is being controlled. There are also some computations, which matter <br>
    for multiple functions. The main function first finds the absolute path of the parent directory of the run_tests.py, <br>
    so it is guaranteed that the files for testing are being generated in the correct directory no matter where the file <br>
    is being run from. This is done in the main function, since it is needed in the setup and teardown function. <br>
    Further the list files_start is initialized which gives a timestamp of the files in the parent directory of the <br>
    run_tests.py this will be of importance when the teardown function is run to compare which files where already <br>
    existing and which were generated. </p>
    
    

----------------------------------------------------------------**Setup**----------------------------------------------------------------
- (Ambros 16.10.2023)
    <p> In the setup function the environment is being prepared for the testing. </p>
    <p> Here all files are created, which are after being used by the individual tests (expect for files created by the <br>
    test itself). </p>
    <p> There are 3 dictionaries, so the files can be split by functionality in the tests. </p>
        <p> the f_read is for files which are being used by the tests for the read function </p>
        <p> the f_write is for files which are being used by the tests for the write function </p>
        <p> the f_delete is for files which are being used by the tests for the delete function </p>
        <p> for the create function there are no files needed, since it is going to create the files itself </p>
    <p> The decision to use 3 dictionaries: </p>
        <p> On the one hand this generates a little overhead, since also a single dictionary could be used for all the <br>
        files which are being created, however like this there is a better overview which might help in scalability of <br>
        the code. </p>
        <p> Also it reduces the chances of faulty reusing of files for multiple tests. (e.g. test tries to read a file <br>
        which has been already deleted by another test). With this organization it is clear which files can be reused <br> 
        and which should only be used once (f_delete e.g.). </p>
    <p> After all the files specified in the 3 dictionaries are being created in the parents directory of run_tests.py <br>
    with the given content. </p>

----------------------------------------------------------------**User**-----------------------------------------------------------------

- (Yannik 23.10.2023)
    <p> We imported the sys module to be able to read the user input. With sys.argv we can access the command-line <br>
    arguments. The pattern is set to None if there is no pattern selection, so all tests are selected by default. <br>
    In the main we check if the user has selected a pattern for example "read" and assign it to the variable pattern. <br>
    The pattern is passed to the tests() function where all tests with this pattern are tested (or by default all tests <br>
    are tested). Before we test we have to check if there are tests with the selected pattern and this happens in the <br>
    for loop before the try block. </p>

---------------------------------------------------------------**Results**---------------------------------------------------------------
- (Yannik 21.10.2023)
    <p> The results are tracked and afterwards printed inside the tests() function. We have decided to give the results <br> 
    for each individual test and at the end print the overview of all tests In the res dictionary the three outcomes <br>
    pass, fail and error will be updated during testing. </p>
    <p> As we learned in the lecture, we used introspection to find all tests with the prefix "test_" which we want to <br>
    test. For the individual test results, the time will be tracked with the time.time() method and starts before the <br>
    test is performed. Depending on how the test results, the time will stop in the try or one of the two except blocks <br>
    and the result will be printed for this test. After the except blocks a finally block is implemented to track the <br>
    total number of tests which are carried out. In the for loop the res dictionary gets updated with the outcome of <br>
    every test performed and when the loop ends, the time is stopped. Finally, the overall results of the testing is <br>
    printed out. </p>

- (Ambros 24.10.2023)
    <p>The results are color-coded for a better overview</p><br>
    <p>Green is used in case the test passes, yellow for fails and red for errors.</p><br>
    <p>Indents and symbols are also used to allow for a better readibility, the time information has been caped at 8 floating points. Since 
    the tests do not require big amounts of computation the tests will execute rather quickly, with 8 digits the time information is still 
    there and the output is more readable</p><br>

----------------------------------------------------------------**Tests**----------------------------------------------------------------
- (Wassim 23.10.2023)
    <p>The name is very important for all test functions. Each test must begin with test_ so that the tests can be found <br>
    in the tests() function as discussed in class. The rest of the name was chosen so that one should already understand <br>
    what is being tested with this function.</p>
    <p>The three tests for the read_me() function are similar to those already discussed in the lab and task description. <br>
    The files have already been entered in the setup() function, so we only applied the read_file function and set it <br>
    equal to the content. The next test checks if you want to read an empty file and the last one compares a non-existent <br>
    file to None. <br></p>
    <p>We have two tests for the create_file function. The first one tests if we can create a new empty file and asserts it <br>
    to True. The second one checks if we can create an already existing file. It also checks if we would overwrite the already <br>
    existing file with the new content. <br></p>
    <p>We have four different tests for the write_file() function. The first test checks if new content can be written at all. <br>
    We use the write_file function to write new content in an already existing file. The next test checks if we can write an <br>
    empty string. We have to use the write_file() function first to write an emtpy string and then assert the file equal to an <br>
    empty string. We also test if we can write to a non-existing file. Since the file doesn't exist, it is not mentioned in the <br> 
    setup function. The last test checks if we can write with some special characters.<br></p>
    <p>The delete_file tests are structured the same as the others. Here, however, we have built in two assert arguments, one to <br>
    see if the file has been deleted and another just to extra check that there is nothing in the file with the read_me function. <br>
    The first test deletes an existing file. The file is already mentioned in the setup function as well. The next test <br>
    checks if we can delete a non existing file. The last test deletes an empty file.</p>

- (Ambros 24.10.2023)
    <p>The test execution order is randomized to ensure that all tests are independent from one another</p><br>
    <p>Tests also give a little feedbackmessage in case the test fails, so the user already has a first hint where the failure might come from 
    e.g. test for writing wheter the file has not been written at all or with the wrong contents</p><br>
    <p>Tests get an argument path_t which stands for path test. It is the absolute path to the file which is being manipulated by the 
    test function. Therefore it makes sense to only manipulate one file per test, since otherwise the absolute path would need to be 
    reconstructed. An alternative would be to give the test functions the path to the parent, so it is easy to reconstruct absolute paths 
    to multiple files, however it is good practice to test only one functionality per test which makes this concern fade.</p><br>

--------------------------------------------------------------**Teardown**---------------------------------------------------------------

- (Ambros 16.10.2023)
    <p> In the teardown function all files which were generated during the test are being removed. </p>
    <p> The approach is to get a stamp of all files which exist in the beginning of the program and then in the end <br>
    delete all files which are not in the stamp from the beginning. Therefore, all files that are generated after the <br>
    list files_start has been made will be deleted. </p>
        <p> This poses a problem: The teardown function does not distinguish between files which were generated by the <br>
        testing and files which were generated by something else (e.g. another developer) </p>
        <p> Another approach which would fix this problem is to work with a list (e.g. move the dictionary with all filenames <br>
        from the tests function to the main function and pass the values to the teardown) however this would make the code <br>
        harder to understand and the main functions purpose is flow control, not storing and distributing dictionaries.<br>

---------------------------------------------------------------**Further**---------------------------------------------------------------

- (Ambros 24.10.2023)
    <p>What still could be added in the future:</p><br>
    <p>Information for the tests if the test has an error</p><br>
    <p>User option to get the time output without the cutting to get more detailed information</p><br>
    <p>Additional cleanup if program crashes unexpectedly -> having teardown always even if program crashes</p><br>
    <p>Cleanup function that removes everything from folder except for files of the program and files specified in case there are
    many files produced by an error</p><br>
    <p>In case the of big test amounts consider minimizing the setup function with the --select option</p><br>



