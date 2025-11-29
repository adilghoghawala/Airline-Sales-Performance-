# src/analysis.py
import pandas as pd
from pathlib import Path

# Path to your Kaggle CSV
DATA_PATH = Path("data/US Airline Flight Routes and Fares 1993-2024.csv")  # <-- adjust name if needed

# CONFIG
YEAR_MIN = 2018
YEAR_MAX = 2023
OUR_CARRIER = "UA"   # e.g. "UA", "DL", "AA" – will filter on carrier_lg


def load_and_prepare():
    df = pd.read_csv(DATA_PATH, low_memory=False)
    #print(df["carrier_lg"].value_counts().head(20))


    # Map your real column names
    year_col = "Year"
    quarter_col = "quarter"
    origin_col = "airport_1"
    dest_col = "airport_2"
    pax_col = "passengers"
    fare_col = "fare"
    carrier_lg_col = "carrier_lg"
    large_ms_col = "large_ms"   # market share of largest carrier

    df = df[
        [
            year_col,
            quarter_col,
            origin_col,
            dest_col,
            pax_col,
            fare_col,
            carrier_lg_col,
            large_ms_col,
        ]
    ].copy()

    # Filter to a recent window
    df = df[(df[year_col] >= YEAR_MIN) & (df[year_col] <= YEAR_MAX)]

    # Standardize names
    df = df.rename(
        columns={
            year_col: "year",
            quarter_col: "quarter",
            origin_col: "origin",
            dest_col: "dest",
            pax_col: "passengers",
            fare_col: "avg_fare",
            carrier_lg_col: "largest_carrier",
            large_ms_col: "largest_ms",
        }
    )

    # Route key
    df["route"] = df["origin"] + "-" + df["dest"]

    # Total market revenue (all carriers on that route)
    df["market_revenue"] = df["passengers"] * df["avg_fare"]

    # Ensure largest_ms is in 0–1, not 0–100
    df["largest_ms"] = pd.to_numeric(df["largest_ms"], errors="coerce")
    if df["largest_ms"].max() > 1.5:
        # looks like percentages; convert to fraction
        df["largest_ms"] = df["largest_ms"] / 100.0

    # Approx "our" revenue = market_revenue * largest carrier share
    df["our_revenue"] = df["market_revenue"] * df["largest_ms"]

    return df


def summarize_for_carrier(df: pd.DataFrame, carrier: str):
    """
    Focus on one carrier: rows where this carrier is the largest.
    """
    ours = df[df["largest_carrier"] == carrier].copy()
    if ours.empty:
        raise ValueError(f"No rows found where carrier_lg == '{carrier}'. Try a different code.")

    # Route-level summary across years
    route_summary = (
        ours.groupby("route", as_index=False)
        .agg(
            avg_annual_our_revenue=("our_revenue", "mean"),
            avg_annual_market_revenue=("market_revenue", "mean"),
            avg_share=("largest_ms", "mean"),
            years_active=("year", pd.Series.nunique),
        )
    )

    # Simple revenue trend: first vs last year
    ours_sorted = ours.sort_values(["route", "year"])
    first = (
        ours_sorted.groupby("route", as_index=False)
        .first()[["route", "year", "our_revenue"]]
        .rename(columns={"year": "year_first", "our_revenue": "rev_first"})
    )
    last = (
        ours_sorted.groupby("route", as_index=False)
        .last()[["route", "year", "our_revenue"]]
        .rename(columns={"year": "year_last", "our_revenue": "rev_last"})
    )

    trend = first.merge(last, on="route")
    trend["rev_change"] = trend["rev_last"] - trend["rev_first"]
    trend["rev_change_pct"] = trend["rev_change"] / trend["rev_first"].replace(0, pd.NA)

    route_summary = route_summary.merge(trend, on="route", how="left")
    return ours, route_summary


def identify_underperforming_routes(route_summary: pd.DataFrame,
                                    share_threshold: float = 0.25,
                                    rev_change_threshold: float = 0.0):
    """
    Underperforming = route where our carrier has:
      - low average share (below share_threshold), AND
      - flat or declining revenue over time (rev_change <= rev_change_threshold).
    """
    underperf = route_summary[
        (route_summary["avg_share"] < share_threshold)
        & (route_summary["rev_change"] <= rev_change_threshold)
    ].copy()

    underperf = underperf.sort_values(["avg_share", "rev_change"])
    return underperf


def main():
    print("Loading and preparing data...")
    df = load_and_prepare()
    print(f"Loaded {len(df):,} rows for years {YEAR_MIN}-{YEAR_MAX}")
    print("Example largest carriers:", df["largest_carrier"].value_counts().head().to_dict())

    print(f"\nFocusing on carrier_lg == '{OUR_CARRIER}'...")
    ours, route_summary = summarize_for_carrier(df, OUR_CARRIER)

    print("\n=== Top 10 routes by average annual our_revenue ===")
    print(
        route_summary.sort_values("avg_annual_our_revenue", ascending=False)
        .head(10)[["route", "avg_annual_our_revenue", "avg_share", "rev_change_pct"]]
        .to_string(index=False)
    )

    print("\n=== Underperforming routes (low share + flat/declining revenue) ===")
    underperf = identify_underperforming_routes(route_summary)
    if underperf.empty:
        print("No routes meet underperformance criteria with current thresholds.")
    else:
        print(
            underperf[[
                "route",
                "avg_annual_our_revenue",
                "avg_share",
                "rev_first",
                "rev_last",
                "rev_change",
                "rev_change_pct",
            ]].head(15).to_string(index=False)
        )

    # Save CSVs for further review / charts
    out_dir = Path("outputs")
    out_dir.mkdir(exist_ok=True)
    route_summary.to_csv(out_dir / f"{OUR_CARRIER}_route_summary.csv", index=False)
    underperf.to_csv(out_dir / f"{OUR_CARRIER}_underperforming_routes.csv", index=False)
    print(f"\nSaved summary CSVs in {out_dir}/")


if __name__ == "__main__":
    main()
