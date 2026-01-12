import pandas as pd


def cost_saving_recommendations(df: pd.DataFrame) -> pd.DataFrame:
    recos = []
    avg_unit_cost = df["cost_per_unit"].mean()

    for _, row in df.iterrows():
        if row["cost_pct"] > 20:
            recos.append({
                "item": row["item"],
                "issue": "High cost driver",
                "suggestion": "Negotiate supplier or reduce usage"
            })
        elif row["cost_per_unit"] > avg_unit_cost:
            recos.append({
                "item": row["item"],
                "issue": "High unit cost",
                "suggestion": "Find alternate vendor"
            })

    reco_df = pd.DataFrame(recos)

    with open("reports/management_summary.txt", "w", encoding="utf-8") as f:
        f.write("MANAGEMENT COST SUMMARY\n\n")
        for _, r in reco_df.iterrows():
            f.write(
                f"- {r['item'].title()}: {r['issue']} -> {r['suggestion']}\n"
            )

    return reco_df
