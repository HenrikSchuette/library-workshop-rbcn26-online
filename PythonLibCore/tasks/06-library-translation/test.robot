*** Settings ***
Library     TodoLibrary.py    plugin=${CURDIR}/TearDownKeywords.py     translation=${CURDIR}/de.json
# This way keywords are only available in german.



*** Test Cases ***
My Test Case
    # Create Todo    Buy milk2    I need to buy milk    False
    Erstelle Todo    Milch kaufen2    Ich muss Milch kaufen    False
    # ${todos}=    Get Todos
    # Log    ${todos}
    # [Teardown]    TodoLibrary.Delete All Todos
