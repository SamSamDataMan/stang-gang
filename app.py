import random
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

df = pd.read_excel("Data.xlsx", usecols=["Date", "Fancy App", "The Micros"])
df["Date"] = pd.to_datetime(df["Date"])

# Create a display-only version with date stripped
df_display = df.copy()
df_display["Date"] = df_display["Date"].dt.date

# --- SIDEBAR ---
st.sidebar.write("### Data Table")
st.sidebar.dataframe(df_display, use_container_width=True, hide_index=True)

# --- MAIN PAGE ---
df_plot = df.set_index("Date").sort_index()

# Compute min/max across all numeric columns
y_min = df_plot.min().min()
y_max = df_plot.max().max()

# 10% padding
padding = 0.10 * (y_max - y_min if y_max != y_min else max(abs(y_max), 1))
lower = y_min - padding
upper = y_max + padding


def hex_to_rgb(color_value):
    color_value = (color_value or "").lstrip("#")
    if len(color_value) != 6:
        return (15, 23, 42)
    return tuple(int(color_value[i:i + 2], 16) for i in (0, 2, 4))


def rgba(color_value, alpha):
    red, green, blue = hex_to_rgb(color_value)
    return f"rgba({red}, {green}, {blue}, {alpha})"


theme_base = st.get_option("theme.base") or "light"
is_dark_mode = theme_base == "dark"
theme_background = st.get_option("theme.backgroundColor") or ("#0E1117" if is_dark_mode else "#FFFFFF")
theme_text = st.get_option("theme.textColor") or ("#F9FAFB" if is_dark_mode else "#111827")

chart_colors = {
    "paper_bg": rgba(theme_background, 0),
    "plot_bg": "rgba(198, 205, 214, 0.18)" if is_dark_mode else "rgba(215, 221, 228, 0.82)",
    "grid": rgba(theme_text, 0.12 if is_dark_mode else 0.14),
    "zero": rgba(theme_text, 0.22 if is_dark_mode else 0.24),
    "text": theme_text,
    "hover_bg": "rgba(31, 41, 55, 0.96)" if is_dark_mode else "rgba(255, 255, 255, 0.98)",
    "border": rgba(theme_text, 0.22),
    "axis": rgba(theme_text, 0.32),
}

# Make the plot
fig = go.Figure()

color_map = {
    "The Micros": "#2E7D32",  # money green
    "Fancy App": "#0B1F5E",   # dark blue
}

for column in df_plot.columns:
    series = df_plot[column]
    color = color_map.get(column)

    # Draw a continuous line by forward-filling gaps
    line_series = series.ffill()
    fig.add_trace(
        go.Scatter(
            x=df_plot.index,
            y=line_series,
            mode="lines",
            name=column,
            line={"color": color, "width": 3},
            hoverinfo="skip",
        )
    )

    # Only show markers when the value changes (and exists)
    change_mask = series.notna() & (series != series.shift())
    fig.add_trace(
        go.Scatter(
            x=df_plot.index[change_mask],
            y=series[change_mask],
            mode="markers",
            marker={"color": color, "size": 9},
            name=column,
            showlegend=False,
            customdata=[column] * int(change_mask.sum()),
            hovertemplate=(
                "%{customdata}<br>"
                "Date: %{x|%m/%d/%y}<br>"
                "Value: $%{y:,.0f}"
                "<extra></extra>"
            ),
        )
    )

fig.update_layout(
    title={
        "text": "<b>Software Development vs Unbridled Degeneracy</b>",
        "x": 0.5,
        "xanchor": "center",
        "font": {"size": 24},
    },
    xaxis_title="<b>Date</b>",
    yaxis_title="<b>Gleanings ($)</b>",
    yaxis={"range": [lower, upper], "tickformat": "$,.0f"},
    xaxis={"tickformat": "%m/%d/%y"},
    hovermode="closest",
    paper_bgcolor=chart_colors["paper_bg"],
    plot_bgcolor=chart_colors["plot_bg"],
    font={"color": chart_colors["text"], "size": 14},
    hoverlabel={
        "bgcolor": chart_colors["hover_bg"],
        "bordercolor": chart_colors["border"],
        "font": {"color": chart_colors["text"], "size": 14},
    },
    legend_title_text="",
    legend={
        "bgcolor": "rgba(0, 0, 0, 0)",
        "bordercolor": "rgba(0, 0, 0, 0)",
        "orientation": "h",
        "x": 0.5,
        "xanchor": "center",
        "y": 1.03,
        "yanchor": "bottom",
        "font": {"size": 13},
    },
    margin={"l": 72, "r": 40, "t": 110, "b": 72},
)

fig.update_xaxes(
    showgrid=True,
    gridcolor=chart_colors["grid"],
    zeroline=False,
    showline=True,
    linecolor=chart_colors["axis"],
    linewidth=1.5,
    tickfont={"size": 13},
    title_font={"size": 17},
)

fig.update_yaxes(
    showgrid=True,
    gridcolor=chart_colors["grid"],
    zeroline=True,
    zerolinecolor=chart_colors["zero"],
    showline=True,
    linecolor=chart_colors["axis"],
    linewidth=1.5,
    tickfont={"size": 13},
    title_font={"size": 17},
)

st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# Spotify embed link (user has to click Play)
spotify_embed_url = "https://open.spotify.com/embed/track/563vSy3HB5NHxel1VGQCW6"

songs = {
    # "Still Fly — Big Tymers": "https://open.spotify.com/embed/track/563vSy3HB5NHxel1VGQCW6",
    # "Rack City — Tyga": "https://open.spotify.com/embed/track/0srwKuJPH8yBzzFUJMBQM2",
    # "Gimme the Loot — The Notorious B.I.G.": "https://open.spotify.com/embed/track/1xIxMz1sNQ4b6svH1GuTtF",
    # "Maybach Music 2 — Rick Ross": "https://open.spotify.com/embed/track/1PSOEWhJXNJ0NpjgedMqZ6",
    # "Gazillion Ear — MF DOOM": "https://open.spotify.com/embed/track/5KeW2rotY0Gdsml5RPOBN8",
    # "Beautiful Life - Shawn Anthony": "https://open.spotify.com/embed/track/3IgOUvG0HOn2gAscvGffTP",
    # "Rick Ross - The Boss": "https://open.spotify.com/embed/track/67LLvp5hpAtJRZQa7frobT",
    # "Rick Ross - Hustlin'": "https://open.spotify.com/embed/track/3hQCHzkE5oSA3F1xM8bpcM",
    # 'Jay-Z - Allure':'https://open.spotify.com/embed/track/6Sgm6qofFJPJG1A06mzDIb?si=hNi_yqzXRD6zykfUd5Ejcg',
    # 'Marcy Playground - Sex and Candy': 'https://open.spotify.com/embed/track/5mkGfmJGFZpwK9nA5amOhv',
    # 'De La Soul - The Bizness': 'https://open.spotify.com/embed/track/22wlZ0k1c3BSZuZpHkqAnl?si=1be81327c3664146',
    'Fall Out Boy - Sophomore Slump Or Comeback Of The Year': 'https://open.spotify.com/embed/track/1iir1dMidSGRzbPMCCEtfX?si=bdc41c5d60bf4c7e'
}

# Shuffle only once per session
if "shuffled_songs" not in st.session_state:
    st.session_state.shuffled_songs = list(songs.keys())
    random.shuffle(st.session_state.shuffled_songs)

# Use the stable shuffled list
song_list = st.session_state.shuffled_songs

selected_song = st.selectbox("Choose a song", song_list)

# Play the correct URL
components.iframe(songs[selected_song], width=300, height=80)
