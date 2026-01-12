import pandas as p

def clean_data(df: p.DataFrame) -> p.DataFrame:
    # Rename columns
    cleaned_df = df.rename(columns={
        "Unnamed: 0": "item",
        "UNITS": "unit",
        "NUMBER": "quantity",
        "RUPEES": "cost",
    })

    # Select required columns
    cleaned_df = cleaned_df[["item", "unit", "quantity", "cost"]]

    # Convert to numeric
    cleaned_df["quantity"] = p.to_numeric(cleaned_df["quantity"], errors="coerce")
    cleaned_df["cost"] = p.to_numeric(cleaned_df["cost"], errors="coerce")

    # Drop missing values
    cleaned_df = cleaned_df.dropna()

    # Clean item names
    cleaned_df["item"] = cleaned_df["item"].str.lower().str.strip()

    return cleaned_df
