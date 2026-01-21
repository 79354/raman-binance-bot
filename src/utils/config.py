import os
import logging
from binance.um_futures import UMFutures
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
USE_TESTNET = os.getenv("USE_TESTNET", "True").lower() == "true"

BASE_URL = "https://testnet.binancefuture.com" if USE_TESTNET else "https://fapi.binance.com"

def get_client() -> UMFutures:
    """
    Initializes and returns the Binance USDT-M Futures Client.
    """
    if not API_KEY or not SECRET_KEY:
        raise ValueError("API credentials not found in .env file.")
    
    return UMFutures(key=API_KEY, secret=SECRET_KEY, base_url=BASE_URL)

def setup_logger(name: str) -> logging.Logger:
    """
    Configures a structured logger that writes to console (INFO) 
    and file (DEBUG).
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )

    # File Handler (bot.log)
    file_handler = logging.FileHandler('bot.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # Avoid duplicate handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger