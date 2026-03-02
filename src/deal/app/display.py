import streamlit as st
import numpy as np




# -----------------------------------------------------------------------------------------------------
# ------------------------------------ Auxiliary Functions --------------------------------------------
# -----------------------------------------------------------------------------------------------------


def display_streamlit_css_basics():
    """
    This function deals with displaying Streamlit and CSS basics
    """
    st.set_page_config(page_title="Deal Game Dashboard", page_icon="💼", layout="wide")
    st.markdown("""
    <style>
        /* 1. Low-value blue checkboxes */
        input[id^="low_"] {
            accent-color: #2196F3;
        }
        /* 2. High-value red checkboxes */
        input[id^="high_"] {
            accent-color: #F44336;
        }
    </style>
    """, unsafe_allow_html=True)


def display_values_grid(LOW_VALUES, HIGH_VALUES):

    """
    This function deals with displaying:
    * HTML row 1 for LOW_VALUES (Blue)
    * HTML row 2 for HIGH_VALUES (Red)
    """

    # ------------------------------------------
    # ---- HTML row 1 for LOW_VALUES (Blue) ----
    # ------------------------------------------
    st.markdown("<h2 style='color: #2196F3;'>Low Values (11 Total)</h2>", unsafe_allow_html=True)
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
                    font-size:24px;
                    font-weight:700;
                    padding:10px;
                    text-align:center;
                    border-radius:8px;"
                    class="big-number">
                    {value:,} €
                </div>
                """,
                unsafe_allow_html=True
            )
            if checked:
                selected.append(value)

    # ------------------------------------------
    # ---- HTML row 2 for HIGH_VALUES (Red) ----
    # ------------------------------------------
    st.markdown("<h2 style='color: #F44336; margin-top:1rem;'>High Values (11 Total)</h2>", unsafe_allow_html=True)
    cols_high = st.columns(len(HIGH_VALUES))
    for i, value in enumerate(HIGH_VALUES):
        with cols_high[i]:
            checked = st.checkbox(f"{value}", value=True, key=f"high_{i}")
            st.markdown(
                f"""
                <div style="
                    background-color:#F44336;
                    color:white;
                    font-size:24px;
                    font-weight:700;
                    padding:10px;
                    text-align:center;
                    border-radius:8px;"
                    class="big-number">
                    {value:,} €
                </div>
                """,
                unsafe_allow_html=True
            )
            if checked:
                selected.append(value)
    return selected


def display_offer_and_metrics(result):
    
    """
    This function deals with displaying:
    * HTML row 3 for Offer Guess
    * HTML row 4 for Metrics Grid
    """

    # ---------------------------------------------
    # -------- HTML row 3 for: Offer Guess --------
    # ---------------------------------------------
    st.markdown("<h2 style='color: #00C853;'>EV-based Offer Guess</h2>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="
            border: 4px solid #00C853;
            color: #00C853;
            padding: 30px;
            font-size: 36px;
            font-weight:700;
            text-align: center;
            border-radius: 12px;">
            {int(result["offer_guess"]):,} €
        </div>
        """,
        unsafe_allow_html=True
    )
    # Include all metrics
    metrics = {
        # Engineered Features (First 5)
        "EV": f"{result["EV"]:.2f}",
        "Std. Dev.": f"{result["std"]:.2f}",
        "Max Value": result["max_value"],
        "Min Value": result["min_value"],
        "Top3 Values": result["top3_sum"],
        # Engineered Features (Last 3)
        "Remaining Cases": result["cases_left"],
        "Cases To Open Next": result["cases_to_open_next"],
        "Round": result["round"],
        # Guess Features
        "k Multiplier": result["k_prediction"],
        "Offer Guess": result["offer_guess"] 
    }
    # Include the most necessary metrics only 
    metrics = {
        "Round": result["round"],
        "Offer Guess": result["offer_guess"],
        "k": result["k_prediction"],
        "EV": result["EV"],
        "Remaining Cases": result["cases_left"],
        "Cases To Open Next": result["cases_to_open_next"]
    }

    # ----------------------------------------------
    # -------- HTML row 4 for: Metrics Grid --------
    # ----------------------------------------------
    st.markdown("<h2 style='margin-top:1rem;'>Game Metrics</h2>", unsafe_allow_html=True)
    metric_cols = st.columns(len(metrics))
    for index, (key, value) in enumerate(metrics.items()):
        # Formatting options for value
        try:
            numeric_value = float(value)
            if key == "k":
                value = f"{100*numeric_value:.2f}%"
            elif key == "Offer Guess" or key == "EV":
                value = f"{int(numeric_value):,} €"
            elif numeric_value.is_integer():
                value = f"{int(numeric_value)}"
            else:
                value = f"{numeric_value:,.2f}"
        except:
            pass

        with metric_cols[index]:
            st.markdown(
                f"""
                <div style="
                    background-color:#1c1c1c;
                    padding:20px;
                    border-radius:12px;
                    text-align:center;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
                    transition: transform 0.2s ease;
                ">
                    <div style="
                        font-size:18px;
                        font-weight:700;
                        color:#aaa;
                        margin-bottom:8px;
                        letter-spacing:0.5px;
                    ">
                        {key}
                    </div>
                    <div style="
                        font-size:26px;
                        font-weight:700;
                        color:white;
                    ">
                        {value}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------