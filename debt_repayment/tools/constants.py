import logging
from pathlib import Path

# Constants
LOG_DIR = Path("debt_repayment/files/logs")
LOG_FILE = LOG_DIR / "getting_out_of_debt.log"
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"