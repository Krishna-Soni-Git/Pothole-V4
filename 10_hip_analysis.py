# """
# 10_hip_analysis.py  —  Highway Improvement Plan (HIP) Analysis
# Generates 3 figures for the HIP slide of the NS Pothole Dashboard.

# Place Highway_Improvement_Plan_-_Roads_20260309.csv in the same folder
# and run:  python 10_hip_analysis.py

# Outputs (saved to outputs/):
#     10a_hip_by_county.png      — KM investment by county, coloured by work type
#     10b_hip_by_type.png        — Work type breakdown (donut / bar)
#     10c_hip_status.png         — Project status: Completed vs Planned vs Started
# """

# import pandas as pd
# import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches
# import numpy as np
# import os

# # ── colours matching dashboard ──────────────────────────────────
# BG   = "#0D1117"
# CARD = "#161B22"
# BORDER = "#21262D"
# RED  = "#F85149"
# BLUE = "#388BFD"
# GOLD = "#D29922"
# GREEN = "#3FB950"
# TEXT = "#E6EDF3"
# SUB  = "#8B949E"
# MUTED= "#6E7681"
# PURPLE = "#A371F7"

# plt.rcParams.update({
#     "figure.facecolor": BG,
#     "axes.facecolor":   CARD,
#     "axes.edgecolor":   BORDER,
#     "axes.labelcolor":  SUB,
#     "xtick.color":      SUB,
#     "ytick.color":      SUB,
#     "text.color":       TEXT,
#     "grid.color":       BORDER,
#     "grid.linestyle":   "--",
#     "grid.alpha":       0.6,
#     "font.family":      "DejaVu Sans",
#     "axes.spines.top":  False,
#     "axes.spines.right":False,
# })

# os.makedirs("outputs", exist_ok=True)

# # ── counties we map to your existing 5 weather regions ──────────
# REGION_MAP = {
#     "Halifax":     "Halifax / Lunenburg",
#     "Lunenburg":   "Halifax / Lunenburg",
#     "Annapolis":   "Annapolis Valley",
#     "Kings":       "Annapolis Valley",
#     "Digby":       "Annapolis Valley",
#     "Yarmouth":    "SW Nova / Shelburne",
#     "Shelburne":   "SW Nova / Shelburne",
#     "Queens":      "SW Nova / Shelburne",
#     "Cape Breton": "Cape Breton",
#     "Inverness":   "Cape Breton",
#     "Richmond":    "Cape Breton",
#     "Victoria":    "Cape Breton",
#     "Colchester":  "Central NS",
#     "Cumberland":  "Central NS",
#     "Pictou":      "Central NS",
#     "Antigonish":  "Central NS",
#     "Guysborough": "Central NS",
#     "Hants":       "Central NS",
# }

# REGION_COLORS = {
#     "Halifax / Lunenburg":  RED,
#     "Annapolis Valley":     BLUE,
#     "SW Nova / Shelburne":  GOLD,
#     "Cape Breton":          GREEN,
#     "Central NS":           PURPLE,
# }

# VALID_COUNTIES = list(REGION_MAP.keys())

# # ──────────────────────────────────────────────────────────────
# # LOAD & CLEAN
# # ──────────────────────────────────────────────────────────────
# df = pd.read_csv(
#     "Highway_Improvement_Plan_-_Roads_20260309.csv",
#     usecols=["PROJECT_DE","KM","COUNTY","PROJECT_TY","CONSTRUCT_","YEAR_START","YEAR_END","Status"],
#     dtype=str,
#     low_memory=False,
# )

# # Drop rows where COUNTY is actually geometry junk
# df = df[df["COUNTY"].isin(VALID_COUNTIES)].copy()
# df["KM"]   = pd.to_numeric(df["KM"], errors="coerce")
# df["Status"] = df["Status"].str.strip()
# df = df[df["Status"].isin(["Planned","Completed","Started"])].copy()
# df["Region"] = df["COUNTY"].map(REGION_MAP)

