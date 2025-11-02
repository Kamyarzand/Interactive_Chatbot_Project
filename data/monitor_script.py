import time
import logging
from task26 import TemperatureMonitor

logging.basicConfig(
    filename='/home/dtuser/chatbot/tasks/output.log',
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    encoding='utf-8'
)

monitor = TemperatureMonitor()
city = "Braunschweig"

while True:
    try:
        monitor.record_reading(city)
        time.sleep(1800)  
    except Exception as e:
        logging.error(f"Error in monitoring loop: {str(e)}")
        time.sleep(1800)  