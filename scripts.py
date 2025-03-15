import subprocess
import uvicorn

def start():
    """Start the application using repository type from .env file"""
    print("Starting server with repository type from .env file...")
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
    update_env_file('REPOSITORY_TYPE', 'memory')
    print("Switched to in-memory repositories")
    print("Restart the server for changes to take effect")

def use_postgres_db():
    """Switch the application to use PostgreSQL repositories"""
    update_env_file('REPOSITORY_TYPE', 'sql')
    print("Switched to PostgreSQL repositories")
    print("Restart the server for changes to take effect")