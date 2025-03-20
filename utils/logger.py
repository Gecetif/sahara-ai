from loguru import logger
import sys

logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <7}</level> |  <level>{message}</level>",
    colorize=True
)
logger.add('./data/logs.log', format="{time:YYYY-MM-DD HH:mm:ss} | {level: <5} | {message}", enqueue=True)

def get_logger():
    return logger
