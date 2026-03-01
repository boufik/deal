import pandas as pd
import json
from deal.core.logic import *
from deal.core.plotting import *


def main():
    filepath = """./data/Deal.xlsx"""
    df = pd.read_excel(filepath)
    df_transformed = transform_original(df)
    print(f"\n[*] Starting main...\n\n[*] A Deal Game Example:\n\n{df_transformed.head(7)}\n")
    plot_all_dates(df_transformed)
    avg_ks = calculate_average_k_per_round(df_transformed)
    plot_average_k_per_round(avg_ks)
    print("[*] Average k per round:")
    for round, avg_k in avg_ks.items():
        print(f"    Round {round}: avg_k = {100 * avg_k:.2f}%")
    print("\n\n[*] User Prompt to Click on the Remaining Cases")
    remaining_values = [1, 5, 10000, 20000, 70000]
    print(f"    remaining_values = {remaining_values}\n")
    object = compute_offer_with_avg(remaining_values, avg_ks)
    print(json.dumps(object, indent=4))
    print("\n[*] Exitting main...\n")


# MAIN FUNCTION
if __name__ == "__main__":
    main()