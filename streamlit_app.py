import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

def calculate_weekly_emissions(emissions_total, decay_percent):
    weeks = np.arange(1, 101)  # Simulating 100 weeks
    weekly_emissions = (1 / (decay_percent / 100)) ** (-1) * emissions_total
    emissions_values = [weekly_emissions * ((1 - decay_percent / 100) ** week) for week in weeks]
    return weeks, emissions_values

def main():
    st.title("Token Supply Distribution")
    
    st.sidebar.header("Initial Supply Input")
    
    categories = [
        "Liquidity Providers", "Incentives", "Ecosystem", "Treasury (Future Development)",
        "Fund Raising", "Seed Round", "Bridge Round", "Private Round", "Public Round", "Future Raise", "Team & Advisors"
    ]
    
    initial_values = [
        12_500_000, 23_000_000, 4_305_556, 14_000_000, 10_000_000,
        2_200_000, 1_666_667, 5_694_444, 3_333_333, 23_300_000
    ]
    
    total_supply = sum(initial_values)  # Ensure total supply matches
    category_supply = {categories[i]: initial_values[i] for i in range(len(categories))}
    
    st.sidebar.header("Emissions")
    emissions_total = st.sidebar.number_input("Emissions Total", min_value=0.0, value=200_000_000.0, step=1_000_000.0)
    emissions_decay = st.sidebar.slider("Emissions Decay (Weekly %)", min_value=1, max_value=5, value=3)
    
    # Create DataFrame
    data = pd.DataFrame({
        "Category": list(category_supply.keys()),
        "Amount": list(category_supply.values())
    })
    
    # Display the DataFrame
    st.write("### Initial Supply Breakdown", data)
    
    # Display a Pie Chart
    fig = px.pie(data, names='Category', values='Amount', title="Token Supply Distribution")
    st.plotly_chart(fig)
    
    # Calculate and plot weekly emissions
    weeks, emissions_values = calculate_weekly_emissions(emissions_total, emissions_decay)
    fig_emissions = go.Figure()
    fig_emissions.add_trace(go.Scatter(x=weeks, y=emissions_values, mode='lines', name='Weekly Emissions'))
    fig_emissions.update_layout(title="Emissions Over Time", xaxis_title="Week", yaxis_title="Emissions")
    st.plotly_chart(fig_emissions)
    
    # Display Emissions Data
    st.write("### Emissions")
    st.write(f"Total Emissions: {emissions_total}")
    st.write(f"Decay Rate: {emissions_decay}% per week")
    
if __name__ == "__main__":
    main()
