"""
Application package initialization and factory function exports.
"""

from app.app import create_app

__all__ = ["create_app"]
