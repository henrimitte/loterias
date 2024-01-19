from pathlib import Path


BASE_DIR = Path.home() / '.local/lib/loterias/'
BASE_DIR.mkdir(exist_ok=True, parents=True)

DATA_DIR = BASE_DIR / 'data/'
DATA_DIR.mkdir(exist_ok=True, parents=True)

LOGS_DIR = BASE_DIR / 'logs/'
LOGS_DIR.mkdir(exist_ok=True, parents=True)
