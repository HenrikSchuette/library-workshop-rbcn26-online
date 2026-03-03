*** Settings ***
Library     TodoLibrary.py    plugin=${CURDIR}/TearDownKeywords.py     # Hier ein Problem mit Backslashes in Windows
# Library     TodoLibrary.py    plugin=E:/Projekte/robocon_library_workshop/PythonLibCore/tasks/05-plugin-interface/TearDownKeywords.py



*** Test Cases ***
My Test Case
    Create Todo    Buy milk2    I need to buy milk    False
    ${todos}=    Get Todos
    Log    ${todos}
    [Teardown]    TodoLibrary.Delete All Todos
