*** Settings ***
Library     MyLibCoreLibrary.py


*** Test Cases ***
My Test Case
    ${result}    My Keyword
    Should Be Equal    ${result}    some result
