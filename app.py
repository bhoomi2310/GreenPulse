import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import os
import sys

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from utils.sensor_simulator import SensorSimulator
from utils.model_utils import MossHealthPredictor
from utils.data_generator import HistoricalDataGenerator

# Page configuration
st.set_page_config(
    page_title="AI-Powered Moss Wall Monitor",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'sensor_simulator' not in st.session_state:
    st.session_state.sensor_simulator = SensorSimulator()
if 'predictor' not in st.session_state:
    st.session_state.predictor = MossHealthPredictor()
if 'historical_generator' not in st.session_state:
    st.session_state.historical_generator = HistoricalDataGenerator()
if 'locations' not in st.session_state:
    st.session_state.locations = [
        "Building A - Lobby", "Building B - Facade", "Highway Wall - Section 1", 
        "University Campus - Library", "Corporate HQ - Conference Room"
    ]
if 'selected_location' not in st.session_state:
    st.session_state.selected_location = st.session_state.locations[0]

# Main title and header
st.title("🌿 AI-Powered Moss Wall Monitoring System")
st.markdown("**Real-time monitoring and automated maintenance for sustainable green infrastructure**")

# Sidebar controls
with st.sidebar:
    st.header("🏢 Location Selection")
    selected_location = st.selectbox(
        "Choose monitoring location:",
        st.session_state.locations,
        index=st.session_state.locations.index(st.session_state.selected_location)
    )
    st.session_state.selected_location = selected_location
    
    st.header("⚙️ System Controls")
    auto_refresh = st.checkbox("Auto-refresh data", value=True)
    refresh_interval = st.slider("Refresh interval (seconds)", 5, 60, 10)
    
    st.header("📊 Data Export")
    if st.button("Export Current Data"):
        current_data = st.session_state.sensor_simulator.get_current_readings(selected_location)
        st.download_button(
            label="Download CSV",
            data=pd.DataFrame([current_data]).to_csv(index=False),
            file_name=f"moss_data_{selected_location.replace(' ', '_')}.csv",
            mime="text/csv"
        )
    
    st.header("ℹ️ About")
    st.markdown("""
    **Benefits of Moss Walls:**
    - Air purification & CO₂ absorption
    - Natural insulation & temperature regulation
    - Urban heat island reduction
    - Biodiversity enhancement
    - Aesthetic green architecture
    """)

# Auto-refresh mechanism
if auto_refresh:
    placeholder = st.empty()
    with placeholder.container():
        # Get current sensor readings
        current_data = st.session_state.sensor_simulator.get_current_readings(selected_location)
        
        # Make prediction
        prediction, confidence, health_score = st.session_state.predictor.predict_health(
            current_data['humidity'], current_data['light'], current_data['moisture']
        )
        
        # Main dashboard layout
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="💧 Humidity",
                value=f"{current_data['humidity']:.1f}%",
                delta=f"{current_data['humidity'] - 65:.1f}%" if current_data['humidity'] != 65 else None
            )
        
        with col2:
            st.metric(
                label="☀️ Light Intensity",
                value=f"{current_data['light']:.0f} lux",
                delta=f"{current_data['light'] - 500:.0f}" if current_data['light'] != 500 else None
            )
        
        with col3:
            st.metric(
                label="🌱 Soil Moisture",
                value=f"{current_data['moisture']:.0f}",
                delta=f"{current_data['moisture'] - 600:.0f}" if current_data['moisture'] != 600 else None
            )
        
        with col4:
            st.metric(
                label="🌿 Health Score",
                value=f"{health_score:.1f}/10",
                delta=f"{health_score - 7.5:.1f}" if health_score != 7.5 else None
            )
        
        # Health status and predictions
        st.header("🤖 AI Health Analysis")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Health status indicator
            status_colors = {
                'Healthy': 'green',
                'Needs Water': 'orange',
                'Needs Shade': 'red',
                'Needs Attention': 'purple'
            }
            
            st.markdown(f"""
            <div style="padding: 20px; border-radius: 10px; background-color: {status_colors.get(prediction, 'gray')}20; border-left: 5px solid {status_colors.get(prediction, 'gray')};">
                <h3 style="color: {status_colors.get(prediction, 'gray')}; margin: 0;">Status: {prediction}</h3>
                <p style="margin: 5px 0;">Confidence: {confidence:.1f}%</p>
                <p style="margin: 5px 0;">Health Score: {health_score:.1f}/10</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Maintenance recommendations
            st.subheader("🔧 Maintenance Actions")
            recommendations = st.session_state.predictor.get_recommendations(prediction, current_data)
            for rec in recommendations:
                st.write(f"• {rec}")
        
        # Real-time sensor charts
        st.header("📈 Real-time Sensor Data")
        
        # Generate historical data for charts
        historical_data = st.session_state.historical_generator.generate_historical_data()
        
        # Create subplots for sensor data
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Humidity (%)', 'Light Intensity (lux)', 'Soil Moisture', 'CO₂ Levels (ppm)'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Add traces
        fig.add_trace(
            go.Scatter(x=historical_data['timestamp'], y=historical_data['humidity'],
                      mode='lines', name='Humidity', line=dict(color='blue')),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=historical_data['timestamp'], y=historical_data['light'],
                      mode='lines', name='Light', line=dict(color='orange')),
            row=1, col=2
        )
        
        fig.add_trace(
            go.Scatter(x=historical_data['timestamp'], y=historical_data['moisture'],
                      mode='lines', name='Moisture', line=dict(color='green')),
            row=2, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=historical_data['timestamp'], y=historical_data['co2'],
                      mode='lines', name='CO₂', line=dict(color='red')),
            row=2, col=2
        )
        
        fig.update_layout(height=600, showlegend=False, title_text="Live Sensor Monitoring")
        st.plotly_chart(fig, use_container_width=True)
        
        # Health trends over time
        st.header("📊 Health Trends & Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Health score trend
            health_scores = [st.session_state.predictor.calculate_health_score(row['humidity'], row['light'], row['moisture']) 
                           for _, row in historical_data.iterrows()]
            
            fig_health = go.Figure()
            fig_health.add_trace(go.Scatter(
                x=historical_data['timestamp'],
                y=health_scores,
                mode='lines+markers',
                name='Health Score',
                line=dict(color='green', width=3)
            ))
            fig_health.update_layout(
                title="Moss Health Score Trend",
                xaxis_title="Time",
                yaxis_title="Health Score (0-10)",
                yaxis=dict(range=[0, 10])
            )
            st.plotly_chart(fig_health, use_container_width=True)
        
        with col2:
            # Prediction distribution
            predictions_sample = []
            for _, row in historical_data.iterrows():
                pred, _, _ = st.session_state.predictor.predict_health(row['humidity'], row['light'], row['moisture'])
                predictions_sample.append(pred)
            
            pred_counts = pd.Series(predictions_sample).value_counts()
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=pred_counts.index,
                values=pred_counts.values,
                hole=0.3,
                marker_colors=['green', 'orange', 'red', 'purple']
            )])
            fig_pie.update_layout(title="Health Status Distribution (24h)")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Automation status
        st.header("🤖 Automated Maintenance System")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader("💧 Water System")
            water_status = "Active" if prediction == "Needs Water" else "Standby"
            st.write(f"Status: **{water_status}**")
            if prediction == "Needs Water":
                st.success("🚿 Misting system activated")
            else:
                st.info("💤 System on standby")
        
        with col2:
            st.subheader("🌡️ Climate Control")
            climate_status = "Active" if prediction == "Needs Shade" else "Normal"
            st.write(f"Status: **{climate_status}**")
            if prediction == "Needs Shade":
                st.warning("🌬️ Ventilation system activated")
            else:
                st.info("✅ Climate optimal")
        
        with col3:
            st.subheader("🚨 Alert System")
            alert_status = "Alert" if prediction == "Needs Attention" else "Normal"
            st.write(f"Status: **{alert_status}**")
            if prediction == "Needs Attention":
                st.error("🚨 Maintenance team notified")
            else:
                st.success("✅ All systems normal")
        
        # Environmental impact metrics
        st.header("🌍 Environmental Impact")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            co2_absorbed = current_data.get('co2_absorption', np.random.uniform(15, 25))
            st.metric("CO₂ Absorbed Today", f"{co2_absorbed:.1f} kg", "↑ 2.3 kg")
        
        with col2:
            air_purified = np.random.uniform(500, 800)
            st.metric("Air Purified", f"{air_purified:.0f} m³", "↑ 50 m³")
        
        with col3:
            energy_saved = np.random.uniform(25, 40)
            st.metric("Energy Saved", f"{energy_saved:.1f} kWh", "↑ 3.2 kWh")
        
        with col4:
            water_efficiency = np.random.uniform(85, 95)
            st.metric("Water Efficiency", f"{water_efficiency:.1f}%", "↑ 2.1%")

    # Auto-refresh
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

else:
    st.info("Auto-refresh is disabled. Enable it in the sidebar to see live data.")
    if st.button("Manual Refresh"):
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>🌿 AI-Powered Moss Wall Monitoring System | Sustainable Green Infrastructure | Real-time IoT Analytics</p>
    <p>Supporting smart cities, green buildings, and environmental sustainability</p>
</div>
""", unsafe_allow_html=True)
