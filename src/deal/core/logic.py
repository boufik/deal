import numpy as np
import pandas as pd


# GLOBAL VARIABLES
VALID_CASES_LEFT = [17, 14, 11, 8, 5, 3, 2]
MAPPING_CASES_LEFT = {
    17: {"cases_to_open_next": 3, "round": 1},
    14: {"cases_to_open_next": 3, "round": 2},
    11: {"cases_to_open_next": 3, "round": 3},
    8: {"cases_to_open_next": 3, "round": 4},
    5: {"cases_to_open_next": 2, "round": 5},
    3: {"cases_to_open_next": 1, "round": 6},
    2: {"cases_to_open_next": 0, "round": 7},
}

# AUXILIARY FUNCTIONS
def transform_original(df):
    """
    Input: original dataframe with default features
    Output: transformed dataframe with engineered features
    """
    # Clean the column 'Offer' --> Remove € and commas if present --> Make it a numeric column
    df["Offer"] = (df["Offer"].astype(str).str.replace("€", "", regex=False).str.replace(",", "", regex=False).str.strip())
    df["Offer"] = pd.to_numeric(df["Offer"], errors="coerce")
    # Identify amount columns (everything except metadata)
    metadata_cols = ["Offer", "Date", "Timestamp"]
    amount_cols = [cname for cname in df.columns if cname not in metadata_cols]
    # Row-by-row Transformation
    transformed_rows = []
    for idx, row in df.iterrows():
        remaining_values = []
        for cname in amount_cols:
            if row[cname] == 1:
                try:
                    remaining_values.append(float(cname))
                except:
                    pass
        cases_left = len(remaining_values)
        if cases_left == 0:
            continue
        # 1) Engineered Features (First 5)
        EV = np.mean(remaining_values)
        std_remaining = np.std(remaining_values)
        max_value = np.max(remaining_values)
        min_value = np.min(remaining_values)
        if cases_left >= 3:
            top3_sum = sum(sorted(remaining_values, reverse=True)[:3])
        else:
            top3_sum = sum(remaining_values)
        transformed_row = {"EV": EV, "std": std_remaining, "max_value": max_value, "min_value": min_value, "top3_sum": top3_sum}
        # 2) Engineered Features (Last 3)
        transformed_row["cases_left"] = cases_left
        if cases_left in VALID_CASES_LEFT:
            transformed_row["cases_to_open_next"] = MAPPING_CASES_LEFT[cases_left]["cases_to_open_next"]
            transformed_row["round"] = MAPPING_CASES_LEFT[cases_left]["round"]
        else:
            print(f"\n{50*'-'}\nThis round has NOT a valid count of cases_left...\n{50*'-'}\n\n")
        # 3) Target Columns: Offer + k
        transformed_row["Offer"] = row["Offer"]
        transformed_row["k"] = row["Offer"] / EV
        # 4) Metadata Features
        if "Date" in df.columns:
            transformed_row["Date"] = row["Date"]
        # Append the row
        transformed_rows.append(transformed_row)
    df_transformed = pd.DataFrame(transformed_rows)
    return df_transformed


def calculate_average_k_per_round(df_transformed):
  """
  This function calculates the average value for k = Offer / EV per round.
  One can easily notice that this value keeps increasing as the rounds of the game proceed.
  It returns a dictionary like:
  [
      {1: 0.1128},
      {2: 0.2376},
      ...,
      {6: 0.7439},
      {7: 0.9063}
  ]
  """
  unique_rounds = df_transformed["round"].unique()
  avg_ks = dict()
  for round in unique_rounds:
    # Filtering
    subset = df_transformed[df_transformed["round"] == round]
    avg_k = subset["k"].mean()
    avg_ks[round] = float(avg_k)
  return avg_ks


# AUXILIARY FUNCTION
def compute_offer_with_avg(remaining_values, avg_ks):
    """
    This function guesses the banker's offer, based ONLY on the EV of the remaining case values.
    It does NOT deal with any ML techniques, that could consider other game states (e.g., cases_to_open_next).
    """
    # Check for validity
    cases_left = len(remaining_values)
    if cases_left not in VALID_CASES_LEFT:
        return {
            "valid": False,
            "message": "Invalid number of remaining cases. Please try again..."
        }
    # 1) Engineered Features (First 5)
    EV = float(np.mean(remaining_values))
    std_remaining = float(np.std(remaining_values))
    max_value = float(np.max(remaining_values))
    min_value = float(np.min(remaining_values))
    if cases_left >= 3:
        top3_sum = sum(sorted(remaining_values, reverse=True)[:3])
    else:
        top3_sum = sum(remaining_values)
    # 2) Engineered Features (Last 2)
    if cases_left in VALID_CASES_LEFT:
        cases_to_open_next = MAPPING_CASES_LEFT[cases_left]["cases_to_open_next"]
        round = MAPPING_CASES_LEFT[cases_left]["round"]
    else:
        print(f"\n{50*'-'}\nThis round has NOT a valid count of cases_left...\n{50*'-'}\n\n")
    # 3) Guess based on the EV
    k_prediction = avg_ks[round]
    offer_guess = k_prediction * EV
    # Return a dictionary will all available information
    return {
        "valid": True,
        "EV": EV,
        "std": std_remaining,
        "max_value": max_value,
        "min_value": min_value,
        "top3_sum": top3_sum,
        "cases_left": cases_left,
        "cases_to_open_next": cases_to_open_next,
        "round": round,
        "k_prediction": k_prediction,
        "offer_guess": offer_guess
    }