*** Settings ***
Library     MyLibCoreLibrary.py


*** Test Cases ***
My Test Case
    ${result1}    My Keyword
    Should Be Equal    ${result1}    my_keyword executed!
    ${result2}    Library Component Keyword
    Should Be Equal    ${result2}    library_component_keyword executed!
