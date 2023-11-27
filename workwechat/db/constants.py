import os

ROOT_DIR = os.path.expanduser("~\\Desktop\\SMR")
ROAMING_PATH = os.getenv("APPDATA")
DATA_PATH = os.path.join(ROAMING_PATH, "SMR")
LOG_PATH = os.path.join(DATA_PATH, "log")
DB_PATH = os.path.join(DATA_PATH, "data")


if __name__ == '__main__':
    print(DB_PATH)