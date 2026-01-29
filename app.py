import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from statsbombpy import sb
from mplsoccer import Pitch, VerticalPitch, Sbopen
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as path_effects

# --- Page Configuration ---
st.set_page_config(
    page_title="CAN 2023 | Elite Performance Dashboard",
    layout="wide",
    page_icon="⚽"
)

# --- Professional Styling ---
# Font Import
st.markdown('<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# CSS Injection
style_code = """
<style>
    * { font-family: 'Outfit', sans-serif; }
    .stApp { background-color: #0d1117; color: #e6edf3; }
    h1 { color: #f85149 !important; font-weight: 700 !important; letter-spacing: -1px; }
    h2, h3 { color: #f0f6fc !important; border-bottom: 2px solid #30363d; padding-bottom: 10px; }
    section[data-testid="stSidebar"] { background-color: #161b22 !important; border-right: 1px solid #30363d !important; }
    section[data-testid="stSidebar"] label p { color: white !important; font-weight: 600 !important; }
    .metric-card {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-value { font-size: 2rem; font-weight: 700; color: #f85149; }
    .metric-label { font-size: 0.9rem; color: #8b949e; text-transform: uppercase; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background-color: #161b22; padding: 10px; border-radius: 15px; }
    .stTabs [data-baseweb="tab"] {
        height: 45px; color: #8b949e; background-color: transparent; border: none; 
        font-weight: 600; transition: 0.3s;
    }
    .stTabs [aria-selected="true"] { color: #ffffff !important; background-color: #f85149 !important; border-radius: 10px !important; }
    .divider { height: 2px; background: linear-gradient(90deg, #f85149, transparent); margin: 20px 0; }
</style>
"""
st.markdown(style_code, unsafe_allow_html=True)

# --- Constants & Data Loading ---
MATCHES_FILE = 'data/matches.csv'
EVENTS_FILE = 'data/events.csv'
TOUCH_TYPES = ["Pass", "Ball Receipt*", "Carry", "Clearance", "Foul Won", "Block", "Ball Recovery", "Duel", "Dribble", "Interception", "Miscontrol", "Shot"]

@st.cache_data
def load_data():
    if os.path.exists(MATCHES_FILE) and os.path.exists(EVENTS_FILE):
        m = pd.read_csv(MATCHES_FILE)
        e = pd.read_csv(EVENTS_FILE, low_memory=False)
        return m, e
    st.error("Data files missing. Run 'data_extractor.py' first.")
    st.stop()

matches_all, events_all = load_data()

# --- Utility Functions ---
def add_direction_arrow(ax, pitch_type='horizontal'):
    if pitch_type == 'horizontal':
        # Large, clear arrow symbol drawn on top of heatmap/pitch but below labels
        ax.text(60, 40, "⇒", color="#ffffff", ha="center", va="center", 
                size=150, fontweight='bold', alpha=0.15, zorder=2)
    else: # vertical
        # Large, clear arrow symbol for vertical pitch
        ax.text(40, 60, "⇑", color="#ffffff", ha="center", va="center", 
                size=150, fontweight='bold', alpha=0.15, zorder=2)

def style_plt(fig, ax):
    fig.patch.set_facecolor('#0d1117')
    ax.set_facecolor('#161b22')
    ax.tick_params(colors='#8b949e', which='both')
    ax.xaxis.label.set_color('#8b949e')
    ax.yaxis.label.set_color('#8b949e')
    ax.title.set_color('#f0f6fc')
    for spine in ax.spines.values():
        spine.set_edgecolor('#30363d')

# --- Sidebar ---
with st.sidebar:
    st.title("🏆 Elite CAN 2023")
    teams = sorted(pd.concat([matches_all['home_team'], matches_all['away_team']]).unique())
    sel_team = st.selectbox("Sélection de l'Équipe", teams, index=teams.index("Morocco") if "Morocco" in teams else 0)
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    team_m = matches_all[(matches_all["home_team"] == sel_team) | (matches_all["away_team"] == sel_team)].sort_values(by="match_date", ascending=False)
    m_options = team_m.apply(lambda r: f"{r.home_team} vs {r.away_team} ({r.match_date})", axis=1).tolist()
    sel_m_names = st.multiselect("Filtre des Matchs", options=m_options, default=m_options)
    sel_m_ids = team_m[team_m.apply(lambda r: f"{r.home_team} vs {r.away_team} ({r.match_date})", axis=1).isin(sel_m_names)]['match_id'].tolist()
    
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    
    t_events = events_all[(events_all.team == sel_team) & (events_all.match_id.isin(sel_m_ids))]
    players = sorted(t_events.player.dropna().unique().tolist())
    sel_player = st.selectbox("Analyse Joueur", players)

if not sel_m_ids:
    st.warning("Veuillez sélectionner au moins un match.")
    st.stop()

# --- Main Dashboard ---
st.markdown(f"<h1>{sel_team.upper()} : DASHBOARD ANALYTIQUE</h1>", unsafe_allow_html=True)

# Top Bar Metrics
m1, m2, m3, m4 = st.columns(4)
total_passes = len(t_events[t_events.type == "Pass"])
success_rate = (len(t_events[(t_events.type == "Pass") & (t_events.pass_outcome.isna())]) / total_passes * 100) if total_passes > 0 else 0
total_shoots = len(t_events[t_events.type == "Shot"])
high_intensity = len(t_events[t_events.type.isin(["Dribble", "Interception", "Ball Recovery"])])

m1.markdown(f"<div class='metric-card'><div class='metric-label'>Passes Totales</div><div class='metric-value'>{total_passes}</div></div>", unsafe_allow_html=True)
m2.markdown(f"<div class='metric-card'><div class='metric-label'>Précision %</div><div class='metric-value'>{success_rate:.1f}%</div></div>", unsafe_allow_html=True)
m3.markdown(f"<div class='metric-card'><div class='metric-label'>Tirs au But</div><div class='metric-value'>{total_shoots}</div></div>", unsafe_allow_html=True)
m4.markdown(f"<div class='metric-card'><div class='metric-label'>Actions Défensives</div><div class='metric-value'>{high_intensity}</div></div>", unsafe_allow_html=True)

tab_t, tab_p, tab_n = st.tabs(["📊 ANALYSE D'ÉQUIPE", "👤 GÉOMÉTRIE JOUEUR", "🕸️ RÉSEAU TACTIQUE"])

# TAB 1: TEAM ANALYTICS
with tab_t:
    st.subheader("Progression Collective (Dernier Tiers)")
    c1, c2 = st.columns(2)
    
    f3_p = t_events[(t_events.type == "Pass") & (t_events.x < 80) & (t_events.pass_end_x > 80) & (t_events.pass_outcome.isna())]
    f3_c = t_events[(t_events.type == "Carry") & (t_events.x < 80) & (t_events.carry_end_x > 80)]
    p_df = pd.merge(f3_p.groupby("player").size().reset_index(name="P"), f3_c.groupby("player").size().reset_index(name="C"), on="player", how="outer").fillna(0)
    p_df["Total"] = p_df["P"] + p_df["C"]
    p_df = p_df.sort_values(by="Total", ascending=False).head(12)

    with c1:
        st.write("**Entrées Totales (Passes + Carries)**")
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.barplot(x="Total", y="player", data=p_df, palette="Reds_d", ax=ax)
        style_plt(fig, ax)
        st.pyplot(fig)
    
    with c2:
        st.write("**Répartition par Méthode**")
        fig, ax = plt.subplots(figsize=(10, 7))
        m_p_df = p_df.melt(id_vars="player", value_vars=["P", "C"])
        sns.barplot(x="value", y="player", hue="variable", data=m_p_df, palette={"P": "#f85149", "C": "#30363d"}, ax=ax)
        ax.legend(title="Type", labels=["Passes", "Carries"], facecolor='#161b22', edgecolor='#30363d', labelcolor='white')
        style_plt(fig, ax)
        st.pyplot(fig)

    st.markdown("<br>", unsafe_allow_html=True)
    c3, c4 = st.columns(2)
    
    with c3:
        st.write("**Passes vers le Dernier Tiers**")
        p_df_p = p_df.sort_values(by="P", ascending=False)
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.barplot(x="P", y="player", data=p_df_p, palette="Blues_d", ax=ax)
        style_plt(fig, ax)
        st.pyplot(fig)
        
    with c4:
        st.write("**Carries vers le Dernier Tiers**")
        p_df_c = p_df.sort_values(by="C", ascending=False)
        fig, ax = plt.subplots(figsize=(10, 7))
        sns.barplot(x="C", y="player", data=p_df_c, palette="Greens_d", ax=ax)
        style_plt(fig, ax)
        st.pyplot(fig)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.subheader("Intensité Spatiale Collective")
    h_ev = st.selectbox("Action Team", TOUCH_TYPES)
    h_df = t_events[t_events.type == h_ev].dropna(subset=['x', 'y'])
    
    # Force full pitch markings
    vp = VerticalPitch(pitch_type="statsbomb", line_color="#8b949e", pitch_color='#161b22', linewidth=2, line_zorder=2)
    cmap = LinearSegmentedColormap.from_list("", ["#161b22", "#30363d", "#f85149"])
    
    fig, ax = vp.draw(figsize=(8, 10))
    if not h_df.empty:
        bs = vp.bin_statistic(h_df.x, h_df.y, statistic="count", bins=(6, 4), normalize=True)
        vp.heatmap(bs, ax=ax, cmap=cmap)
        vp.label_heatmap(bs, color="white", path_effects=[path_effects.Stroke(linewidth=1.5, foreground="black"), path_effects.Normal()], fontsize=18, ax=ax, str_format="{:.0%}", exclude_zeros=True)
    add_direction_arrow(ax, 'vertical')
    st.pyplot(fig)

# TAB 2: PLAYER GEOMETRY
with tab_p:
    st.subheader(f"Profil Stratégique : {sel_player}")
    
    ca, cb = st.columns(2)
    # Force full pitch markings for horizontal pitch
    hp = Pitch(pitch_type='statsbomb', pitch_color='#161b22', line_color='#8b949e', linewidth=2, line_zorder=2)
    pl_p = t_events[(t_events.player == sel_player) & (t_events.type == "Pass")]
    
    with ca:
        st.write("**Passes Réussies**")
        suc = pl_p[pl_p.pass_outcome.isna()]
        fig, ax = hp.draw(figsize=(10, 7))
        if not suc.empty:
            hp.arrows(suc.x, suc.y, suc.pass_end_x, suc.pass_end_y, color='#2ea043', ax=ax, width=1.5, headwidth=4, alpha=0.8)
            hp.scatter(suc.pass_end_x, suc.pass_end_y, color='#2ea043', s=20, ax=ax, alpha=0.6)
        add_direction_arrow(ax, 'horizontal')
        st.pyplot(fig)
        
    with cb:
        st.write("**Passes Manquées**")
        inc = pl_p[pl_p.pass_outcome == "Incomplete"]
        fig, ax = hp.draw(figsize=(10, 7))
        if not inc.empty:
            hp.arrows(inc.x, inc.y, inc.pass_end_x, inc.pass_end_y, color='#f85149', ax=ax, width=1.5, headwidth=4, alpha=0.8)
        add_direction_arrow(ax, 'horizontal')
        st.pyplot(fig)

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.subheader("Carte de Densité Individuelle")
    p_h_ev = st.selectbox("Action Joueur", TOUCH_TYPES, key="p_h_ev")
    p_ev_df = t_events[(t_events.player == sel_player) & (t_events.type == p_h_ev)].dropna(subset=['x', 'y'])
    
    fig, ax = vp.draw(figsize=(8, 10))
    if not p_ev_df.empty:
        bs = vp.bin_statistic(p_ev_df.x, p_ev_df.y, statistic="count", bins=(6, 4), normalize=True)
        vp.heatmap(bs, ax=ax, cmap=cmap)
        vp.label_heatmap(bs, color="white", path_effects=[path_effects.Stroke(linewidth=1.5, foreground="black"), path_effects.Normal()], fontsize=18, ax=ax, str_format="{:.0%}", exclude_zeros=True)
    add_direction_arrow(ax, 'vertical')
    st.pyplot(fig)

# TAB 3: TACTICAL NETWORK
with tab_n:
    net_m_id = st.selectbox("Match Context", options=sel_m_ids, 
                            format_func=lambda x: team_m[team_m.match_id == x].apply(lambda r: f"{r.home_team} vs {r.away_team}", axis=1).values[0])
    
    with st.spinner("Décodage de la géométrie tactile..."):
        parser = Sbopen()
        df, _, _, _ = parser.event(net_m_id)
        df_t = df[df['team_name'] == sel_team]
        
        pass_df = df_t[df_t['type_name'] == 'Pass'].copy()
        pass_df['outcome_name'] = pass_df['outcome_name'].fillna('Successful')
        
        st.subheader("Distribution des Passes")
        fig, ax = plt.subplots(figsize=(10, 4))
        pass_df['outcome_name'].value_counts().plot(kind='barh', color='#f85149', ax=ax)
        style_plt(fig, ax)
        st.pyplot(fig)
        
        suc_p = pass_df[pass_df['outcome_name'] == 'Successful']
        first_s = df_t[df_t['type_name'] == 'Substitution']['minute'].min()
        if pd.isna(first_s): first_s = 90
        
        nw = suc_p[suc_p['minute'] < first_s]
        avg = nw.groupby('player_name').agg(x=('x', 'mean'), y=('y', 'mean'), count=('id', 'size')).reset_index()
        btn = nw.groupby(['player_name', 'pass_recipient_name']).size().reset_index(name='cnt')
        btn = btn.merge(avg, left_on='player_name', right_on='player_name')
        btn = btn.merge(avg, left_on='pass_recipient_name', right_on='player_name', suffixes=['', '_end'])
        
        st.subheader(f"Réseau Tactique (Avant 1er changement : {int(first_s)}')")
        # Full pitch markings for network
        np_pitch = Pitch(pitch_type='custom', pitch_length=120, pitch_width=80, pitch_color='#0d1117', line_color='#8b949e', linewidth=2, line_zorder=2)
        fig, ax = np_pitch.draw(figsize=(12, 8))
        
        np_pitch.lines(1.2 * btn.x, 0.8 * btn.y, 1.2 * btn.x_end, 0.8 * btn.y_end,
                      lw=btn['cnt'] * 0.5, color='#f85149', ax=ax, alpha=0.5, zorder=1)
        np_pitch.scatter(1.2 * avg.x, 0.8 * avg.y, s=30 * avg['count'], color='#161b22', edgecolors='#f85149', linewidth=2, ax=ax, zorder=2)
        
        for i, row in avg.iterrows():
            ax.annotate(row.player_name.split()[-1], xy=(1.2 * row.x, 0.8 * row.y), c='white', weight='bold', size=10, ha='center', va='center')
        
        add_direction_arrow(ax, 'horizontal')
        st.pyplot(fig)

st.sidebar.markdown("---")
st.sidebar.caption("Source : StatsBomb Data")
