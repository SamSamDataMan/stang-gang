from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

df = pd.read_excel("Data.xlsx", usecols=["Date", "Fancy App", "The Micros"])
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

# Rotate x-axis labels and set smaller font
ax.tick_params(axis="x", rotation=45, labelsize=8)

# Format dates as mm/dd/yy
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d/%y"))

ax.set_ylim(lower, upper)
ax.set_xlabel("Date")
ax.set_ylabel("Gleanings ($)")
ax.legend()
ax.grid(True, alpha=0.3)

st.pyplot(fig)

# Spotify embed link (user has to click Play)
spotify_embed_url = "https://open.spotify.com/embed/track/563vSy3HB5NHxel1VGQCW6"

songs = {
    "Still Fly — Big Tymers": "https://open.spotify.com/embed/track/563vSy3HB5NHxel1VGQCW6",
    "Rack City — Tyga": "https://open.spotify.com/embed/track/0srwKuJPH8yBzzFUJMBQM2",
    "Gimme the Loot — The Notorious B.I.G.": "https://open.spotify.com/embed/track/1xIxMz1sNQ4b6svH1GuTtF",
    "Maybach Music 2 — Rick Ross": "https://open.spotify.com/embed/track/1PSOEWhJXNJ0NpjgedMqZ6",
    "Gazillion Ear — MF DOOM": "https://open.spotify.com/embed/track/5KeW2rotY0Gdsml5RPOBN8",
}

# Step 2: Create dropdown
selected_song = st.selectbox("Choose a song", list(songs.keys()))

# Step 3: Show Spotify player for the selected song
spotify_embed_url = songs[selected_song]
components.iframe(spotify_embed_url, width=300, height=80)
