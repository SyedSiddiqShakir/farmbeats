import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# --- CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="FarmBeats Prototype",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- DARK MODE CSS STYLING ---
st.markdown("""
    <style>
        /* 1. Main Background - Deep Dark Blue/Black */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        
        /* 2. Sidebar Background - Slightly lighter dark */
        [data-testid="stSidebar"] {
            background-color: #161B22;
            border-right: 1px solid #30363D;
        }

        /* 3. Metric Cards (The boxes with numbers) */
        div[data-testid="metric-container"] {
            background-color: #21262D;
            border: 1px solid #30363D;
            padding: 15px;
            border-radius: 8px;
            color: #ffffff;
        }
        
        /* 4. Text Coloring inside Metrics */
        [data-testid="stMetricLabel"] {
            color: #8B949E; /* Dimmed gray for labels */
        }
        [data-testid="stMetricValue"] {
            color: #FFFFFF; /* Bright white for values */
        }
        
        /* 5. Headers & Titles */
        h1, h2, h3 {
            color: #4CAF50 !important; /* FarmBeats Green */
        }
        
        /* 6. Expander/Dropdown backgrounds */
        .streamlit-expanderHeader {
            background-color: #21262D;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---

def get_weather_impact(weather):
    """Returns solar input and battery impact based on weather."""
    if weather == "Sunny":
        return 94, "200Wh/day", "Normal"
    elif weather == "Cloudy":
        return 65, "140Wh/day", "Conservation Mode"
    else: # Storm
        return 28, "10Wh/day", "Deep Sleep"

# --- PAGE 1: EXECUTIVE DASHBOARD ---
def show_dashboard():
    st.title("Farm Monitor")
    st.caption("📍 Zwickau Farm")

    # Weather Control Simulation
    with st.expander("Simulation Controls (Demo)", expanded=True):
        weather_state = st.selectbox("Simulate Weather Condition", ["Sunny", "Cloudy", "Storm"])
        batt_level, solar_input, mode = get_weather_impact(weather_state)
    
    st.markdown("### System Status")
    
    # Top Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Connectivity (TVWS)", "Strong", "470 MHz", help="Using TV White Spaces for long range ")
    with col2:
        st.metric("Solar Battery", f"{batt_level}%", solar_input, help="Solar-powered edge devices")
    with col3:
        st.metric("Active Sensors", "12 / 100", "-88% count", help="80% fewer sensors needed due to AI Fusion")
    with col4:
        st.metric("System Mode", mode, "Active")

    st.markdown("---")

    # Main Content Split
    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("🔋 Live Battery Performance")
        # Fake historical data based on weather
        hours = list(range(24))
        if weather_state == "Sunny":
            energy = [50 + (x * 2) if x < 12 else 74 - (x * 0.5) for x in hours]
        else:
            energy = [60 - (x * 1.5) for x in hours]
        
        # Plotly Chart with DARK Template
        fig = px.area(x=hours, y=energy, labels={'x': 'Hour of Day', 'y': 'Battery %'})
        fig.update_layout(
            title="24-Hour Energy Profile",
            template="plotly_dark",  # <--- CRITICAL FOR DARK MODE
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=300,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        fig.update_traces(line_color='#4CAF50', fillcolor='rgba(76, 175, 80, 0.3)')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("Notifications")
        alerts = [
            {"emoji": " ", "msg": "Zone B needs water", "time": "10m ago"},
            {"emoji": " ", "msg": "Pest risk high (Sector 3)", "time": "2h ago"},
            {"emoji": " ", "msg": "Cow herd movement detected", "time": "5h ago"},
        ]
        for a in alerts:
            # Styled warning boxes
            st.warning(f"{a['emoji']} **{a['msg']}** \n\n *{a['time']}*")

# --- PAGE 2: DRONE FLIGHT PLANNER ---
def show_drone_planner():
    st.title("🚁 Drone Path Planner")
    st.markdown("Use **Wind-Assisted Path Planning** to save battery.")

    c1, c2 = st.columns([1, 3])
    
    with c1:
        st.write("### Flight Settings")
        st.slider("Flight Altitude", 10, 50, 30, format="%d m")
        wind_dir = st.selectbox("Wind Direction", ["North", "East", "South", "West"])
        st.info(f"Using **{wind_dir}** wind to accelerate/decelerate drone.")
        
        if st.button("Calculate Optimal Path"):
            with st.spinner("Calculating Min-Waypoint Path..."):
                time.sleep(1.5)
            st.success("Path Optimized: 30% Battery Saving predicted.")

    with c2:
        st.write("### Projected Coverage Path")
        
        # Mock coordinates for a zig-zag path
        lat = [10, 10, 40, 40, 10, 10, 40, 40]
        lon = [10, 20, 20, 30, 30, 40, 40, 50]
        
        fig = px.line(x=lon, y=lat, labels={'x':'Field Width', 'y':'Field Length'})
        fig.update_layout(
        title="Min-Waypoint Flight Pattern",
            template="plotly_dark", # <--- CRITICAL FOR DARK MODE
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        fig.update_traces(line=dict(color="#FF4B4B", width=4, dash='dot'))
        fig.add_annotation(x=25, y=25, text=f"Wind: {wind_dir} ➡️", showarrow=False, font=dict(size=20, color="cyan"))
        st.plotly_chart(fig, use_container_width=True)

# --- PAGE 3: SOIL ANALYTICS ---
def show_analytics():
    st.title("🧪 Precision Soil Analytics")
    st.markdown("Comparing **Traditional Sensors** vs **FarmBeats AI Fusion**.")

    # Generate Mock Data
    x_axis = np.linspace(0, 10, 20)
    ground_truth = np.sin(x_axis) + 2  # The real moisture curve
    sparse_sensors = [2, 2.8, 1.2, 2] # Only 4 sensors readings
    sparse_x = [0, 3, 6, 9]
    
    # Plotting
    fig = go.Figure()

    # 1. Ground Truth (The AI prediction)
    fig.add_trace(go.Scatter(x=x_axis, y=ground_truth, mode='lines', name='FarmBeats AI Prediction', 
                             line=dict(color='#4CAF50', width=4)))
    
    # 2. Sparse Sensors (Dots)
    fig.add_trace(go.Scatter(x=sparse_x, y=sparse_sensors, mode='markers', name='Physical Sensors',
                             marker=dict(color='#FF5252', size=12)))

    fig.update_layout(
        title="Soil Moisture Extrapolation",
        xaxis_title="Distance (meters)", 
        yaxis_title="Moisture Level (1-5)",
        template="plotly_dark", # <--- CRITICAL FOR DARK MODE
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        # Standard placeholder image for drone view
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Aerial_view_of_the_Rothschild_Wines_vineyards_at_Ramat_Hanadiv.jpg/640px-Aerial_view_of_the_Rothschild_Wines_vineyards_at_Ramat_Hanadiv.jpg", caption="Drone Visual Input", use_container_width=True)
    with col2:
        st.write("### Data Insights")
        st.markdown("""
        * **Fusion Model:** Combined video pixel data with the 4 red dots to generate the green line.
        * **Result:** Detected moisture drop at 6 meters that linear sensors missed. Interpolation of missing data
        * **Action:** Applied water specifically to Zone 6.
        """)
        st.button("Export Data")

# --- PAGE 4: FIELD MAP (UPGRADED) ---
def show_field_map():
    st.title("🗺️ Live Field Operations Map")
    st.markdown("Real-time status of defined field zones.")
    
    fig = go.Figure()

    # --- DEFINE CUSTOM FIELD SHAPES (POLYGONS) ---
    
    # Area 1: North Field (Healthy - Green)
    # Irregular polygon coordinates
    x1 = [10, 40, 60, 50, 20, 10]
    y1 = [60, 60, 80, 95, 95, 60]
    
    fig.add_trace(go.Scatter(
        x=x1, y=y1,
        fill="toself",
        mode="lines",
        line=dict(color="#4CAF50", width=2),
        fillcolor="rgba(76, 175, 80, 0.3)",
        name="North Field",
        hoverinfo="skip" # We will use text points for better hover control
    ))

    # Area 2: East Field (Warning - Yellow)
    x2 = [65, 95, 90, 65, 60]
    y2 = [50, 55, 90, 80, 50]
    
    fig.add_trace(go.Scatter(
        x=x2, y=y2,
        fill="toself",
        mode="lines",
        line=dict(color="#FFC107", width=2),
        fillcolor="rgba(255, 193, 7, 0.3)",
        name="East Field",
        hoverinfo="skip"
    ))

    # Area 3: South Field (Critical - Red)
    x3 = [10, 50, 95, 80, 15, 10]
    y3 = [10, 10, 45, 45, 40, 10]
    
    fig.add_trace(go.Scatter(
        x=x3, y=y3,
        fill="toself",
        mode="lines",
        line=dict(color="#FF5252", width=2),
        fillcolor="rgba(255, 82, 82, 0.3)",
        name="South Field",
        hoverinfo="skip"
    ))

    # --- ADD CONTEXTUAL ELEMENTS (Roads & Station) ---
    
    # Farm Road (Dashed Line)
    fig.add_trace(go.Scatter(
        x=[0, 100], y=[48, 48],
        mode="lines",
        line=dict(color="#666", width=4, dash="dash"),
        name="Farm Road",
        hoverinfo="skip"
    ))

    # Base Station Icon
    fig.add_trace(go.Scatter(
        x=[55], y=[48],
        mode="markers+text",
        marker=dict(symbol="star", size=18, color="cyan"),
        text=["<b>Base Station</b>"],
        textposition="bottom center",
        textfont=dict(color="cyan"),
        hoverinfo="text",
        hovertext="Connectivity Hub: 470 MHz Signal"
    ))

    # --- DATA POINTS (HOVER INFO) ---
    # We place these text labels in the "center" of each polygon
    
    cx = [35, 75, 50] # Center X for labels
    cy = [75, 70, 25] # Center Y for labels
    
    fig.add_trace(go.Scatter(
        x=cx, y=cy,
        text=["<b>North Field</b>", "<b>East Field</b>", "<b>South Field</b>"],
        mode="text",
        textfont=dict(color="white", size=14, family="Arial Black"),
        hoverinfo="text",
        hovertext=[
            # Data for Area 1
            "<b>Status:</b> 🟢 Optimal<br>" +
            "<b>Stock:</b> Corn (Gen 4)<br>" +
            "<b>Harvest:</b> 85% Ready<br>" +
            "<b>Moisture:</b> 42% (Good)<br>" +
            "<b>Wind:</b> 12 km/h NW<br>" +
            "<b>Sun:</b> High UV",
            
            # Data for Area 2
            "<b>Status:</b> 🟡 Warning<br>" +
            "<b>Stock:</b> Wheat<br>" +
            "<b>Harvest:</b> 40% Ready<br>" +
            "<b>Moisture:</b> 15% (Low)<br>" +
            "<b>Wind:</b> 10 km/h NW<br>" +
            "<b>Sun:</b> High UV",

            # Data for Area 3
            "<b>Status:</b> 🔴 Critical<br>" +
            "<b>Stock:</b> Fallow<br>" +
            "<b>Harvest:</b> N/A<br>" +
            "<b>Moisture:</b> 8% (Critical)<br>" +
            "<b>Wind:</b> 5 km/h N<br>" +
            "<b>Sun:</b> Moderate"
        ]
    ))

    # --- CHART LAYOUT ---
    fig.update_layout(
        template="plotly_dark",
        height=600,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 100]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 100]),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        dragmode="pan"
    )

    st.plotly_chart(fig, use_container_width=True)
    
    # Legend below map
    c1, c2, c3 = st.columns(3)
    c1.success("North Field: Healthy")
    c2.warning("East Field: Irrigation Needed")
    c3.error("South Field: Critical Dryness")

# --- MAIN APP LOGIC ---

# Sidebar Navigation
with st.sidebar:
    st.title("Explorer")
    st.markdown("---")
    
    # Navigation Menu
    page = st.radio("Navigate", ["Dashboard", "Field Map", "Drone Flight", "Soil Analytics"])
    
    st.markdown("---")
    st.caption("System Status")
    st.success("Cloud: Online")
    st.success("Gateway: Online")
    st.caption("v1.0 | WHZ")

# Page Routing
if page == "Dashboard":
    show_dashboard()
elif page == "Field Map":
    show_field_map()
elif page == "Drone Flight":
    show_drone_planner()
elif page == "Soil Analytics":

    show_analytics()
