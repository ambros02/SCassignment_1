# DOCUMENTATION

- (Yannik, 11.10.2023)
    opened documentation
- (Wassim, 11.10.2023)
    opened documentation
- (Ambros, 11.10.2023)
    opened documentation


---------------------------------------------------------------**Overview**--------------------------------------------------------------

-----------------------------------------------------------------**Main**----------------------------------------------------------------
- Ambros(16.10.2023)
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
        <p> for the create function there are no files needed, since it is gonna create the files itself </p>
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

----------------------------------------------------------------**Tests**----------------------------------------------------------------

--------------------------------------------------------------**Teardown**---------------------------------------------------------------
- (Ambros 16.10.2023)
    <p> In the teardown function all files which were generated during the test are being removed. </p>
    <p> The approach is to get a stamp of all files which exist in the beginning of the program and then in the end <br>
    delete all files which are not in the stamp from the beginning. Therefore all files that are generated after the <br>
    list files_start has been made will be deleted. </p>
        <p> This poses a problem: The teardown function does not distinguish between files which were generated by the <br>
        testing and files which were generated by something else (e.g. another developer) </p>
        <p> Another approach which would fix this problem is to work with a list (e.g. global list) which stores all the <br>
        names of files which are being generated by the test and have to be deleted in the end. However this generates <br>
        overhead since all the files which are being generated/deleted need to be tracked also it is prone to errors <br>
        (e.g. file is in the list which is already deleted). Therefore the decision has been made to use the first <br>
        approach, since it is not expected that files are being generated by something else than the test, while the <br>
        test is being run. </p>

--------------------------------------------------------------**Conclusions**-------------------------------------------------------------