# # Simplify CONSTRUCT_ labels
# label_map = {
#     "Repaving 100 Series Highways":           "Repave: 100-Series Hwy",
#     "Repaving Arterial/Collectors":           "Repave: Arterial/Collector",
#     "Repaving Local Roads":                   "Repave: Local Roads",
#     "Maintenance Paving":                     "Maintenance Paving",
#     "Single Lift Overlay":                    "Single Lift Overlay",
#     "Double Chip Resurfacing":                "Double Chip Resurfacing",
#     "Pavement Strengthening":                 "Pavement Strengthening",
#     "Gravel Road Program":                    "Gravel Road Program",
#     "Construction 100 Series Highways":       "Construction: 100-Series",
#     "Construction Arterial/Collector":        "Construction: Arterial",
#     "Construction Local Road":                "Construction: Local Road",
#     "100 Series Expansion & Other Major Road Upgrade":  "Major Expansion",
#     "100 Series Expansion & Other Major Road Upgrades": "Major Expansion",
#     "Paving Subdivision Roads":               "Subdivision Paving",
# }
# df["WorkType"] = df["CONSTRUCT_"].map(label_map).fillna(df["CONSTRUCT_"].str.strip())

# print(f"Clean rows: {len(df)}")
# print(f"Total KM: {df['KM'].sum():.1f}")

# # ──────────────────────────────────────────────────────────────
# # FIGURE 1 — KM by County, coloured by Region
# # ──────────────────────────────────────────────────────────────
# county_km = (df.groupby(["COUNTY","Region"])["KM"]
#              .sum().reset_index()
#              .sort_values("KM", ascending=True))

# fig1, ax1 = plt.subplots(figsize=(10, 7))
# bars = ax1.barh(
#     county_km["COUNTY"],
#     county_km["KM"],
#     color=[REGION_COLORS[r] for r in county_km["Region"]],
#     height=0.65,
#     alpha=0.85,
# )
# # Value labels
# for bar, km in zip(bars, county_km["KM"]):
#     ax1.text(bar.get_width() + 3, bar.get_y() + bar.get_height()/2,
#              f"{km:.0f} km", va="center", ha="left",
#              fontsize=9, color=SUB)

# ax1.set_xlabel("Total Road Kilometres Planned / Completed", fontsize=10, color=SUB, labelpad=8)
# ax1.set_title("Highway Improvement Plan: KM Investment by County",
#               fontsize=13, fontweight="bold", color=TEXT, pad=14, loc="left")
# ax1.set_xlim(0, county_km["KM"].max() * 1.22)
# ax1.tick_params(axis="both", labelsize=9)
# ax1.grid(axis="x", alpha=0.4)
# ax1.set_facecolor(CARD)
# fig1.patch.set_facecolor(BG)

# # Legend
# patches = [mpatches.Patch(color=c, label=r) for r, c in REGION_COLORS.items()]
# ax1.legend(handles=patches, loc="lower right", fontsize=8,
#            facecolor=CARD, edgecolor=BORDER, labelcolor=TEXT)

# plt.tight_layout()
# plt.savefig("outputs/10a_hip_by_county.png", dpi=150, bbox_inches="tight", facecolor=BG)
# plt.close()
# print("Saved 10a_hip_by_county.png")

# # ──────────────────────────────────────────────────────────────
# # FIGURE 2 — Work Type bar chart (top 10 by KM)
# # ──────────────────────────────────────────────────────────────
# work_km = (df.groupby("WorkType")["KM"]
#            .sum().sort_values(ascending=True).tail(10))

# # Colour: repaving = RED, construction = BLUE, maintenance/other = GOLD
# def wtype_color(w):
#     if "Repave" in w or "Overlay" in w or "Chip" in w:
#         return RED
#     if "Construction" in w or "Expansion" in w:
#         return BLUE
#     if "Gravel" in w:
#         return GOLD
#     return GREEN

# colors2 = [wtype_color(w) for w in work_km.index]

