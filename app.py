from matplotlib import pyplot as plt
import streamlit as st
import pandas as pd

df = pd.read_excel("Data.xlsx")
df["Date"] = pd.to_datetime(df["Date"])

# Create a display-only version with date stripped
df_display = df.copy()
df_display["Date"] = df_display["Date"].dt.date

# --- SIDEBAR ---
st.sidebar.write("### Data Table")
st.sidebar.dataframe(df_display, use_container_width=True, hide_index=True)

# --- MAIN PAGE ---
df_plot = df.set_index("Date")

# Compute min/max across all numeric columns
y_min = df_plot.min().min()
y_max = df_plot.max().max()

# 10% padding
padding = 0.10 * (y_max - y_min if y_max != y_min else max(abs(y_max), 1))
lower = y_min - padding
upper = y_max + padding

# Make the plot
fig, ax = plt.subplots(figsize=(8, 4))

plt.title("Software Development vs Unbridled Degeneracy")

for column in df_plot.columns:
    ax.plot(df_plot.index, df_plot[column], marker="o", label=column)

ax.set_ylim(lower, upper)
ax.set_xlabel("Date")
ax.set_ylabel("Value")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)
