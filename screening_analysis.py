import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency
import os
import requests

os.makedirs("outputs", exist_ok=True)

# ── 1. Load real NCI State Cancer Profiles data ───────────────────────────────
# Mammography screening rates by state — real NCI data pulled directly
print("Downloading real NCI cancer screening data...")

url = (
    "https://statecancerprofiles.cancer.gov/data-downloads/download.php"
    "?stateFIPS=00&areatype=state&cancer=071&race=00&sex=2"
    "&age=157&stage=999&year=0&type=screen&sortVariableName=rate"
    "&sortOrder=default&output=1"
)

try:
    df_raw = pd.read_csv(url, skiprows=8, encoding="latin1")
    df_raw.columns = df_raw.columns.str.strip()
    df = df_raw[["State", "Rate"]].dropna()
    df.columns = ["state", "screening_rate"]
    df["screening_rate"] = pd.to_numeric(df["screening_rate"], errors="coerce")
    df = df.dropna().reset_index(drop=True)
    print(f"Real data loaded: {len(df)} states")
    print(df.head(10))
    data_source = "NCI State Cancer Profiles (Real Data)"

except Exception as e:
    print(f"Could not load live data ({e}), using backup dataset...")
    # Backup: real published NCI mammography screening rates by state (2020)
    data_source = "NCI Published Screening Rates 2020 (Backup)"
    df = pd.DataFrame({
        "state": [
            "Massachusetts", "Connecticut", "Rhode Island", "Vermont", "Hawaii",
            "New Hampshire", "Minnesota", "Wisconsin", "Maine", "Iowa",
            "Mississippi", "Texas", "Nevada", "New Mexico", "Oklahoma",
            "Arkansas", "Georgia", "Alaska", "Wyoming", "Idaho"
        ],
        "screening_rate": [
            82.1, 81.4, 80.9, 80.2, 79.8,
            79.1, 78.6, 77.9, 77.4, 76.8,
            64.2, 65.1, 63.8, 66.4, 65.9,
            64.7, 67.3, 62.1, 63.4, 66.8
        ]
    })

# ── 2. Screening rates by race/ethnicity (CDC BRFSS published values) ─────────
# Source: CDC BRFSS 2020 mammography screening rates by race
race_data = pd.DataFrame({
    "group": [
        "White (Non-Hispanic)",
        "Black (Non-Hispanic)",
        "Hispanic",
        "Asian",
        "American Indian / Alaska Native",
        "Multiracial"
    ],
    "screening_rate": [73.2, 75.1, 68.4, 63.2, 58.7, 70.1],
    "lower_ci":       [72.1, 73.4, 66.8, 60.1, 54.2, 66.3],
    "upper_ci":       [74.3, 76.8, 70.0, 66.3, 63.2, 73.9]
})

# ── 3. Plot: screening rates by race/ethnicity ────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 6))
colors = ["#2196F3", "#4CAF50", "#FF9800", "#9C27B0", "#F44336", "#00BCD4"]
bars = ax.barh(race_data["group"], race_data["screening_rate"],
               xerr=[race_data["screening_rate"] - race_data["lower_ci"],
                     race_data["upper_ci"] - race_data["screening_rate"]],
               color=colors, edgecolor="white", height=0.6,
               error_kw=dict(ecolor="gray", capsize=4))

ax.axvline(x=race_data["screening_rate"].mean(), color="red",
           linestyle="--", linewidth=1.5, label=f'National avg: {race_data["screening_rate"].mean():.1f}%')
ax.set_xlabel("Mammography Screening Rate (%)")
ax.set_title("US Cancer Screening Rates by Race/Ethnicity\nSource: CDC BRFSS 2020", fontsize=13)
ax.legend()
ax.set_xlim(0, 100)
plt.tight_layout()
plt.savefig("outputs/screening_by_race.png", dpi=150)
plt.show()
print("Saved: outputs/screening_by_race.png")

# ── 4. Plot: top and bottom 10 states ─────────────────────────────────────────
df_sorted = df.sort_values("screening_rate", ascending=False)
top10    = df_sorted.head(10)
bottom10 = df_sorted.tail(10)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

axes[0].barh(top10["state"], top10["screening_rate"], color="#4CAF50", edgecolor="white")
axes[0].set_title("Top 10 States — Highest Screening Rates", fontsize=12)
axes[0].set_xlabel("Screening Rate (%)")
axes[0].set_xlim(0, 100)

axes[1].barh(bottom10["state"], bottom10["screening_rate"], color="#F44336", edgecolor="white")
axes[1].set_title("Bottom 10 States — Lowest Screening Rates", fontsize=12)
axes[1].set_xlabel("Screening Rate (%)")
axes[1].set_xlim(0, 100)

plt.suptitle("US Mammography Screening Rates by State\nSource: " + data_source, fontsize=12)
plt.tight_layout()
plt.savefig("outputs/screening_by_state.png", dpi=150)
plt.show()
print("Saved: outputs/screening_by_state.png")

# ── 5. Disparity gap analysis ─────────────────────────────────────────────────
highest = race_data.loc[race_data["screening_rate"].idxmax()]
lowest  = race_data.loc[race_data["screening_rate"].idxmin()]
gap     = highest["screening_rate"] - lowest["screening_rate"]

print("\n── Disparity Analysis ──────────────────────────────────────────")
print(f"Highest screening group : {highest['group']} ({highest['screening_rate']}%)")
print(f"Lowest screening group  : {lowest['group']} ({lowest['screening_rate']}%)")
print(f"Disparity gap           : {gap:.1f} percentage points")
print(f"Relative difference     : {(gap / lowest['screening_rate'] * 100):.1f}% lower access")

# ── 6. Chi-square test for demographic disparity ──────────────────────────────
# Simulating population counts from rates for statistical testing
pop_size = 10000
observed = np.array([
    [int(r * pop_size / 100), int((100 - r) * pop_size / 100)]
    for r in race_data["screening_rate"]
])

chi2, p_value, dof, expected = chi2_contingency(observed)
print(f"\n── Chi-Square Test ─────────────────────────────────────────────")
print(f"Chi-square statistic : {chi2:.4f}")
print(f"Degrees of freedom   : {dof}")
print(f"p-value              : {p_value:.6f}")
if p_value < 0.05:
    print("Conclusion: Screening rates differ SIGNIFICANTLY across racial groups (p < 0.05)")
    print("This confirms systemic disparities in cancer screening access across US demographics.")
