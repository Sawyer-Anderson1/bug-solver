"""

src/tools/test_tools.py


Bridge layer exposing Git operations to the LLM.
Translates adapter responses/outcomes into Markdown response templates.
"""

# -----------------------------------------
#  Necessary Standard & LangChain Imports
# -----------------------------------------
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

    return []
