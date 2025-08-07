import pickle
import numpy as np
import os

class MossHealthPredictor:
    """Handles moss health predictions using the trained model"""
    
    def __init__(self):
        self.model = None
        self.labels = ['Healthy', 'Needs Water', 'Needs Shade', 'Needs Attention']
        self.load_model()
    
    def load_model(self):
        """Load the pre-trained moss health model"""
        try:
            model_path = "moss_health_model.pkl"
            if not os.path.exists(model_path):
                # Create a simple model if file doesn't exist
                self.create_fallback_model()
            else:
                with open(model_path, "rb") as file:
                    self.model = pickle.load(file)
        except Exception as e:
            print(f"Error loading model: {e}")
            self.create_fallback_model()
    
    def create_fallback_model(self):
        """Create a simple rule-based fallback model"""
        from sklearn.tree import DecisionTreeClassifier
        
        # Generate synthetic training data
        np.random.seed(42)
        n_samples = 500
        
        humidity = np.random.uniform(20, 95, n_samples)
        light = np.random.uniform(100, 1500, n_samples)
        moisture = np.random.uniform(200, 900, n_samples)
        
        labels = []
        for h, l, m in zip(humidity, light, moisture):
            if h >= 60 and h <= 80 and l >= 300 and l <= 800 and m >= 500 and m <= 750:
                labels.append(0)  # Healthy
            elif m < 400:
                labels.append(1)  # Needs Water
            elif l > 1000 or h < 40:
                labels.append(2)  # Needs Shade
            else:
                labels.append(3)  # Needs Attention
        
        X = np.column_stack([humidity, light, moisture])
        y = np.array(labels)
        
        self.model = DecisionTreeClassifier(random_state=42, max_depth=10)
        self.model.fit(X, y)
        
        # Save the fallback model
        with open("moss_health_model.pkl", "wb") as file:
            pickle.dump(self.model, file)
    
    def predict_health(self, humidity, light, moisture):
        """Predict moss health status"""
        try:
            data = np.array([[humidity, light, moisture]])
            prediction = self.model.predict(data)[0]
            
            # Calculate prediction confidence using decision function or probability
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(data)[0]
                confidence = np.max(probabilities) * 100
            else:
                # Fallback confidence calculation
                confidence = self.calculate_confidence(humidity, light, moisture, prediction)
            
            # Calculate health score
            health_score = self.calculate_health_score(humidity, light, moisture)
            
            return self.labels[prediction], confidence, health_score
        
        except Exception as e:
            print(f"Prediction error: {e}")
            return "Unknown", 0.0, 0.0
    
    def calculate_confidence(self, humidity, light, moisture, prediction):
        """Calculate prediction confidence based on ideal conditions"""
        ideal_conditions = {
            0: {'humidity': 70, 'light': 500, 'moisture': 650},  # Healthy
            1: {'humidity': 50, 'light': 400, 'moisture': 300},  # Needs Water
            2: {'humidity': 35, 'light': 1200, 'moisture': 500}, # Needs Shade
            3: {'humidity': 45, 'light': 900, 'moisture': 400}   # Needs Attention
        }
        
        ideal = ideal_conditions[prediction]
        
        # Calculate distance from ideal conditions
        h_diff = abs(humidity - ideal['humidity']) / 100
        l_diff = abs(light - ideal['light']) / 1500
        m_diff = abs(moisture - ideal['moisture']) / 900
        
        distance = np.sqrt(h_diff**2 + l_diff**2 + m_diff**2)
        confidence = max(50, 100 - distance * 200)  # Scale to 50-100%
        
        return confidence
    
    def calculate_health_score(self, humidity, light, moisture):
        """Calculate overall health score (0-10)"""
        # Optimal ranges
        humidity_score = 1 - abs(humidity - 70) / 50  # Optimal at 70%
        light_score = 1 - abs(light - 500) / 700     # Optimal at 500 lux
        moisture_score = 1 - abs(moisture - 650) / 450  # Optimal at 650
        
        # Ensure scores are between 0 and 1
        humidity_score = max(0, min(1, humidity_score))
        light_score = max(0, min(1, light_score))
        moisture_score = max(0, min(1, moisture_score))
        
        # Weighted average (moisture is most important)
        health_score = (humidity_score * 0.3 + light_score * 0.3 + moisture_score * 0.4) * 10
        
        return max(0, min(10, health_score))
    
    def get_recommendations(self, prediction, sensor_data):
        """Get maintenance recommendations based on prediction"""
        recommendations = []
        
        if prediction == "Needs Water":
            recommendations.extend([
                "Activate automatic misting system",
                "Check water reservoir levels",
                "Verify sprinkler system functionality",
                f"Current moisture: {sensor_data['moisture']:.0f} (target: 600-750)"
            ])
        
        elif prediction == "Needs Shade":
            recommendations.extend([
                "Adjust building ventilation",
                "Consider temporary shading solutions",
                "Check air conditioning efficiency",
                f"Current light: {sensor_data['light']:.0f} lux (optimal: 300-800)"
            ])
        
        elif prediction == "Needs Attention":
            recommendations.extend([
                "Schedule maintenance inspection",
                "Check all sensor calibrations",
                "Examine moss growth patterns",
                "Review environmental control systems"
            ])
        
        else:  # Healthy
            recommendations.extend([
                "Continue current maintenance schedule",
                "Monitor sensor readings",
                "System operating optimally"
            ])
        
        return recommendations
