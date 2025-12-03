import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Tyre Market Analysis", layout="wide")

# --- HEADER ---
st.title("🚗 Tyre Market Consumer Behavior Analysis")
st.subheader("Region: North Kerala (Kannur District)")
st.markdown("""
> **⚠️ Project Disclaimer:** This dashboard uses a **synthetic dataset** generated via Python (NumPy) 
> to simulate local market trends. It demonstrates the analytical pipeline but does not represent real survey results.
""")

# --- LOAD DATA ---
@st.cache_data
def get_data():
    return pd.read_csv("kerala_tyre_data.csv")

df = get_data()

# ==============================================
# --- SIDEBAR FILTERS (MODIFIED TO CHECKBOXES) ---
# ==============================================
st.sidebar.header("🔍 Filter Data")

# --- 1. TOWN FILTER (Checkboxes) ---
st.sidebar.subheader("📍 Select Towns")
town_list = df['Town'].unique()
selected_towns = []

# Create a checkbox for every town found in the data
# We set value=True so they are checked by default when the page loads
for town in town_list:
    if st.sidebar.checkbox(town, value=True, key=town):
        selected_towns.append(town)

# --- 2. VEHICLE FILTER (Checkboxes) ---
st.sidebar.divider() # Adds a visual line separator
st.sidebar.subheader("🛵 Select Vehicle Types")
vehicle_list = df['Vehicle_Type'].unique()
selected_vehicles = []

for vehicle in vehicle_list:
    if st.sidebar.checkbox(vehicle, value=True, key=vehicle):
        selected_vehicles.append(vehicle)

# ==============================================
# --- APPLY FILTERS ---
# ==============================================

# Check if lists are empty (User uncurled everything) to prevent errors
if not selected_towns or not selected_vehicles:
    st.error("Please select at least one Town and one Vehicle Type to view analysis.")
    st.stop() # Stops the code here so charts don't break

filtered_df = df[
    (df['Town'].isin(selected_towns)) & 
    (df['Vehicle_Type'].isin(selected_vehicles))
]

# --- KEY METRICS (KPIs) ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Respondents", len(filtered_df))
# Handle case where filtered data might be empty
if not filtered_df.empty:
    mode_val = filtered_df['Current_Brand'].mode()
    popular_brand = mode_val[0] if not mode_val.empty else "N/A"
    col2.metric("Most Popular Brand", popular_brand)
    col3.metric("Avg. Satisfaction Score", f"{filtered_df['Satisfaction_Score'].mean():.1f} / 10")
else:
    col2.metric("Most Popular Brand", "-")
    col3.metric("Avg. Satisfaction Score", "-")

st.divider()

# --- VISUALIZATIONS ---

if not filtered_df.empty:
    # ROW 1
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("🏆 Market Share by Brand")
        fig_pie = px.pie(filtered_df, names='Current_Brand', hole=0.4, 
                         color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        st.subheader("🤔 Why do people buy?")
        fig_bar = px.histogram(filtered_df, x='Current_Brand', color='Purchase_Factor', 
                            barmode='group', title="Buying Factors per Brand")
        st.plotly_chart(fig_bar, use_container_width=True)

    # ROW 2
    st.subheader("💰 Price Sensitivity Analysis")
    fig_box = px.box(filtered_df, x='Current_Brand', y='Price_Paid', color='Current_Brand',
                    title="How much are people paying for each brand?")
    st.plotly_chart(fig_box, use_container_width=True)
