# Overview

This is an AI-Powered Moss Wall Monitoring System built with Streamlit that provides real-time monitoring and automated maintenance for sustainable green infrastructure. The application simulates IoT sensor networks that monitor moss-covered concrete walls in various locations (buildings, highways, campuses) and uses machine learning to predict moss health conditions and maintenance needs.

The system combines environmental monitoring (humidity, light, moisture, CO₂, temperature) with AI-driven predictions to optimize moss wall maintenance, reduce water consumption, and ensure healthy moss growth for pollution mitigation and aesthetic purposes.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit web application with real-time dashboard interface
- **Visualization**: Plotly Express and Graph Objects for interactive charts and real-time data visualization
- **Layout**: Wide layout with expandable sidebar for location selection and controls
- **State Management**: Streamlit session state to maintain sensor simulators, ML models, and user selections across interactions

## Backend Architecture
- **Sensor Simulation**: Custom `SensorSimulator` class that generates realistic IoT sensor readings with time-based variations and location-specific adjustments
- **ML Pipeline**: `MossHealthPredictor` using scikit-learn Decision Tree classifier with rule-based fallback system
- **Data Generation**: `HistoricalDataGenerator` creates 24-hour historical data with realistic patterns including daily cycles, watering events, and maintenance activities
- **Modular Design**: Utility classes separated into `/utils` directory for sensor simulation, model operations, and data generation

## Data Architecture
- **Real-time Data**: In-memory pandas DataFrames for current sensor readings and historical data
- **Data Models**: Structured sensor data including humidity, light intensity, moisture levels, CO₂ concentration, and temperature
- **Time Series**: 15-minute interval data points with timestamp indexing for trend analysis
- **Location-based Data**: Multi-location monitoring with location-specific environmental factors and adjustments

## ML Model Architecture
- **Algorithm**: Decision Tree Classifier with synthetic training data generation
- **Features**: 3-dimensional feature space (humidity, light, moisture) for health prediction
- **Classes**: 4-class classification system (Healthy, Needs Water, Needs Shade, Needs Attention)
- **Fallback System**: Rule-based model creation when pre-trained model file is unavailable
- **Model Persistence**: Pickle-based model serialization for trained model storage

# External Dependencies

## Python Libraries
- **streamlit**: Web application framework for dashboard interface
- **plotly**: Interactive visualization library for charts and graphs
- **pandas**: Data manipulation and analysis for sensor data handling
- **numpy**: Numerical computing for sensor simulation and data generation
- **scikit-learn**: Machine learning library for moss health prediction model
- **pickle**: Python serialization for model persistence

## Potential IoT Integration Points
- **ESP32/Arduino**: Microcontroller integration for actual sensor hardware
- **Raspberry Pi**: Local AI model deployment for edge computing
- **MQTT/HTTP APIs**: Communication protocols for real sensor data ingestion
- **Time Series Databases**: InfluxDB or similar for production sensor data storage

## System Integration Capabilities
- **Smart Building Systems**: Integration with building automation and HVAC systems
- **Automated Irrigation**: Connection to misting pumps and water management systems
- **Alert Systems**: LED indicators and notification systems for maintenance teams
- **Cloud Platforms**: Deployment capability for AWS/Azure/GCP cloud infrastructure