
import logging
import warnings
import os

warnings.filterwarnings("ignore")

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, "app.log")

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    handlers=[logging.StreamHandler(), 
                              logging.FileHandler(log_file, mode='a')])

logger = logging.getLogger(__name__)