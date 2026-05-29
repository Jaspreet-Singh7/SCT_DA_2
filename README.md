# 🧹 Task 02 — Data Cleaning and Preparation

![SkillCraft Technology](https://img.shields.io/badge/SkillCraft-Technology-blue?style=for-the-badge)
![Track](https://img.shields.io/badge/Track-Data%20Analyst-green?style=for-the-badge)
![Task](https://img.shields.io/badge/Task-02-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.x-yellow?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Library-150458?style=for-the-badge&logo=pandas)

---

## 📌 Internship Details
| Field | Details |
|-------|---------|
| **Company** | SkillCraft Technology |
| **Intern** | Jaspreet Singh |
| **Track** | Data Analyst |
| **Track Code** | DA |
| **Task** | 02 |
| **Duration** | May 2026 – June 2026 |

---

## 📝 Task Description
Load a dataset (Global Superstore) into a **Python environment** using the **Pandas library**.

**Goal:** Identify and handle missing values, drop duplicate rows, and convert data types (e.g., change a string column to a date format). Export the cleaned data to a new CSV file.

---

## ✅ What I Did — 10 Step Process

| Step | Action | Result |
|------|--------|--------|
| 1 | Load raw dataset | 504 rows × 19 columns |
| 2 | Data quality report | Found 59 nulls, 9 duplicates |
| 3 | Remove duplicates | Removed 9 duplicate rows |
| 4 | Fix date columns | Converted to datetime format |
| 5 | Handle missing values | 0 nulls remaining |
| 6 | Fix data quality issues | Fixed negative sales & outliers |
| 7 | Standardize data types | Category dtype, rounded floats |
| 8 | Feature engineering | 4 new columns added |
| 9 | Final quality check | 0 nulls, 0 duplicates ✅ |
| 10 | Export cleaned CSV | 491 rows × 27 columns |

---

## 🔧 Data Issues Fixed
- ✅ **9 duplicate rows** removed
- ✅ **59 missing values** handled intelligently
- ✅ **Mixed date formats** (YYYY-MM-DD & DD/MM/YYYY) standardized
- ✅ **5 negative Sales** values corrected
- ✅ **3 profit outliers** capped at 99th percentile

---

## ⚙️ New Features Engineered
| Feature | Description |
|---------|-------------|
| `Profit Margin` | Profit / Sales ratio |
| `Net Revenue` | Sales × Quantity × (1 - Discount) |
| `Profit Category` | High / Moderate / Low Profit or Loss |
| `Shipping Speed` | Express / Standard / Slow |

---

## 🛠️ Tools & Libraries
- Python 3.x
- Pandas
- NumPy
- Jupyter Notebook / Google Colab compatible

---

## 📁 Files
| File | Description |
|------|-------------|
| `SCT_DA_2_Data_Cleaning.py` | Python script — 10 step cleaning process |
| `SCT_DA_2_global_superstore_cleaned.csv` | Final cleaned dataset |

---

## ▶️ How to Run
```python
# Install required libraries
pip install pandas numpy

# Run the script
python SCT_DA_2_Data_Cleaning.py
```

---

## 🔗 Connect
- **LinkedIn:** [Jaspreet Singh](https://linkedin.com/in/jaspreet-singh-877748275)
- **GitHub:** [Jaspreet-Singh7](https://github.com/Jaspreet-Singh7)

---

*SkillCraft Technology Data Analyst Internship — Task 02*
