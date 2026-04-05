import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import base64
import pickle

csv_path = "players_data_light-2024_2025.csv"
bg_path = "background.jpeg"

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(page_title="Football Analytics", layout="wide")

# ==============================
# BACKGROUND IMAGE FUNCTION
# ==============================

def set_bg(image_file):

    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    bg_css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/webp;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    [data-testid="stTable"] {{
        background-color: transparent !important;
    }}
    [data-testid="stTable"] th, [data-testid="stTable"] td {{
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: white !important;
    }}
    </style>
    """

    st.markdown(bg_css, unsafe_allow_html=True)


# ==============================
# SET BACKGROUND IMAGE
# ==============================

set_bg(bg_path)

# ==============================
# LOAD DATA
# ==============================

df = pd.read_csv(csv_path)

df = df.dropna(subset=["League","Squad","Player"])

# ==============================
# LOAD CLUSTERING MODEL
# ==============================

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

outfield = model['outfield']

# ==============================
# TITLE
# ==============================

st.title(" Football Player Analytics Dashboard")

# ==============================
# SIDEBAR
# ==============================

league = st.sidebar.selectbox(
"Select League",
sorted(df["League"].unique())
)

teams = df[df["League"]==league]["Squad"].unique()

team = st.sidebar.selectbox(
"Select Team",
sorted(teams)
)

players = df[df["Squad"]==team]["Player"].unique()

player = st.sidebar.selectbox(
"Select Player",
sorted(players)
)

analysis = st.sidebar.selectbox(
"Select Analysis",
[
"Player Comparison",
"Radar Chart",
"Radar Chart Player Comparison",
"xG vs Goals",
"Percentile Chart",
"Similar Players"
]
)

player_row = df[df["Player"]==player].iloc[0]

# ==============================
# PLAYER COMPARISON
# ==============================

if analysis == "Player Comparison":

    stat = st.selectbox(
    "Select Stat",
    ["Gls","Ast","xG","xA","SoT","KP","PrgC"]
    )

    compare_type = st.radio(
    "Compare With",
    ["League","Overall"]
    )

    if compare_type == "League":
        dataset = df[df["League"] == player_row["League"]]
        title_scope = "League"
    else:
        dataset = df
        title_scope = "Overall"

    dataset = dataset.sort_values(stat, ascending=False)
    top14 = dataset.head(14)
    player_data = dataset[dataset["Player"] == player]
    combined = pd.concat([top14, player_data]).drop_duplicates(subset="Player")

    fig, ax = plt.subplots(figsize=(12,6))
    fig.patch.set_facecolor((0, 0, 0, 0.6))
    ax.set_facecolor((0, 0, 0, 0.6))

    bars = ax.bar(combined["Player"], combined[stat])

    for i,p in enumerate(combined["Player"]):
        if p == player:
            bars[i].set_edgecolor("white")
            bars[i].set_linewidth(3)

    plt.xticks(rotation=45)
    ax.set_title(player + " vs " + title_scope + " (" + stat + ")")
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(colors='white')
    st.pyplot(fig)

# ==============================
# RADAR CHART
# ==============================

elif analysis == "Radar Chart":

    radar_stats = ["Gls","Ast","xG","xA","SoT"]
    labels = ["Goals","Assists","xG","xA","Shots on Target"]

    values = [player_row[s] for s in radar_stats]
    angles = np.linspace(0,2*np.pi,len(radar_stats),endpoint=False)
    values = np.concatenate((values,[values[0]]))
    angles = np.concatenate((angles,[angles[0]]))

    fig = plt.figure(figsize=(12,6))
    ax = fig.add_subplot(111, polar=True)
    fig.patch.set_facecolor((0, 0, 0, 0.6))
    ax.set_facecolor((0, 0, 0, 0.6))
    ax.plot(angles,values,linewidth=2)
    ax.fill(angles,values,alpha=0.3)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color='white')
    ax.tick_params(colors='white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')
    plt.title(player+" Radar Chart", color='white')
    st.pyplot(fig)

# ==============================
# RADAR PLAYER COMPARISON
# ==============================

elif analysis == "Radar Chart Player Comparison":

    radar_stats = ["Gls","Ast","xG","xA","SoT"]
    labels = ["Goals","Assists","xG","xA","Shots on Target"]

    league1 = st.sidebar.selectbox("Select League for Player 1", df["League"].unique())
    players1 = df[df["League"] == league1]["Player"].unique()
    player1 = st.sidebar.selectbox("Select Player 1", players1)

    league2 = st.sidebar.selectbox("Select League for Player 2", df["League"].unique())
    players2 = df[df["League"] == league2]["Player"].unique()
    player2 = st.sidebar.selectbox("Select Player 2", players2)

    p1 = df[df["Player"]==player1].iloc[0]
    p2 = df[df["Player"]==player2].iloc[0]

    values1 = [p1[s] for s in radar_stats]
    values2 = [p2[s] for s in radar_stats]
    angles = np.linspace(0,2*np.pi,len(radar_stats),endpoint=False)
    values1 = np.concatenate((values1,[values1[0]]))
    values2 = np.concatenate((values2,[values2[0]]))
    angles = np.concatenate((angles,[angles[0]]))

    fig = plt.figure(figsize=(12,6))
    ax = fig.add_subplot(111, polar=True)
    fig.patch.set_facecolor((0, 0, 0, 0.6))
    ax.set_facecolor((0, 0, 0, 0.6))

    ax.plot(angles,values1,linewidth=2,label=player1)
    ax.fill(angles,values1,alpha=0.25)
    ax.plot(angles,values2,linewidth=2,label=player2)
    ax.fill(angles,values2,alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, color='white')
    ax.tick_params(colors='white')
    ax.yaxis.label.set_color('white')
    plt.title(player1+" vs "+player2+" Radar Comparison", color='white')
    legend = plt.legend(loc="upper right")
    for text in legend.get_texts():
        text.set_color('white')
    legend.get_frame().set_facecolor((0, 0, 0, 0.6))
    st.pyplot(fig)

# ==============================
# xG VS GOALS
# ==============================

elif analysis == "xG vs Goals":

    fig, ax = plt.subplots(figsize=(12,6))
    fig.patch.set_facecolor((0, 0, 0, 0.6))
    ax.set_facecolor((0, 0, 0, 0.6))

    ax.scatter(df["xG"],df["Gls"], alpha=0.5)
    ax.scatter(player_row["xG"],player_row["Gls"],s=150, color='red', zorder=5, label=player)

    ax.set_xlabel("Expected Goals (xG)")
    ax.set_ylabel("Goals")
    ax.set_title("xG vs Goals")
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(colors='white')
    legend = ax.legend()
    for text in legend.get_texts():
        text.set_color('white')
    legend.get_frame().set_facecolor((0, 0, 0, 0.6))
    st.pyplot(fig)

# ==============================
# PERCENTILE CHART
# ==============================

elif analysis == "Percentile Chart":

    stats = ["Gls","Ast","xG","xA"]
    labels = ["Goals","Assists","xG","xA"]

    league_data = df[df["League"]==player_row["League"]]
    percentiles = []

    for s in stats:
        value = player_row[s]
        percentile = (league_data[s] < value).mean()*100
        percentiles.append(percentile)

    fig, ax = plt.subplots(figsize=(12,6))
    fig.patch.set_facecolor((0, 0, 0, 0.6))
    ax.set_facecolor((0, 0, 0, 0.6))

    ax.bar(labels,percentiles)
    ax.set_ylabel("Percentile")
    ax.set_title(player+" Percentile vs League")
    ax.title.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(colors='white')
    st.pyplot(fig)

# ==============================
# SIMILAR PLAYERS
# ==============================

elif analysis == "Similar Players":

    matches = outfield[outfield['Player'].str.contains(player, case=False)]

    if not matches.empty:

        idx = matches.index[0]
        target = outfield.loc[idx]

        distances = np.sqrt(
            (outfield['umap_x'] - target['umap_x'])**2 +
            (outfield['umap_y'] - target['umap_y'])**2
        )

        similar = outfield.loc[distances.nsmallest(6).index[1:]]

        st.subheader(f"Top 5 similar players to {player}")

        st.table(
            similar[['Player','Squad','League','Pos','Age']].reset_index(drop=True)
        )

    else:
        st.write("Player not found in clustering data.")
