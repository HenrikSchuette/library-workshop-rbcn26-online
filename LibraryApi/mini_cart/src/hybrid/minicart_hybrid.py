"""
MiniCart Hybrid Library (reference implementation).

Scenario: Config-driven keyword exposure.

- Target module: components.minicart_starter
- Library argument: keywords="all" | "pricing"
- Hybrid API methods:
  - get_keyword_names(): controls discovery
  - __getattr__(): delegates execution to the underlying module functions

Notes:

This implementation intentionally uses a simplified discovery rule:
'public callables from the target module'.
"""

from types import ModuleType
from typing import Callable

from robot.api.deco import library

import components.minicart_starter as _minicart

# Keyword groups (by the function names in minicart_starter).
_GROUPS: dict[str, list[str]] = {
    "pricing": ["apply_discount", "total_with_tax"],
    "cart": ["add_line_item", "sum_line_items"],
}

@library(scope="SUITE", version="0.0.1")
class MiniCartHybridLibrary:
    """
    Hybrid library that exposes a configurable subset of minicart KWs.
    """

    def __init__(self, kw_group: str = "all"):
        # The source of the keyword implementations.
        self._target: ModuleType = _minicart
        # Normalize (from e.g. "" or "All").
        self._group = (kw_group or "all").strip().lower()

    # Hyrid API methods.

    def get_keyword_names(self) -> list[str]:
        """
        Return a list of keyword names (as strings) based on the
        selected group.
        """
        # 1) Get all KW implementations in the target (callable + public).
        if self._group == "all":
            fn_names: list[str] = [
                ...
                # Get all attribute names from the target module,
                # that are callable and public (not private).
                # Use: dir(), callable(), getattr(), startswith().
            ]
        # 2) Get only the keywords that are in the selected group.
        elif self._group in _GROUPS:
            fn_names: list[str] = ... # Get the function names directly from _GROUPS.
        # 3) Handle an unknown/invalid group name.
        else:
            raise ValueError(
                f"Unknown KW group: {self._group!r}."
                f"Supported groups: 'all', {sorted(_GROUPS)}"
            )
        # 4) Return KW names in Robot-style: 'function_name' -> 'Function Name'.
        fn_names.append("library_info")
        return [... for n in fn_names]

    def __getattr__(self, name: str) -> Callable:
        """
        Return the callable implementing the given keyword name.

        Robot resolves keywords by direct attribute access on the
        library instance.

        For hybrid libraries, __getattr__ can return a callable for
        names that are not attributes of the imported library.
        """
        # Robot name to function name.
        fn_name = ...
        # Try to get the attribute (by name) from the module.
        func = ...
        # Return if callable and public.
        if ...:
            return func
        # Or raise error due to missing keyword.
        raise AttributeError(f"No such keyword or attribute: {name}")

    # Helper methods.

    @staticmethod
    def _to_robot_name(fn_name: str) -> str:
        return fn_name.replace("_", " ").title()

    @staticmethod
    def _from_robot_name(robot_name: str) -> str:
        # Inverse of _to_robot_name for this workshop's naming scheme
        return robot_name.strip().lower().replace(" ", "_")
