*** Settings ***
Library     OpenApiLibrary


*** Test Cases ***
My Test Case
    Post Todo    TodoCreate=${{{'title': "Buy milk", 'description': "Remember to buy milk", 'completed': False}}}
    ${all_todos}=    Get Todos
    # ${single_todo}=    Get Todo   1
    VAR     &{updated_todo}    title=Buy milk    description=Remember to buy milk    completed=True
    Put Todo   todo_id=${all_todos[0]['id']}    TodoCreate=${updated_todo}
    [Teardown]    Delete ALL Todos

*** Keywords ***
Delete ALL Todos
    ${todos}=    Get Todos
    FOR    ${todo}    IN    @{todos}
        Delete Todo   todo_id=${todo['id']}
    END