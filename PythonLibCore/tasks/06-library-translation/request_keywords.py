import requests
from robotlibcore import keyword

from library_component import BaseLibraryComponent


class RequestKeywords(BaseLibraryComponent):
    @keyword
    def create_todo(self, title: str, description: str, completed: bool = False):
        """Creates a new todo item."""
        response = requests.post(
            f"{self.library.base_url}/todo",
            json={"title": title, "description": description, "completed": completed},
            timeout=self.library.timeout,
        )
        response.raise_for_status()
        return response.json()

    @keyword
    def get_todos(self):
        """Retrieves all todo items."""
        response = requests.get(
            f"{self.library.base_url}/todos", timeout=self.library.timeout
        )
        response.raise_for_status()
        return response.json()
