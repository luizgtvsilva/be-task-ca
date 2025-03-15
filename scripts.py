import subprocess
import uvicorn
import argparse
import sys


def cli_start():
    """
        Entry point for Poetry 'start' command that handles command-line arguments
        Examples of usage:
            Start with SQL database (default)
            'poetry run start'

            Start with in-memory database
            'poetry run start --db memory'

            Run other commands
            'poetry run format'
            'poetry run test'
            'poetry run memory'  # Switch to memory DB for other operations
            'poetry run sql'     # Switch to SQL DB for other operations
    """

    parser = argparse.ArgumentParser(description="Start the application with specified database")
    parser.add_argument("--db", choices=["sql", "memory"], default="sql",
                        help="Database type to use: 'sql' for PostgreSQL or 'memory' for in-memory")

    args = parser.parse_args()

    if args.db == "memory":
        use_memory_db()
    else:
        use_postgres_db()

    print(f"Starting server with {args.db} database...")
    uvicorn.run("be_task_ca.main:app", host="0.0.0.0", port=8000, reload=True)


def start():
    """Original start function without argument handling (for backward compatibility)"""
    uvicorn.run("be_task_ca.main:app", host="0.0.0.0", port=8000, reload=True)


def auto_format():
    subprocess.call(["black", "be_task_ca"])


def run_linter():
    subprocess.call(["flake8", "be_task_ca"])


def run_tests():
    subprocess.call(["pytest"])


def create_dependency_graph():
    subprocess.call(["pydeps", "be_task_ca", "--cluster"])


def check_types():
    subprocess.call(["mypy", "be_task_ca"])


def use_memory_db():
    """Switch the application to use in-memory repositories"""
    from be_task_ca.config import use_in_memory_repositories
    use_in_memory_repositories()
    print("Switched to in-memory repositories")


def use_postgres_db():
    """Switch the application to use PostgreSQL repositories"""
    from be_task_ca.config import use_sql_repositories
    use_sql_repositories()
    print("Switched to PostgreSQL repositories")