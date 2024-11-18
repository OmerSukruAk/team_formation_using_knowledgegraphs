import os
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(name: str) -> str:
    try:
        return os.environ[name]
    except KeyError:
        raise EnvironmentError(f"Set the {name} environment variable.")