# fig2, ax2 = plt.subplots(figsize=(10, 5))
# bars2 = ax2.barh(work_km.index, work_km.values, color=colors2, height=0.6, alpha=0.85)
# for bar, km in zip(bars2, work_km.values):
#     ax2.text(bar.get_width() + 2, bar.get_y() + bar.get_height()/2,
#              f"{km:.0f} km", va="center", ha="left", fontsize=9, color=SUB)
# ax2.set_xlabel("Total KM", fontsize=10, color=SUB)
# ax2.set_title("Investment by Construction Work Type (Top 10)",
#               fontsize=13, fontweight="bold", color=TEXT, pad=14, loc="left")
# ax2.set_xlim(0, work_km.max() * 1.22)
# ax2.tick_params(axis="both", labelsize=9)
# ax2.grid(axis="x", alpha=0.4)
# ax2.set_facecolor(CARD)
# fig2.patch.set_facecolor(BG)

# patch_leg = [
#     mpatches.Patch(color=RED,  label="Repaving / Resurfacing"),
#     mpatches.Patch(color=BLUE, label="New Construction"),
#     mpatches.Patch(color=GOLD, label="Gravel Program"),
#     mpatches.Patch(color=GREEN,label="Strengthening / Other"),
# ]
# ax2.legend(handles=patch_leg, fontsize=8, facecolor=CARD, edgecolor=BORDER, labelcolor=TEXT)

# plt.tight_layout()
# plt.savefig("outputs/10b_hip_by_type.png", dpi=150, bbox_inches="tight", facecolor=BG)
# plt.close()
# print("Saved 10b_hip_by_type.png")

# # ──────────────────────────────────────────────────────────────
# # FIGURE 3 — Status × Region grouped bar
# # ──────────────────────────────────────────────────────────────
# region_status = (df.groupby(["Region","Status"])["KM"]
#                  .sum().unstack(fill_value=0).reset_index())

# regions = region_status["Region"].tolist()
# x = np.arange(len(regions))
# width = 0.25

# fig3, ax3 = plt.subplots(figsize=(10, 5))

# if "Completed" in region_status.columns:
#     ax3.bar(x - width, region_status["Completed"], width, label="Completed", color=GREEN, alpha=0.85)
# if "Started" in region_status.columns:
#     ax3.bar(x,         region_status["Started"],   width, label="Started",   color=GOLD,  alpha=0.85)
# if "Planned" in region_status.columns:
#     ax3.bar(x + width, region_status["Planned"],   width, label="Planned",   color=BLUE,  alpha=0.85)

# ax3.set_xticks(x)
# ax3.set_xticklabels([r.replace(" / ", "\n").replace(" / ", "/") for r in regions],
#                     fontsize=9, color=SUB)
# ax3.set_ylabel("KM", fontsize=10, color=SUB)
# ax3.set_title("Project Status by Region: Completed vs. Planned",
#               fontsize=13, fontweight="bold", color=TEXT, pad=14, loc="left")
# ax3.legend(fontsize=9, facecolor=CARD, edgecolor=BORDER, labelcolor=TEXT)
# ax3.tick_params(axis="both", labelsize=9)
# ax3.grid(axis="y", alpha=0.4)
# ax3.set_facecolor(CARD)
# fig3.patch.set_facecolor(BG)

# plt.tight_layout()
# plt.savefig("outputs/10c_hip_status.png", dpi=150, bbox_inches="tight", facecolor=BG)
# plt.close()
# print("Saved 10c_hip_status.png")

# # ──────────────────────────────────────────────────────────────
# # PRINT KEY STATS for the slide commentary
# # ──────────────────────────────────────────────────────────────
# print("\n── KEY STATS ──")
# print(f"Total projects: {len(df)}")
# print(f"Total KM:       {df['KM'].sum():.1f}")
# print(f"\nStatus breakdown:")
# print(df.groupby("Status")["KM"].agg(count="count", km_sum="sum").round(1))
# print(f"\nRegion breakdown:")
# print(df.groupby("Region")["KM"].sum().sort_values(ascending=False).round(1))
# print(f"\nTop 5 work types by KM:")
# print(df.groupby("WorkType")["KM"].sum().sort_values(ascending=False).head(5).round(1))