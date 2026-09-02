"""

src/tools/test_tools.py


Bridge layer exposing Git operations to the LLM.
Translates adapter responses/outcomes into Markdown response templates.
"""

# -----------------------------------------
#  Necessary Standard & LangChain Imports
# -----------------------------------------
import os
from pathlib import Path
from typing import List, Callable
from langchain_core.tools import tool, BaseTool

# -----------------------------------------
#  Abstract Interface & Result Types
# -----------------------------------------
from adapters.testing.base import BaseTestRunner
from adapters.testing.types import TestResult, TestOpStatus

# -----------------------------------------
#  Helper / Prompt Engineering Utility
# -----------------------------------------
from utils.template_loader import load_response_template


# -----------------------------------------
#  Factory Function (Dependency Injection)
# -----------------------------------------
def test_tools(test_adapter: BaseTestRunner) -> List[BaseTool]:
    """
    Factory that binds an adapter implementation to LangChain @tools decorators.
    Using parse_docstring to give more argument context to the LLM.
    Returns a list of tools to be bound to a LangGraph node(s).
    """

    # -------------------------------------
    #  Tools 1: Run Tests
    # -------------------------------------
    @tool(parse_docstring=True)
    def run_tests(paths: list[str | os.PathLike | Path] = None, keyword: str = None):
        """
        This tool runs tests located in the repository

        Args:
            paths: List of paths of test files
            keyword: Keyword that specifies certain test files to be run, that have that name
        """

        # Execute via abstract adapter
        result: TestResult = test_adapter.run_tests(paths=paths, keyword=keyword)

        # Then load the markdown response template
        template: str = load_response_template(
            skill="test_runner", tool_name="run_tests", section=result.status.value
        )

        # Format template placeholders with tool inputs and adapter results
        return template.format(
            paths=paths,
            keyword=keyword,
            raw_data=result.raw_data,
            error_details=result.error_details,
            passed=result.passed,
            failed=result.failed,
        )

    # -------------------------------------
    #  Tools 2: Collect Tests
    # -------------------------------------
    @tool(parse_docstring=True)
    def collect_tests(
        paths: list[str | os.PathLike | Path] = None, keyword: str = None
    ):
        """
        Collects tests to be retreived

        Args:
            paths: List of paths of test files
            keyword: Keyword that specifies certain test files to be run, that have that name
        """

        # Execute via abstract adapter
        result: TestResult = test_adapter.collect_tests(paths=paths, keyword=keyword)

        # Then load the markdown response template
        template: str = load_response_template(
            skill="test_runner", tool_name="collect_tests", section=result.status.value
        )

        # Format template placeholders with tool inputs and adapter results
        return template.format(
            paths=paths,
            keyword=keyword,
            raw_data=result.raw_data,
            error_details=result.error_details,
            passed=result.passed,
            failed=result.failed,
        )

    # -------------------------------------
    #  Tools 3: Run Test Command
    # -------------------------------------
    @tool(parse_docstring=True)
    def run_test_command(args_str: str, timeout_seconds: float = 60.0):
        """
        Fallback command that can run a variety of commands using the args_str variable.

        Args:
            args_str: String of arguments to be run for a test command
            timeout_seconds:  The time give for a command to be run, defaults to 60 seconds
        """

        # Execute via abstract adapter
        result: TestResult = test_adapter.run_test_command(
            args_str=args_str, timeout_seconds=timeout_seconds
        )

        # Then load the markdown response template
        template: str = load_response_template(
            skill="test_runner",
            tool_name="run_test_command",
            section=result.status.value,
        )

        # Format template placeholders with tool inputs and adapter results
        return template.format(
            args_str=args_str,
            timeout_seconds=timeout_seconds,
            raw_data=result.raw_data,
            error_details=result.error_details,
        )

    return [run_tests, collect_tests, run_test_command]
