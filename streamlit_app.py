import streamlit as st
import pandas as pd

def main():
    st.title("Token Supply and Unlock Schedule")
    
    # Define categories and values
    categories = [
        "Liquidity Providers", "Incentives", "Ecosystem", "Treasury (Future Development)",
        "Seed Round", "Bridge Round", "Private Round", "Public Round", "Future Raise", "Team & Advisors"
    ]
    
    total_allocation = [
        12_500_000, 23_000_000, 4_305_556, 14_000_000, 10_000_000,
        2_200_000, 1_666_667, 5_694_444, 3_333_333, 23_300_000
    ]
    
    tge_unlock = [
        2_778_000, 6_191_250, 733_333, 0, 0,
        0, 83_333, 5_694_444, 0, 0
    ]
    
    # Create DataFrame
    data = pd.DataFrame({
        "Category": categories,
        "Total Allocation": total_allocation,
        "Initial Unlock at TGE": tge_unlock
    })
    
    # Display Table
    st.write("### Initial Supply Breakdown")
    st.table(data)
    
if __name__ == "__main__":
    main()
