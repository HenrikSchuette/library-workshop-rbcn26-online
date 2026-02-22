*** Settings ***
Library     MyLibCoreLibrary.py    take_screenshot


*** Test Cases ***
My Test Case
    My Keyword
    TRY
        My Failing Keyword
    EXCEPT
        Pass Execution    This keyword fails on purpose
    END
