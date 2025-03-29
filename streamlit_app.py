import streamlit as st
import pandas as pd
import plotly.express as px

def main():
    st.title("Token Supply Distribution")
    
    st.sidebar.header("Initial Supply Input")
    
    categories = [
        "Treasury (Future Development)", "Team & Advisors", "Liquidity Providers", "Incentives", 
        "Ecosystem", "Fund Raising", "Seed Round", "Bridge Round", "Private Round", "Public Round"
    ]
    
    initial_supply = {}
    total_supply = st.sidebar.number_input("Total Initial Supply", min_value=0.0, value=1000000.0, step=1000.0)
    
    for category in categories:
        initial_supply[category] = st.sidebar.number_input(f"{category}", min_value=0.0, value=total_supply/len(categories), step=1000.0)
    
    st.sidebar.header("Emissions")
    emissions_raw = st.sidebar.number_input("Emissions Raw Number", min_value=0.0, value=50000.0, step=1000.0)
    emissions_decay = st.sidebar.slider("Emissions Decay (%)", min_value=0, max_value=100, value=10)
    
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
    
    # Display Emissions Data
    st.write("### Emissions")
    st.write(f"Raw Emissions: {emissions_raw}")
    st.write(f"Decay Rate: {emissions_decay}%")
    
if __name__ == "__main__":
    main()
