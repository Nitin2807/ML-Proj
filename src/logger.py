import logging
import os
from datetime import datetime

# 1. Create the filename
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# 2. Define the 'logs' DIRECTORY path
logs_dir_path = os.path.join(os.getcwd(), 'logs')

# 3. Create the directory (not the file path)
os.makedirs(logs_dir_path, exist_ok=True)

# 4. Join the directory with the filename to get the actual FILE path
LOG_FILE_PATH = os.path.join(logs_dir_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format='[%(asctime)s: %(levelname)s: %(module)s]: %(message)s',
)