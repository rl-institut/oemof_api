import os
import pathlib
import dotenv
import warnings

SERVER_ROOT = pathlib.Path(__file__).parent
ROOT_DIR = SERVER_ROOT.parent
DATA_DIR = ROOT_DIR / "data"
DATAPACKAGES_DIR = DATA_DIR / "datapackages"

# Load envs
env_file = os.environ.get("ENV", ".production")
if env_file == ".local":
    warnings.warn("Running local environment - in production this is a security risk!")
dotenv.load_dotenv(ROOT_DIR / ".envs" / env_file)

REDIS_URL = os.environ.get("REDIS_URL")
