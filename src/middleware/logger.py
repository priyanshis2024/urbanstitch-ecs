import logging
import os
from datetime import datetime

log_dir = "src/logs"
os.makedirs(log_dir, exist_ok=True)

today_str = datetime.now().strftime("%d-%m-%Y")
log_file_path = os.path.join(log_dir, f"{today_str}.log")

logger = logging.getLogger(__name__)
handler = logging.FileHandler(filename=log_file_path)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
