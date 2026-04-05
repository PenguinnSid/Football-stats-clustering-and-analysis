import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# PAGE TITLE
st.title("⚽ Football Player Analytics Dashboard")

# LOAD DATA
df = pd.read_csv("players_data_light-2024_2025.csv")

df = df.dropna(subset=["League","Squad","Player"])

# ----------------------------
# SIDEBAR FILTERS
# ----------------------------

st.sidebar.header("Filters")

league = st.sidebar.selectbox(
    "Select League",
    df["League"].unique()
)

teams = df[df["League"] == league]["Squad"].unique()

team = st.sidebar.selectbox(
    "Select Team",
    teams
)

players = df[df["Squad"] == team]["Player"].unique()

player = st.sidebar.selectbox(
    "Select Player",
    players
)

analysis = st.sidebar.selectbox(
    "Select Analysis",
    ["Player Comparison","Radar Chart","Radar Chart Player Comparision","xG vs Goals","Percentile"]
)

player_row = df[df["Player"] == player].iloc[0]

# ----------------------------
# PLAYER COMPARISON
# ----------------------------

if analysis == "Player Comparison":

    stat = st.selectbox(
        "Select Stat",
        ["Gls","Ast","xG","xA","SoT","KP","PrgC"]
    )

    league_players = df[df["League"] == player_row["League"]]

    top = league_players.sort_values(stat, ascending=False).head(15)

    fig, ax = plt.subplots(figsize=(10,5))

    bars = ax.bar(top["Player"], top[stat])

    for i,p in enumerate(top["Player"]):
        if p == player:
            bars[i].set_edgecolor("black")
            bars[i].set_linewidth(3)

    plt.xticks(rotation=45)

    ax.set_title(player + " vs League (" + stat + ")")

    st.pyplot(fig)

# ----------------------------
# RADAR CHART
# ----------------------------

elif analysis == "Radar Chart":

    radar_stats = ["Gls","Ast","xG","xA","SoT"]

    labels = ["Goals","Assists","xG","xA","Shots on Target"]

    values = [player_row[s] for s in radar_stats]

    angles = np.linspace(0,2*np.pi,len(radar_stats),endpoint=False)

    values = np.concatenate((values,[values[0]]))
    angles = np.concatenate((angles,[angles[0]]))

    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111,polar=True)

    ax.plot(angles,values)
    ax.fill(angles,values,alpha=0.3)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    plt.title(player + " Radar Chart")

    st.pyplot(fig)

    #-------------------------------
    # Radar Chart Player Comparision
    #-------------------------------
    
elif analysis == "Radar Chart Player Comparision":

    radar_stats = ["Gls","Ast","xG","xA","SoT"]
    labels = ["Goals","Assists","xG","xA","Shots on Target"]

    # League selection for Player 1
    league1 = st.sidebar.selectbox("Select League for Player 1", df["League"].unique())
    players1 = df[df["League"] == league1]["Player"].unique()

    player1 = st.sidebar.selectbox("Select Player 1", players1)

    # League selection for Player 2
    league2 = st.sidebar.selectbox("Select League for Player 2", df["League"].unique())
    players2 = df[df["League"] == league2]["Player"].unique()

    player2 = st.sidebar.selectbox("Select Player 2", players2)

    p1 = df[df["Player"] == player1].iloc[0]
    p2 = df[df["Player"] == player2].iloc[0]

    values1 = [p1[s] for s in radar_stats]
    values2 = [p2[s] for s in radar_stats]

    angles = np.linspace(0,2*np.pi,len(radar_stats),endpoint=False)

    values1 = np.concatenate((values1,[values1[0]]))
    values2 = np.concatenate((values2,[values2[0]]))
    angles = np.concatenate((angles,[angles[0]]))

    fig = plt.figure(figsize=(7,7))
    ax = fig.add_subplot(111, polar=True)

    ax.plot(angles,values1,linewidth=2,label=player1)
    ax.fill(angles,values1,alpha=0.25)

    ax.plot(angles,values2,linewidth=2,label=player2)
    ax.fill(angles,values2,alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    plt.title(player1 + " vs " + player2 + " Radar Comparison")
    plt.legend(loc="upper right")

    st.pyplot(fig)
# ----------------------------
# xG vs GOALS
# ----------------------------

elif analysis == "xG vs Goals":

    fig, ax = plt.subplots()

    ax.scatter(df["xG"], df["Gls"], alpha=0.5)

    ax.set_xlabel("Expected Goals (xG)")
    ax.set_ylabel("Goals")

    ax.set_title("xG vs Goals")

    st.pyplot(fig)

# ----------------------------
# PERCENTILE CHART
# ----------------------------

elif analysis == "Percentile":

    stats = ["Gls","Ast","xG","xA"]

    labels = ["Goals","Assists","xG","xA"]

    league_data = df[df["League"] == player_row["League"]]

    percentiles = []

    for s in stats:

        value = player_row[s]

        percentile = (league_data[s] < value).mean() * 100

        percentiles.append(percentile)

    fig, ax = plt.subplots()

    ax.bar(labels, percentiles)

    ax.set_ylabel("Percentile")

    ax.set_title(player + " Percentile vs League")

    st.pyplot(fig)