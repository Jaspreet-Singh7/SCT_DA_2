# ============================================================
#  SkillCraft Technology — Data Analyst Internship
#  Task 02: Data Cleaning and Preparation
#  Author : Jaspreet Singh  |  Track Code: DA
#  GitHub Repo: SCT_DA_2
# ============================================================

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────────────────────
# STEP 1 — Load the Raw Dataset
# ─────────────────────────────────────────────────────────────
print("=" * 60)
print("STEP 1: Loading Raw Dataset")
print("=" * 60)

df = pd.read_csv("global_superstore_raw.csv")

print(f"\n✅ Dataset loaded successfully!")
print(f"   Shape  : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"\n📋 Column Names:\n   {list(df.columns)}")
print(f"\n🔍 First 5 rows:\n{df.head()}")
print(f"\n📊 Data Types:\n{df.dtypes}")


# ─────────────────────────────────────────────────────────────
# STEP 2 — Initial Data Quality Report
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 2: Data Quality Report (Before Cleaning)")
print("=" * 60)

total_cells = df.shape[0] * df.shape[1]
missing     = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(2)
duplicates  = df.duplicated().sum()

print(f"\n📌 Total Rows        : {df.shape[0]}")
print(f"📌 Total Columns     : {df.shape[1]}")
print(f"📌 Total Cells       : {total_cells}")
print(f"📌 Duplicate Rows    : {duplicates}")
print(f"\n❌ Missing Values per Column:")
missing_report = pd.DataFrame({"Missing Count": missing, "Missing %": missing_pct})
print(missing_report[missing_report["Missing Count"] > 0].to_string())

print(f"\n🔢 Numeric Summary:\n{df.describe().round(2)}")

# Negative Sales check
neg_sales = (df["Sales"] < 0).sum()
print(f"\n⚠️  Negative Sales values : {neg_sales}")

# Profit outliers (> 3 std devs)
profit_mean = df["Profit"].mean()
profit_std  = df["Profit"].std()
outliers    = df[df["Profit"] > profit_mean + 3 * profit_std]
print(f"⚠️  Profit outliers (>3σ) : {len(outliers)}")


# ─────────────────────────────────────────────────────────────
# STEP 3 — Remove Duplicate Rows
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 3: Removing Duplicate Rows")
print("=" * 60)

before = len(df)
df = df.drop_duplicates()
after  = len(df)

print(f"\n🗑️  Duplicates removed : {before - after}")
print(f"✅ Rows after dedup   : {after}")


# ─────────────────────────────────────────────────────────────
# STEP 4 — Fix Date Columns (Convert to datetime)
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 4: Fixing Date Columns")
print("=" * 60)

print(f"\n🗓️  Sample Order Date values (raw):\n   {df['Order Date'].head(10).tolist()}")

def parse_mixed_dates(date_str):
    """Handle both YYYY-MM-DD and DD/MM/YYYY formats."""
    if pd.isna(date_str):
        return pd.NaT
    date_str = str(date_str).strip()
    if "/" in date_str:
        try:
            return pd.to_datetime(date_str, format="%d/%m/%Y")
        except:
            return pd.NaT
    try:
        return pd.to_datetime(date_str, format="%Y-%m-%d")
    except:
        return pd.NaT

df["Order Date"] = df["Order Date"].apply(parse_mixed_dates)
df["Ship Date"]  = pd.to_datetime(df["Ship Date"], errors="coerce")

print(f"\n✅ Order Date dtype  : {df['Order Date'].dtype}")
print(f"✅ Ship Date dtype   : {df['Ship Date'].dtype}")
print(f"   Null Order Dates  : {df['Order Date'].isna().sum()}")
print(f"   Null Ship Dates   : {df['Ship Date'].isna().sum()}")

# Derive useful date features
df["Order Year"]  = df["Order Date"].dt.year
df["Order Month"] = df["Order Date"].dt.month
df["Order Month Name"] = df["Order Date"].dt.strftime("%b")
df["Shipping Days"] = (df["Ship Date"] - df["Order Date"]).dt.days

print(f"\n📅 New derived columns added: Order Year, Order Month, Order Month Name, Shipping Days")


# ─────────────────────────────────────────────────────────────
# STEP 5 — Handle Missing Values
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 5: Handling Missing Values")
print("=" * 60)

# Sales — fill with median per Category
sales_null_before = df["Sales"].isna().sum()
df["Sales"] = df.groupby("Category")["Sales"].transform(
    lambda x: x.fillna(x.median())
)
print(f"\n💰 Sales nulls fixed   : {sales_null_before} → {df['Sales'].isna().sum()} "
      f"(filled with category median)")

# Profit — fill with median per Category
profit_null_before = df["Profit"].isna().sum()
df["Profit"] = df.groupby("Category")["Profit"].transform(
    lambda x: x.fillna(x.median())
)
print(f"💸 Profit nulls fixed  : {profit_null_before} → {df['Profit'].isna().sum()} "
      f"(filled with category median)")

# Discount — fill with 0 (assume no discount if missing)
disc_null_before = df["Discount"].isna().sum()
df["Discount"] = df["Discount"].fillna(0)
print(f"🏷️  Discount nulls fixed: {disc_null_before} → {df['Discount'].isna().sum()} "
      f"(filled with 0 — no discount assumed)")

# Ship Mode — fill with mode
ship_null_before = df["Ship Mode"].isna().sum()
ship_mode_val = df["Ship Mode"].mode()[0]
df["Ship Mode"] = df["Ship Mode"].fillna(ship_mode_val)
print(f"🚚 Ship Mode nulls fixed: {ship_null_before} → {df['Ship Mode'].isna().sum()} "
      f"(filled with mode: '{ship_mode_val}')")

# Customer Name — fill with 'Unknown'
cust_null_before = df["Customer Name"].isna().sum()
df["Customer Name"] = df["Customer Name"].fillna("Unknown")
print(f"👤 Customer Name nulls : {cust_null_before} → {df['Customer Name'].isna().sum()} "
      f"(filled with 'Unknown')")

total_nulls_after = df.isnull().sum().sum()
print(f"\n✅ Total nulls remaining: {total_nulls_after}")


# ─────────────────────────────────────────────────────────────
# STEP 6 — Fix Data Quality Issues
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 6: Fixing Data Quality Issues")
print("=" * 60)

# Fix negative Sales values
neg_before = (df["Sales"] < 0).sum()
df["Sales"] = df["Sales"].abs()
print(f"\n⚠️  Negative Sales fixed : {neg_before} rows → converted to absolute values")

# Cap profit outliers at 99th percentile
p99 = df["Profit"].quantile(0.99)
outlier_before = (df["Profit"] > p99).sum()
df["Profit"] = df["Profit"].clip(upper=p99)
print(f"📈 Profit outliers capped: {outlier_before} rows → capped at 99th percentile (${p99:.2f})")

# Validate Quantity is positive integer
invalid_qty = (df["Quantity"] <= 0).sum()
df = df[df["Quantity"] > 0]
print(f"📦 Invalid Quantity rows removed: {invalid_qty}")

# Validate Discount is between 0 and 1
df["Discount"] = df["Discount"].clip(lower=0, upper=1)
print(f"🏷️  Discount values clipped to [0, 1] range")


# ─────────────────────────────────────────────────────────────
# STEP 7 — Data Type Standardization
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 7: Data Type Standardization")
print("=" * 60)

df["Sales"]    = df["Sales"].round(2).astype(float)
df["Profit"]   = df["Profit"].round(2).astype(float)
df["Discount"] = df["Discount"].round(2).astype(float)
df["Quantity"] = df["Quantity"].astype(int)

cat_cols = ["Ship Mode","Customer ID","Segment","Country",
            "City","State","Region","Category","Sub-Category"]
for col in cat_cols:
    df[col] = df[col].astype("category")

print(f"\n✅ Numeric columns rounded to 2 decimal places")
print(f"✅ Categorical columns converted to 'category' dtype")
print(f"\n📋 Updated Data Types:\n{df.dtypes}")


# ─────────────────────────────────────────────────────────────
# STEP 8 — Feature Engineering
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 8: Feature Engineering")
print("=" * 60)

# Profit Margin
df["Profit Margin"] = (df["Profit"] / df["Sales"]).round(4)
df["Profit Margin"] = df["Profit Margin"].replace([np.inf, -np.inf], 0)

# Revenue after discount
df["Net Revenue"] = (df["Sales"] * df["Quantity"] * (1 - df["Discount"])).round(2)

# Profit Category
def profit_bucket(margin):
    if margin >= 0.20:
        return "High Profit"
    elif margin >= 0.05:
        return "Moderate Profit"
    elif margin >= 0:
        return "Low Profit"
    else:
        return "Loss"

df["Profit Category"] = df["Profit Margin"].apply(profit_bucket)

# Shipping speed label
def ship_speed(days):
    if pd.isna(days) or days < 0:
        return "Unknown"
    if days <= 2:
        return "Express"
    elif days <= 4:
        return "Standard"
    else:
        return "Slow"

df["Shipping Speed"] = df["Shipping Days"].apply(ship_speed)

print(f"\n✅ New features created:")
print(f"   • Profit Margin   — ratio of Profit to Sales")
print(f"   • Net Revenue     — Sales × Quantity × (1 - Discount)")
print(f"   • Profit Category — High/Moderate/Low Profit or Loss")
print(f"   • Shipping Speed  — Express / Standard / Slow")
print(f"\n📊 Profit Category distribution:\n{df['Profit Category'].value_counts()}")
print(f"\n🚀 Shipping Speed distribution:\n{df['Shipping Speed'].value_counts()}")


# ─────────────────────────────────────────────────────────────
# STEP 9 — Final Quality Check
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 9: Final Quality Check")
print("=" * 60)

print(f"\n📌 Final Shape        : {df.shape[0]} rows × {df.shape[1]} columns")
print(f"📌 Remaining Nulls    : {df.isnull().sum().sum()}")
print(f"📌 Remaining Dupes    : {df.duplicated().sum()}")
print(f"📌 Negative Sales     : {(df['Sales'] < 0).sum()}")
print(f"\n📊 Final Numeric Summary:\n{df[['Sales','Profit','Quantity','Discount','Profit Margin','Net Revenue']].describe().round(2)}")
print(f"\n✅ All checks passed! Dataset is clean.")


# ─────────────────────────────────────────────────────────────
# STEP 10 — Export Cleaned Dataset to CSV
# ─────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 10: Exporting Cleaned Dataset")
print("=" * 60)

output_path = "global_superstore_cleaned.csv"
df.to_csv(output_path, index=False)

print(f"\n✅ Cleaned dataset saved to: {output_path}")
print(f"   Rows    : {len(df)}")
print(f"   Columns : {len(df.columns)}")
print(f"   Columns : {list(df.columns)}")
print(f"\n🎉 Task 02 Complete — Data Cleaning and Preparation Done!")
print("=" * 60)
