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

def distribute_remaining(categories, percentages, changed_category, new_value):
    total_remaining = 100 - new_value
    other_categories = [cat for cat in categories if cat != changed_category]
    current_total = sum(percentages[cat] for cat in other_categories)
    
    if current_total == 0:
        for cat in other_categories:
            percentages[cat] = total_remaining / len(other_categories)
    else:
        for cat in other_categories:
            percentages[cat] = (percentages[cat] / current_total) * total_remaining
    
    percentages[changed_category] = new_value

def main():
    st.title("Token Supply Distribution")
    
    st.sidebar.header("Initial Supply Input")
    
    categories = [
        "Treasury (Future Development)", "Team & Advisors", "Liquidity Providers", "Incentives", 
        "Ecosystem", "Fund Raising", "Seed Round", "Bridge Round", "Private Round", "Public Round"
    ]
    
    total_supply = 100_000_000  # Fixed total initial supply
    initial_percentages = [14.56, 23.30, 12.50, 23.00, 6.11, 21.09, 10.00, 2.20, 3.33, 5.00]
    normalized_percentages = [p / sum(initial_percentages) * 100 for p in initial_percentages]
    category_percentages = {cat: normalized_percentages[i] for i, cat in enumerate(categories)}
    
    changed_category = st.sidebar.selectbox("Select category to adjust", categories)
    new_value = st.sidebar.slider(f"{changed_category} (%)", min_value=0.0, max_value=100.0, value=category_percentages[changed_category])
    
    distribute_remaining(categories, category_percentages, changed_category, new_value)
    
    st.sidebar.header("Emissions")
    emissions_total = st.sidebar.number_input("Emissions Total", min_value=0.0, value=200_000_000.0, step=1_000_000.0)
    emissions_decay = st.sidebar.slider("Emissions Decay (Weekly %)", min_value=1, max_value=5, value=3)
    
    # Calculate absolute values for categories
    initial_supply = {cat: (percent / 100) * total_supply for cat, percent in category_percentages.items()}
    
    # Create DataFrame
    data = pd.DataFrame({
        "Category": list(initial_supply.keys()),
        "Amount": list(initial_supply.values())
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

