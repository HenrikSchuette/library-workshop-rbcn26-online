"""
MiniCart Dynamic Library
========================

This module demonstrates a minimal Robot Framework dynamic test library.

It is a natural evolution of our hybrid example:

- Hybrid library:
  - Discovery is dynamic (get_keyword_names).
  - Execution is attribute-based (__getattr__).

- Dynamic library:
  - Discovery is dynamic (get_keyword_names).
  - Execution is dynamic (run_keyword).

In this implementation:

- The keyword surface is determined at import time based on a
  configuration argument (kw_group).
- A keyword registry (Robot name -> Python callable) is built.
- Robot Framework interacts with the library exclusively via the
  Dynamic Library API methods.

This example is intentionally minimal. It implements only:

- get_keyword_names()
- run_keyword()
- get_keyword_documentation() (optional hook)

The goal is to clearly demonstrate how the dynamic API works,
without introducing advanced patterns or tooling complexity.
"""

from collections.abc import Mapping, Sequence
from types import ModuleType
from typing import Any, Callable

from robot.api.deco import library

import components.minicart_starter as _minicart

_GROUPS: dict[str, list[str]] = {
    "pricing": ["apply_discount", "total_with_tax"],
    "cart": ["add_line_item", "sum_line_items"],
}


@library(scope="SUITE", version="0.0.1")
class MiniCartDynamicLibrary:
    """
    Dynamic Robot Framework library for the MiniCart example.

    The library exposes keywords from the underlying
    `minicart_starter` module.

    The visible keyword set is determined by the constructor argument
    `kw_group`:

    - "all"      -> expose all public callables
    - "<group>"  -> expose only keywords in that group

    Unlike static or hybrid libraries, execution is fully controlled
    through the Dynamic Library API:

    - Robot asks for keyword names via get_keyword_names()
    - Robot executes keywords via run_keyword()

    This central dispatch point is the key distinguishing feature of
    dynamic libraries.
    """


    def __init__(self, kw_group: str = "all"):
        """
        When importing this library a central keyword registry is
        constructed.

        The registry maps:

        Robot keyword name -> underlying Python callable

        And is later used by:

        - get_keyword_names()
        - run_keyword()
        - get_keyword_documentation()

        Parameters
        ----------
        kw_group : str
            Determines which subset of keywords is exposed.

            - "all" exposes all public functions from the target module.
            - A named group exposes only the functions listed in _GROUPS.
        """
        # The source of the keyword implementations.
        self._target: ModuleType = _minicart
        # Normalize (from e.g. "" or "All").
        self._group = (kw_group or "all").strip().lower()
        # Build the central registry, mappping kw-names->kw-implementations.
        self._registry: dict[str, Callable[..., Any]] = self._build_registry()


    # Dynamic API (mandatory).


    def get_keyword_names(self) -> list[str]:
        """
        Return the list of keyword names (as strings) exposed by this
        library.

        Robot Framework calls this method during import to determine:

        - Which keywords exist.
        - What names should be registered.
        - What handlers must be created internally

        In this implementation, the method simply returns the keys of
        the keyword registry.
        """
        return ...


    def run_keyword(
        self,
        name: str,
        args: Sequence[Any],
        named: Mapping[str, Any]
    ) -> Any:
        """
        Execute a keyword dynamically, unpacking ``args`` and ``named``.

        The latter means that, upon calling the keyword implementation,
        (method or function), this method forwards Robot’s positional
        and named arguments directly to the underlying callable.

        Core execution hook of the Dynamic Library API.

        Parameters
        ----------
        name : str
            The Robot Framework keyword name.
        args : Sequence[Any]
            Positional arguments from the test case.
        named : Mapping[str, Any]
            Named arguments from the test case.

        Flow:
        1. Resolve keyword name in the registry.
        2. Retrieve underlying Python callable (function/method).
        3. Invoke it with the provided arguments.

        Unlike hybrid libraries, execution does NOT rely on
        attribute lookup. Instead RF dispatches invocation of the KW
        implementation (i.e. method or function) to this method.

        This central dispatch point makes it possible to later add:

        - Retry logic
        - Timing
        - Error transformation
        - External delegation

        without modifying individual keyword implementations.
        """
        try:
            func = ... # Get the callable from the KW registry.
        except KeyError as e:
            # Or fail.
            raise AttributeError(f"Unknown keyword: {name!r}") from e
        return ... # Call, unpacking the arguments.


    # Dynamic API (optional).


    def get_keyword_documentation(self, name: str) -> str | None:
        """
        Return documentation for a keyword with ``name``.

        Robot Framework and tools such as Libdoc/RobotCode call this
        method to retrieve:

        - Keyword documentation
            - Retrieved from: ``func.__doc__``
            - If the method is called with a valid KW name.
        - Library documentation
            - Retrieved from __class__.__doc__
            - If the method is called with "__intro__"
        - Import documentation
            - Retrieved from __init__.__doc__
            - If the method is called with "__init__"
        """
        # Support Libdoc/Robotcode.
        if name == "__intro__":
            return ...
        if name == "__init__":
            return ...
        # Get the callable by name from the registry.
        func = ...
        # Return the retrieved doc (if func was found) or None.
        return ...


    # Helper methods.


    def _build_registry(self) -> dict[str, Callable[..., Any]]:
        """
        Build the keyword registry, that maps:

        Robot-style keyword name -> Python callable.

        Steps:
        1. Determine which function names should be exposed based on the
           selected kw_group.
        2. Retrieve the corresponding callables from the target module.
        3. Convert Python function names to Robot-style names.

        This registry is the single source of truth for:

        - KW discovery
        - KW execution
        - KW documentation
        """
        # 1) Determine function names to expose (same as hybrid).
        if self._group == "all":
            fn_names = [
                n for n in dir(self._target)
                if not n.startswith("_") and \
                    callable(getattr(self._target, n, None))
            ]
        elif self._group in _GROUPS:
            fn_names = list(_GROUPS[self._group])
        else:
            raise ValueError(
                f"Unknown KW group: {self._group!r}."
                f"Supported: 'all', {sorted(_GROUPS)}"
            )
        # 2) Map Robot keyword names -> callables.
        reg: dict[str, Callable[..., Any]] = {}
        for fn_name in fn_names:
            func = ... # Get the callable from the module object.
            reg[... ] = func # Registry key should be a Robot-type name.
        return reg


    @staticmethod
    def _to_robot_name(fn_name: str) -> str:
        return fn_name.replace("_", " ").title()
