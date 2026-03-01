import streamlit as st
import numpy as np
from deal.core.logic import *


# Global Variables
LOW_VALUES = [0.01, 1, 2, 5, 10, 20, 50, 100, 250, 500, 750]
HIGH_VALUES = [1000, 1500, 2000, 3000, 4000, 5000, 7500, 10000, 20000, 40000, 70000]
ALL_VALUES = LOW_VALUES + HIGH_VALUES

# Streamlit Basics
st.set_page_config(layout="wide")
st.title("Deal Game Dashboard")

# ---------------------------------------------------
# -------- HTML row 1 for: LOW_VALUES (Blue) --------
# ---------------------------------------------------
st.markdown("### Low Values")
selected = []
cols_low = st.columns(len(LOW_VALUES))
for i, value in enumerate(LOW_VALUES):
    with cols_low[i]:
        checked = st.checkbox(f"{value}", value=True, key=f"low_{i}")
        st.markdown(
            f"""
            <div style="
                background-color:#2196F3;
                color:white;
                padding:15px;
                text-align:center;
                border-radius:8px;">
                {value}
            </div>
            """,
            unsafe_allow_html=True
        )
        if checked:
            selected.append(value)

# ---------------------------------------------------
# -------- HTML Row 2 for: HIGH_VALUES (Red) --------
# ---------------------------------------------------
st.markdown("### High Values")
cols_high = st.columns(len(HIGH_VALUES))
for i, value in enumerate(HIGH_VALUES):
    with cols_high[i]:
        checked = st.checkbox(f"{value}", value=True, key=f"high_{i}")
        st.markdown(
            f"""
            <div style="
                background-color:#F44336;
                color:white;
                padding:15px;
                text-align:center;
                border-radius:8px;">
                {value}
            </div>
            """,
            unsafe_allow_html=True
        )
        if checked:
            selected.append(value)

# BUSINESS LOGIC
filepath = """./data/Deal.xlsx"""
df = pd.read_excel(filepath)
df_transformed = transform_original(df)
avg_ks = calculate_average_k_per_round(df_transformed)
result = compute_offer_with_avg(selected, avg_ks)
st.markdown("---")
if not result["valid"]:
    st.error(result["message"])
else:
    metrics = {
        # Engineered Features (First 5)
        "EV": f"{result["EV"]:.2f}",
        "Std. Dev.": f"{result["std"]:.2f}",
        "Max Value": result["max_value"],
        "Min Value": result["min_value"],
        "Top3 Values": result["top3_sum"],
        # Engineered Features (Last 3)
        "Cases Left": result["cases_left"],
        "Cases To Open Next": result["cases_to_open_next"],
        "Round": result["round"],
        # Guess Features
        "k Multiplier": result["k_prediction"],
        "Offer Guess": result["offer_guess"] 
    }
    # ----------------------------------------------
    # -------- HTML row 3 for: Metrics Grid --------
    # ----------------------------------------------
    st.markdown("### Game Metrics")
    metric_cols = st.columns(len(list(result.keys())))
    for index, (key, value) in enumerate(metrics.items()):
        with metric_cols[index]:
            st.markdown(
                f"""
                <div style="
                    background-color:#111;
                    color:white;
                    padding:15px;
                    text-align:center;
                    border-radius:8px;">
                    <strong>{key}</strong><br>{value}
                </div>
                """,
                unsafe_allow_html=True
            )
    # ---------------------------------------------
    # -------- HTML row 4 for: Final Offer --------
    # ---------------------------------------------
    st.markdown("### Final Offer")
    st.markdown(
        f"""
        <div style="
            border: 4px solid green;
            padding: 30px;
            font-size: 36px;
            text-align: center;
            border-radius: 12px;">
            €{result["offer_guess"]:,.2f}
        </div>
        """,
        unsafe_allow_html=True
    )