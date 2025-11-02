#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import logging
from datetime import datetime, timedelta
from random import uniform

class UniversityTemperatureMonitor:
    def __init__(self):
        self.base_path = "/home/dtuser/chatbot/tasks"
        self.locations_file = os.path.join(self.base_path, "locations.json")
        self.readings_file = os.path.join(self.base_path, "temperature_readings.json")
        self.setup_logging()
        self.locations = self.load_locations()
        self.readings = self.load_readings()

    def setup_logging(self):
        logging.basicConfig(
            filename='university_temp.log',
            level=logging.INFO,
            format='%(asctime)s - %(message)s'
        )

    def get_ambient_temperature(self):
        try:
            temp = os.popen("vcgencmd measure_temp").readline()
            cpu_temp = float(temp.replace("temp=", "").replace("'C\n", ""))
            ambient_temp = cpu_temp - 30
            return round(ambient_temp, 2)
        except Exception as e:
            logging.error(f"Error getting temperature: {e}")
            return None

    def record_temperature(self, location_id):
        try:
            temp = self.get_ambient_temperature()
            if temp is None:
                return False
            
            if location_id not in self.readings:
                self.readings[location_id] = []
                
            self.readings[location_id].append({
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'temperature': temp
            })
            
            with open(self.readings_file, 'w') as f:
                json.dump(self.readings, f)
                
            return True
        except Exception as e:
            logging.error(f"Error: {e}")
            return False

    def load_locations(self):
        try:
            with open(self.locations_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def load_readings(self):
        try:
            with open(self.readings_file, 'r') as f:
                return json.load(f)
        except Exception:
            return {}

    def get_location_info(self, location_id):
        if location_id not in self.locations:
            return None
        location = self.locations[location_id]
        return {
            'name': location['name'],
            'type': location['type'],
            'working_hours': location['working_hours']
        }
