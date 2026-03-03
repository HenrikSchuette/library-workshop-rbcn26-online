*** Settings ***
Library     TodoLibrary.py


*** Test Cases ***
My Test Case
    Create Todo    Buy milk2    I need to buy milk    False
    ${todos}=    Get Todos
    Log    ${todos}
