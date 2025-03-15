import os
from typing import Literal
from dotenv import load_dotenv

load_dotenv()

def use_in_memory_repositories():
    """Switch to in-memory repositories for current process only"""
    os.environ["REPOSITORY_TYPE"] = "memory"

def use_sql_repositories():
    """Switch to SQL repositories for current process only"""
    os.environ["REPOSITORY_TYPE"] = "sql"

def get_repository_type() -> Literal["sql", "memory"]:
    """Get the current repository type"""
    return os.environ.get("REPOSITORY_TYPE", "sql")