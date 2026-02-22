# Task 3: Library Instance

- Add a library argument called 'timeout' to the 'TodoLibrary' class.
- The timeout value should then be passed to the 'RequestKeywords' class and all other library components that require it.
- Update the 'create_todo' and 'get_todos' keywords so that they use the timeout value when making API calls.
- Create a Robot Framework test to verify the timeout functionality by setting a short timeout and ensuring that a timeout exception is raised if the API call takes too long.
- The timeout value of the test object can be increased by entering the command 'uv run todo-rest --latency <milliseconds>' in the terminal.