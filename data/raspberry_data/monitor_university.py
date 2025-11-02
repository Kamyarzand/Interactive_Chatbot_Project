#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import logging
from task27 import UniversityTemperatureMonitor

logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('university_output.log')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger.addHandler(console_handler)

monitor = UniversityTemperatureMonitor()
locations = monitor.locations.keys()

print("Starting temperature monitoring...")
print(f"Monitoring locations: {list(locations)}")

while True:
    try:
        for location_id in locations:
            if monitor.record_temperature(location_id):
                info = monitor.get_location_info(location_id)
                if info:
                    temp = monitor.get_ambient_temperature()
                    message = (
                        f"Location: {info['name']}\n"
                        f"Current Temperature: {temp}Â°C\n"
                        f"Working Hours: {info['working_hours']['start']} to {info['working_hours']['end']}"
                    )
                    print("\n" + message + "\n")
                    logging.info(message)
        time.sleep(1800)  # 30 minutes
    except Exception as e:
        error_msg = f"Error in monitoring loop: {str(e)}"
        print("\n" + error_msg + "\n")
        logging.error(error_msg)
        time.sleep(1800)
