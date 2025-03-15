from typing import Literal

REPOSITORY_TYPE: Literal["sql", "memory"] = "sql"

DATABASE_URL = "postgresql://postgres:example@localhost:5432/postgres"

def use_in_memory_repositories():
    """Switch to in-memory repositories"""
    global REPOSITORY_TYPE
    REPOSITORY_TYPE = "memory"

def use_sql_repositories():
    """Switch to SQL repositories"""
    global REPOSITORY_TYPE
    REPOSITORY_TYPE = "sql"