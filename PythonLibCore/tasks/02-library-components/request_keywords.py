from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from TodoLibrary import TodoLibrary
import requests
from robotlibcore import keyword


class BaseLibraryComponent:
    def __init__(self, library: TodoLibrary | None = None):
        self.library = library


class RequestKeywords(BaseLibraryComponent):
    @keyword
    def create_todo(self, title: str, description: str, completed: bool = False):
        """Creates a new todo item."""
        response = requests.post(
            "http://localhost:8000/todo",
            json={"title": title, "description": description, "completed": completed},
        )
        response.raise_for_status()
        return response.json()

    @keyword
    def get_todos(self):
        """Retrieves all todo items."""
        response = requests.get("http://localhost:8000/todos")
        response.raise_for_status()
        return response.json()
