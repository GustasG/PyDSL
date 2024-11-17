"""
Custom exceptions for environment errors.
"""


class EnvironmentNotFoundError(Exception):
    """
    Exception raised when an environment with specified ID cannot be found.
    """

    def __init__(self, environment_id: str):
        self.id = environment_id


class DefinitionNotFoundError(Exception):
    """
    Exception raised when a definition with specified ID cannot be found.
    """

    def __init__(self, definition_id: str):
        self.id = definition_id


class ExecutionError(Exception):
    """
    Exception raised when an error occurs during environment execution.
    """

    def __init__(self, callable_: str):
        self.callable = callable_