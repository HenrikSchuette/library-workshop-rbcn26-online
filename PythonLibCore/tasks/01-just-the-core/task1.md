# Task 1: Just the Core

- Get to know the Todo API app.
- Create a 'TodoLibrary' class that inherits from 'DynamicCore'.
- Create a keyword called 'create_todo' with the following parameters: 'title', 'description' and 'completed' (default: False).
- The keyword uses requests.post() to send a POST request to {base_url}/todos with the provided parameters as a JSON payload.
- Create a Robot Framework test that uses the library and keyword.