from .base import BaseLogicUnit
from pandas import DataFrame
from config.configtracker import ConfigTracker
from llm.openai import OpenAI
from llm.base import LLM
from typing import Any, Generator, List, Union
from helpers.optional import import_dependency
from constants import WHITELISTED_BUILTINS, WHITELISTED_LIBRARIES
import pandas as pd
import ast
import astor

class ExecuteCode(BaseLogicUnit):

    def __init__(self, configtracker: ConfigTracker = None, dfs: List = None, query: str = None):
        super(ExecuteCode, self).__init__(config=configtracker)
        self.dfs = dfs
        self.query = query
        self.llm = LLM(OpenAI(temperature=0.3))

    def _required_dfs(self, code: str) -> List[str]:
        """
        List the index of the DataFrames that are needed to execute the code. The goal
        is to avoid to run the connectors if the code does not need them.

        Args:
            code (str): Python code to execute

        Returns:
            List[int]: A list of the index of the DataFrames that are needed to execute
            the code.
        """

        # Sometimes GPT-3.5/4 use a for loop to iterate over the dfs (even if there is only one)
        # or they concatenate the dfs. In this case we need all the dfs
        if "for df in dfs" in code or "pd.concat(dfs)" in code:
            return self.dfs

        required_dfs = []
        for i, df in enumerate(self.dfs):
            if f"dfs[{i}]" in code:
                required_dfs.append(df)
            else:
                required_dfs.append(None)
        return required_dfs
    
    def _get_environment(self) -> dict:
        """
        Returns the environment for the code to be executed.

        Returns (dict): A dictionary of environment variables
        """
        return {
            "pd": pd,
            **{
                lib["alias"]: getattr(import_dependency(lib["module"]), lib["name"])
                if hasattr(import_dependency(lib["module"]), lib["name"])
                else import_dependency(lib["module"])
                for lib in self._additional_dependencies
            },
            "__builtins__": {
                **{builtin: __builtins__[builtin] for builtin in WHITELISTED_BUILTINS},
                "__build_class__": __build_class__,
                "__name__": "__main__",
            },
        }
    
    def _check_imports(self, node: Union[ast.Import, ast.ImportFrom]):
        """
        Add whitelisted imports to _additional_dependencies.

        Args:
            node (object): ast.Import or ast.ImportFrom

        Raises:
            BadImportError: If the import is not whitelisted

        """
        module = node.names[0].name if isinstance(node, ast.Import) else node.module
        library = module.split(".")[0]

        if library == "pandas":
            return

        if (
            library
            in WHITELISTED_LIBRARIES
        ):
            for alias in node.names:
                self._additional_dependencies.append(
                    {
                        "module": module,
                        "name": alias.name,
                        "alias": alias.asname or alias.name,
                    }
                )
            return

        if library not in WHITELISTED_BUILTINS:
            raise f"Bad Import - {library}"
        
    
    def _is_jailbreak(self, node: ast.stmt) -> bool:
        """
        Remove jailbreaks from the code to prevent malicious code execution.
        Args:
            node (ast.stmt): A code node to be checked.
        Returns (bool):
        """

        DANGEROUS_BUILTINS = ["__subclasses__", "__builtins__", "__import__"]

        node_str = ast.dump(node)

        return any(builtin in node_str for builtin in DANGEROUS_BUILTINS)

    def _is_unsafe(self, node: ast.stmt) -> bool:
        """
        Remove unsafe code from the code to prevent malicious code execution.

        Args:
            node (ast.stmt): A code node to be checked.

        Returns (bool):
        """

        code = astor.to_source(node)
        return any(
            (
                method in code
                for method in [
                    ".to_csv",
                    ".to_excel",
                    ".to_json",
                    ".to_sql",
                    ".to_feather",
                    ".to_hdf",
                    ".to_parquet",
                    ".to_pickle",
                    ".to_gbq",
                    ".to_stata",
                    ".to_records",
                    ".to_latex",
                    ".to_html",
                    ".to_markdown",
                    ".to_clipboard",
                ]
            )
        )


    def _clean_code(self, code:str) -> str:
        """
        A method to clean the code to prevent malicious code execution.

        Args:
            code(str): A python code.

        Returns:
            str: A clean code string.

        """

        # Clear recent optional dependencies
        self._additional_dependencies = []

        tree = ast.parse(code)

        # Check for imports and the node where analyze_data is defined
        new_body = []
        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                self._check_imports(node)
                continue

            if (
                self._is_jailbreak(node)
                or self._is_unsafe(node)
            ):
                continue

            new_body.append(node)

        new_tree = ast.Module(body=new_body)
        return astor.to_source(new_tree, pretty_source=lambda x: "".join(x)).strip()

    
    def execute(self):
        code_to_run = self.config.get("pandas_code_generation_response") 
        code_to_run = self._clean_code(code_to_run)
        print(code_to_run)
        dfs = self._required_dfs(code_to_run) 
        print("===============================================")
        print(dfs)
        environment: dict = self._get_environment()
        environment["dfs"] = dfs
        exec(code_to_run, environment)
        if "result" not in environment:
            self.config.set("code_execution_result", None)
        else:
            self.config.set("code_execution_result", environment.get('result', None))
        return {
            "config": self.config, 
            "dfs": self.dfs,
            "query": self.query
        }


