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
        "Seed Round", "Bridge Round", "Private Round", "Public Round", "Future Raise", "Team & Advisors"
    ]
    
    initial_values = [
        12_500_000, 23_000_000, 4_305_556, 14_000_000,10_000_000,
        2_200_000, 1_666_667, 5_694_444, 3_333_333, 23_300_000
    ]
    
    tge_unlock = [
        2_778_000, 6_191_250, 733_333, 0,
        0, 0, 83_333, 5_694_444, 0, 0
    ]
    
    quarterly_unlock = [
        571_731, 988_489, 178_611, 0, 0, 0, 0, 0, 0, 0
    ]
    
    if len(categories) == len(initial_values) == len(tge_unlock) == len(quarterly_unlock):
        data = pd.DataFrame({
            "Category": categories,
            "Total Allocation": initial_values,
            "Initial Unlock at TGE": tge_unlock,
            "Quarterly Unlock": quarterly_unlock
        })
    else:
        st.error("Error: Mismatch in category and value lists. Please check data consistency.")
        return
    
    total_supply = sum(initial_values)  # Ensure total supply matches
    
    st.sidebar.header("Emissions")
    emissions_total = st.sidebar.number_input("Emissions Total", min_value=0.0, value=200_000_000.0, step=1_000_000.0)
    emissions_decay = st.sidebar.slider("Emissions Decay (Weekly %)", min_value=1, max_value=5, value=3)
    
    # Display the DataFrame
    st.write("### Initial Supply Breakdown")
    st.table(data)
    
    # Display a Pie Chart
    fig = px.pie(data, names='Category', values='Total Allocation', title="Token Supply Distribution")
    st.plotly_chart(fig)
    
    # Discussion about TGE
    st.write("## Token Generation Event (TGE)")
    st.write(
        "At the Token Generation Event (TGE), a portion of the total supply is initially unlocked to provide liquidity, incentives, and early participation rewards. "
        "The initial unlock values vary by category, ensuring a controlled release of tokens to the market."
    )
    
    # Mention monthly decay
    st.write("## Monthly Decay")
    st.write("The monthly decay rate is set at 2%, ensuring a gradual reduction in token emissions over time.")
    
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
    
    # Plot category evolution over time (Assuming they remain constant for now)
    weeks = np.arange(1, 101)
    fig_categories = go.Figure()
    
    for i, category in enumerate(categories):
        fig_categories.add_trace(go.Scatter(x=weeks, y=[initial_values[i]]*len(weeks), mode='lines', name=category))
    
    fig_categories.update_layout(title="Category Allocation Over Time", xaxis_title="Week", yaxis_title="Tokens", legend_title="Categories")
    st.plotly_chart(fig_categories)
    
if __name__ == "__main__":
    main()
