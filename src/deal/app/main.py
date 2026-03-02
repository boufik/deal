import streamlit as st
import numpy as np
from deal.core.logic import *
from deal.app.display import *


# Global Variables
LOW_VALUES = [0.01, 1, 2, 5, 10, 20, 50, 100, 250, 500, 750]
HIGH_VALUES = [1000, 1500, 2000, 3000, 4000, 5000, 7500, 10000, 20000, 40000, 70000]
FILEPATH = """./data/Deal.xlsx"""


def main():
    # Streamlit + CSS basics
    display_streamlit_css_basics()
    # Display LOW_VALUES (Blue) + HIGH_VALUES (Red)
    selected = display_values_grid(LOW_VALUES, HIGH_VALUES)
    # Business Logic: Transform the DataFrame that is created by the remaining case values
    df = pd.read_excel(FILEPATH)
    df_transformed = transform_original(df)
    avg_ks = calculate_average_k_per_round(df_transformed)
    result = compute_offer_with_avg(selected, avg_ks)
    # Display the intermediate section
    st.markdown("---")
    if not result["valid"]:
        st.error(result["error_message"])
    else:
        display_offer_and_metrics(result)


# MAIN FUNCTION
if __name__ == "__main__":
    main()