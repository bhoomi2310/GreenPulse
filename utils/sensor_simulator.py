import numpy as np
import time
from datetime import datetime

class SensorSimulator:
    """Simulates IoT sensor readings for moss wall monitoring"""
    
    def __init__(self):
        self.base_values = {
            'humidity': 65,
            'light': 500,
            'moisture': 600,
            'co2': 400,
            'temperature': 22
        }
        self.last_update = time.time()
    
    def get_current_readings(self, location):
        """Generate realistic sensor readings with time-based variations"""
        current_time = datetime.now()
        time_factor = np.sin(current_time.hour * np.pi / 12)  # Daily cycle
        
        # Location-specific adjustments
        location_factors = {
            'Building A - Lobby': {'humidity': 0, 'light': 0.8, 'moisture': 0},
            'Building B - Facade': {'humidity': 0.1, 'light': 1.2, 'moisture': -0.1},
            'Highway Wall - Section 1': {'humidity': -0.1, 'light': 1.5, 'moisture': -0.2},
            'University Campus - Library': {'humidity': 0.05, 'light': 0.6, 'moisture': 0.1},
            'Corporate HQ - Conference Room': {'humidity': -0.05, 'light': 0.7, 'moisture': 0.05}
        }
        
        factor = location_factors.get(location, {'humidity': 0, 'light': 1, 'moisture': 0})
        
        # Generate readings with realistic variations
        readings = {
            'humidity': max(20, min(95, self.base_values['humidity'] + 
                          np.random.normal(0, 5) + time_factor * 10 + factor['humidity'] * 20)),
            'light': max(50, min(1500, self.base_values['light'] + 
                        np.random.normal(0, 50) + time_factor * 300 * factor['light'])),
            'moisture': max(200, min(900, self.base_values['moisture'] + 
                           np.random.normal(0, 30) + factor['moisture'] * 100)),
            'co2': max(300, min(600, self.base_values['co2'] + 
                      np.random.normal(0, 20) - time_factor * 50)),
            'temperature': max(15, min(35, self.base_values['temperature'] + 
                             np.random.normal(0, 2) + time_factor * 5)),
            'timestamp': current_time,
            'location': location
        }
        
        # Add CO₂ absorption calculation
        moss_efficiency = min(1.0, readings['humidity'] / 100 * readings['moisture'] / 700)
        readings['co2_absorption'] = moss_efficiency * np.random.uniform(15, 25)
        
        return readings
    
    def simulate_sensor_failure(self, sensor_type, probability=0.05):
        """Simulate occasional sensor failures"""
        if np.random.random() < probability:
            return None  # Sensor failure
        return True
