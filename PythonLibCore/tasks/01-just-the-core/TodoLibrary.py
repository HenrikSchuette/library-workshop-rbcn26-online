from robotlibcore import keyword, DynamicCore
import requests


class TodoLibrary(DynamicCore):
    def __init__(self):
        super().__init__([])
        self.base_url = "http://localhost:8000"

    @keyword
    def create_todo(self, title: str, description: str, completed: bool = False):
        """Creates a new todo item."""
        response = requests.post(
            f"{self.base_url}/todo",
            json={"title": title, "description": description, "completed": completed},
        )
        response.raise_for_status()
        return response.json()
