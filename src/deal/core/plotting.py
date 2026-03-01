import matplotlib.pyplot as plt


def plot_separate_dates(df_transformed):
    """
    This function creates one separate lineplot per 'Date'
    """
    # Sort the dataframe to ensure correct ordering
    df_transformed = df_transformed.sort_values(["Date", "round"])
    unique_dates = df_transformed["Date"].unique()
    for date in unique_dates:
        # Filtering
        subset = df_transformed[df_transformed["Date"] == date]
        # In case multiple entries/rows per round exist
        grouped = subset.groupby("round", as_index=False)["k"].mean()
        plt.figure(1)
        plt.plot(grouped["round"], grouped["k"])
        plt.xlabel("Round")
        plt.ylabel("k = Offer / EV")
        plt.title(f"{date}: The k Trend by Round")
        plt.show()


def plot_all_dates(df_transformed):
    """
    This function creates one combined plot with all dates
    """
    # Sort the dataframe to ensure correct ordering
    df_transformed = df_transformed.sort_values(["Date", "round"])
    unique_dates = df_transformed["Date"].unique()
    plt.figure(1)
    for date in unique_dates:
        # Filtering
        subset = df_transformed[df_transformed["Date"] == date]
        # In case multiple entries/rows per round exist
        grouped = subset.groupby("round", as_index=False)["k"].mean()
        plt.plot(grouped["round"], grouped["k"], label=str(date))
    plt.xlabel("Round")
    plt.ylabel("k = Offer / EV")
    plt.title("All Dates: The k Trend by Round")
    plt.legend()
    plt.show()


def plot_average_k_per_round(avg_ks):
    """
    This function creates a bar plot, illustrating the trend of k = Offer / EV.
    The plot contains 7 bars, each one of which shows how k increases per round.
    """
    avg_ks_values = list(avg_ks.values())
    unique_rounds = list(avg_ks.keys())
    plt.figure(2)
    bars = plt.bar(unique_rounds, avg_ks_values, color="#a8dae8")
    plt.xlabel("Round")
    plt.ylabel("Average k")
    plt.title("Average k = Offer / EV per Round")
    # Add centered value labels inside each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height / 2, f"{100*height:.2f}%", ha="center", va="center")
    plt.tight_layout()
    plt.show()