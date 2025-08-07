import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class HistoricalDataGenerator:
    """Generates realistic historical data for visualization"""
    
    def __init__(self):
        self.hours_back = 24
    
    def generate_historical_data(self):
        """Generate 24 hours of historical sensor data"""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=self.hours_back)
        
        # Generate timestamps (one reading every 15 minutes)
        timestamps = pd.date_range(start=start_time, end=end_time, freq='15T')
        
        data = []
        for i, timestamp in enumerate(timestamps):
            # Time-based variations
            hour = timestamp.hour
            time_factor = np.sin(hour * np.pi / 12)  # Daily cycle
            
            # Base values with realistic variations
            humidity = 65 + np.random.normal(0, 8) + time_factor * 15
            light = 500 + np.random.normal(0, 100) + time_factor * 400
            moisture = 600 + np.random.normal(0, 50) + np.random.uniform(-20, 20)
            co2 = 400 + np.random.normal(0, 30) - time_factor * 80
            temperature = 22 + np.random.normal(0, 3) + time_factor * 6
            
            # Add some realistic events (watering, maintenance, etc.)
            if hour in [6, 18]:  # Watering times
                moisture += np.random.uniform(50, 100)
                humidity += np.random.uniform(10, 20)
            
            if hour in [12, 13, 14]:  # Peak sunlight
                light *= np.random.uniform(1.2, 1.8)
                temperature += np.random.uniform(2, 5)
            
            # Ensure realistic bounds
            humidity = max(20, min(95, humidity))
            light = max(50, min(1500, light))
            moisture = max(200, min(900, moisture))
            co2 = max(300, min(600, co2))
            temperature = max(15, min(35, temperature))
            
            data.append({
                'timestamp': timestamp,
                'humidity': humidity,
                'light': light,
                'moisture': moisture,
                'co2': co2,
                'temperature': temperature
            })
        
        return pd.DataFrame(data)
    
    def generate_weekly_summary(self):
        """Generate weekly summary statistics"""
        # This could be expanded for weekly/monthly views
        daily_data = []
        for day in range(7):
            date = datetime.now() - timedelta(days=day)
            daily_data.append({
                'date': date.date(),
                'avg_humidity': np.random.uniform(60, 75),
                'avg_light': np.random.uniform(400, 600),
                'avg_moisture': np.random.uniform(550, 700),
                'health_events': np.random.randint(0, 3)
            })
        
        return pd.DataFrame(daily_data)

