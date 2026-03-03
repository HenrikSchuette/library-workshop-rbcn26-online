from library_component import BaseLibraryComponent

import requests
from robotlibcore import keyword


class TearDownKeywords(BaseLibraryComponent):
    @keyword
    def delete_all_todos(self):
        todos = requests.get(f"{self.library.base_url}/todos").json()
        for todo in todos:
            requests.delete(f"{self.library.base_url}/todo/{todo['id']}")
