*** Settings ***
Library     LibInstance.py


*** Test Cases ***
My Test Case
    ${result1}    My Keyword
    Should Be Equal    ${result1}    my_keyword executed!
    ${result2}    Library Component Keyword
    Should Be Equal    ${result2}    I am a property of MyLibCoreLibrary
