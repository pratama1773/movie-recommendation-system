"""
Frontend layer of the movie recommendation application using Streamlit.
Handles UI rendering, language localization, and user interactions.
"""

import streamlit as st
import pandas as pd
import functools
import urllib.parse
import re
from deep_translator import GoogleTranslator
from sklearn.metrics.pairwise import cosine_similarity

# Page configuration
st.set_page_config(page_title="Movie Recommender", layout="wide")

@functools.lru_cache(maxsize=10000)
def tr(text: str) -> str:
    """
    Translates text to Indonesian with LRU Cache implementation.
    
    Args:
        text (str): Source text (English).
        
    Returns:
        str: Translated text or original text if an error occurs.
    """
    if not text or pd.isna(text):
        return ""
    
    if st.session_state.get("language", "en") == "id":
        try:
            return GoogleTranslator(source='auto', target='id').translate(str(text))
        except Exception:
            return str(text)
            
    return str(text)

# UI Translation Dictionary
TRANSLATIONS = {
    "en": {
        "app_title": "Movie Recommendation System",
        "app_desc": "Discover your next favorite movie using content similarity, clustering, and Bayesian probability.",
        "sidebar_title": "Filters & Settings",
        "select_genres": "Select genre(s)",
        "genres_help": "Movies must belong to ALL selected genres",
        "min_rating": "Minimum Rating",
        "min_votes": "Minimum Votes",
        "preferred_cluster": "Preferred Cluster",
        "any_cluster": "Any Cluster",
        "cluster_0": "Popular Movie",
        "cluster_1": "Hidden Gem",
        "reset_button": "Reset All Filters",
        "reset_success": "All filters have been reset!",
        "language": "Language",
        "tab_expert": "Expert System",
        "tab_similar": "Similar Movies",
        "tab_clusters": "Explore Clusters",
        "tab_search": "Search",
        "expert_header": "Bayesian Expert System",
        "expert_desc": "Personalized recommendations ranked mathematically to eliminate bias from low-vote anomalies.",
        "top_recommendations": "Top {n} Recommendations",
        "similar_header": "Content-Based Recommendations",
        "similar_desc": "Find movies most similar to the one you love based on plot, genres, and directors.",
        "choose_movie": "Choose a movie",
        "top_similar": "Top 12 movies similar to {title}",
        "clusters_header": "Movie Clusters",
        "clusters_genres": "Select genre(s) for Clusters:",
        "clusters_genres_help": "Filter movies shown in both clusters. Leave empty to see all genres.",
        "sort_votes": "Sort movies by votes:",
        "sort_top": "Top",
        "sort_bottom": "Bottom",
        "centroid_explanation": "Centroid Data: Avg rating ≈ {rating:.2f} | Avg votes ≈ {votes:,.0f}",
        "search_header": "Search Movies",
        "search_desc": "Search movies by title, genre, director, or keywords in the plot.",
        "search_placeholder": "e.g. Inception, Nolan, superhero, love, zombie...",
        "search_results": "Found {n} movies for keyword: '{query}'",
        "genres_label": "Genres",
        "director_label": "Director(s)",
        "writer_label": "Writers",
        "runtime_label": "Runtime",
        "runtime_unit": "min",
        "plot_label": "Plot",
        "cluster_label": "Cluster",
        "expert_score_label": "Expert Score",
        "imdb_link": "View on IMDB",
        "no_imdb": "IMDB Link Not Available",
        "no_poster": "No poster",
        "poster_error": "Poster unavailable",
        "no_movies_genre": "No genre filter applied - showing all movies.",
        "found_movies_genre": "Found {n:,} movies matching selected genre(s).",
        "no_results": "No movies match the current filters.",
        "no_similar": "No similar movies found.",
        "no_movies_available": "No movies available with the current genre filter.",
        "movie_not_found": "Movie '{title}' not found.",
        "detail_btn": "Detail",
        "dialog_title": "Movie Details"
    },
    "id": {
        "app_title": "Sistem Rekomendasi Film",
        "app_desc": "Temukan film favorit berikutnya menggunakan kemiripan konten, pengelompokan, dan probabilitas Bayesian.",
        "sidebar_title": "Filter & Pengaturan",
        "select_genres": "Pilih genre",
        "genres_help": "Film harus termasuk SEMUA genre yang dipilih",
        "min_rating": "Rating Minimum",
        "min_votes": "Minimum Votes",
        "preferred_cluster": "Cluster yang Diinginkan",
        "any_cluster": "Semua Cluster",
        "cluster_0": "Film Populer Berkualitas",
        "cluster_1": "Permata Tersembunyi (Hidden Gem)",
        "reset_button": "Reset Semua Filter",
        "reset_success": "Semua filter telah direset!",
        "language": "Bahasa",
        "tab_expert": "Sistem Pakar",
        "tab_similar": "Film Serupa",
        "tab_clusters": "Jelajahi Cluster",
        "tab_search": "Cari Film",
        "expert_header": "Sistem Pakar Bayesian",
        "expert_desc": "Rekomendasi personal yang diurutkan secara matematis untuk mengeliminasi bias dari anomali film bervote rendah.",
        "top_recommendations": "Rekomendasi Teratas ({n})",
        "similar_header": "Rekomendasi Berdasarkan Konten",
        "similar_desc": "Temukan film yang paling mirip dari segi sinopsis, genre, dan sutradara.",
        "choose_movie": "Pilih film",
        "top_similar": "12 Film paling mirip dengan {title}",
        "clusters_header": "Kelompok Film",
        "clusters_genres": "Pilih genre untuk Cluster:",
        "clusters_genres_help": "Filter film di kedua cluster. Kosongkan untuk melihat semua genre.",
        "sort_votes": "Urutkan berdasarkan votes:",
        "sort_top": "Teratas",
        "sort_bottom": "Terendah",
        "centroid_explanation": "Data Centroid: Rata-rata rating ≈ {rating:.2f} | Rata-rata votes ≈ {votes:,.0f}",
        "search_header": "Cari Film",
        "search_desc": "Cari film berdasarkan judul, genre, sutradara, atau kata kunci di sinopsis.",
        "search_placeholder": "contoh: Inception, Nolan, superhero, cinta, zombie...",
        "search_results": "Ditemukan {n} film untuk kata kunci: '{query}'",
        "genres_label": "Genre",
        "director_label": "Sutradara",
        "writer_label": "Penulis",
        "runtime_label": "Durasi",
        "runtime_unit": "menit",
        "plot_label": "Sinopsis",
        "cluster_label": "Cluster",
        "expert_score_label": "Skor Pakar",
        "imdb_link": "Lihat di IMDB",
        "no_imdb": "Link IMDB Tidak Tersedia",
        "no_poster": "Tanpa poster",
        "poster_error": "Poster tidak tersedia",
        "no_movies_genre": "Tidak ada filter genre - menampilkan semua film.",
        "found_movies_genre": "Ditemukan {n:,} film sesuai genre yang dipilih.",
        "no_results": "Tidak ada film yang cocok dengan filter saat ini.",
        "no_similar": "Tidak ada film serupa ditemukan.",
        "no_movies_available": "Tidak ada film tersedia dengan filter genre saat ini.",
        "movie_not_found": "Film '{title}' tidak ditemukan.",
        "detail_btn": "Detail",
        "dialog_title": "Detail Film"
    }
}

def t(key: str, **kwargs) -> str:
    """Utility function to fetch localized strings based on active state."""
    lang = st.session_state.get("language", "en")
    text = TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
    return text.format(**kwargs) if kwargs else text

# Initialize Language State
if "language" not in st.session_state:
    st.session_state.language = "en"

# Load resources from the backend pipeline
from utils.preprocessing import load_and_preprocess_data

try:
    data = load_and_preprocess_data("data/movie.csv", sep=';', encoding='utf-8')
    movies       = data['movies']
    tfidf_matrix = data['tfidf_matrix'] 
    all_genres   = data['all_genres']
    cluster_map  = data['cluster_map']  
except Exception as e:
    st.error(f"Error while loading data: {e}")
    st.stop()

# Mathematical K-Means dynamic IDs
POPULAR_ID = cluster_map['popular_id']
HIDDEN_GEM_ID = cluster_map['hidden_gem_id']

# Default form controls
defaults = {
    'selected_genres': [], 
    'rating_min': 0.0, 
    'votes_min': 0, 
    'preferred_cluster': None
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

def reset_filters():
    """Reset filter values in the session state to default mode."""
    for key, val in defaults.items():
        st.session_state[key] = val

# CSS injection for visual component customization
st.markdown("""
<style>
    /* Main Area Banner Element */
    .title-banner {
        background: linear-gradient(135deg, rgba(15, 32, 39, 0.85), rgba(32, 58, 67, 0.85), rgba(44, 83, 100, 0.85)), 
                    url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1920&q=80') center/cover no-repeat;
        padding: 3rem 2rem; border-radius: 8px; text-align: center; margin-bottom: 2.5rem;
        border-bottom: 3px solid #0ea5e9; box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .title-banner h1 { color: #ffffff !important; font-size: 2.5rem !important; font-weight: 700 !important; margin: 0 0 8px 0 !important; letter-spacing: 0.5px; }
    .title-banner p { color: #bae6fd !important; font-size: 1.05rem !important; margin: 0 !important; font-weight: 400; }

    /* Badge and Plot elements restored to solid colors to ensure visibility in any theme */
    .movie-badge {
        display: inline-block; padding: 0.4em 0.8em; font-size: 0.8em; font-weight: 600; border-radius: 4px;
        margin-right: 0.5em; margin-bottom: 0.5em; letter-spacing: 0.5px; text-transform: uppercase;
        background-color: #334155 !important; color: #ffffff !important; border: 1px solid #475569;
    }
    
    .badge-expert {
        background-color: #b45309 !important; color: #ffffff !important; border: 1px solid #d97706; 
    }

    .movie-plot {
        text-align: justify; line-height: 1.7; font-size: 14px;
        margin-top: 1.5rem; margin-bottom: 1.5rem; padding: 16px 20px;
        background-color: #1e293b !important; color: #ffffff !important; border-left: 3px solid #64748b; border-radius: 4px;
    }
    
    /* Meta and Titles are not forced to a specific color to automatically adapt to Streamlit's Light/Dark themes */
    .movie-meta { font-size: 0.95em; margin-bottom: 8px; }
    .movie-meta strong { font-weight: 600; }
    
    .card-title {
        font-size: 1.6rem; font-weight: 700; margin-top: 0; margin-bottom: 1rem;
        border-bottom: 1px solid rgba(128, 128, 128, 0.3); padding-bottom: 0.8rem;
    }

    .poster-container {
        width: 100%; padding-top: 150%; position: relative; border-radius: 4px;
        overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.2); background-color: #333333; margin-bottom: 15px; border: 1px solid rgba(128, 128, 128, 0.2);
    }
    .poster-container img {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; transition: transform 0.4s ease;
    }
    .poster-container:hover img { transform: scale(1.03); }
    
    .grid-title {
        font-weight: 600; font-size: 14px; height: 42px; overflow: hidden; text-overflow: ellipsis;
        display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; text-align: center; 
        margin-bottom: 5px; line-height: 1.5;
    }
    
    /* ========================================================
       SIDEBAR FIX: Securing a Professional Dark Color Scheme 
       ======================================================== */
    [data-testid="stSidebar"] { 
        background-color: #0f172a !important; /* Dark Navy Blue */
        border-right: 1px solid #1e293b !important; 
    }
    /* Forcing header and label texts inside Sidebar to be white/light */
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] .stMarkdown {
        color: #f8fafc !important; 
    }
    /* Customizing navigation buttons in the Sidebar */
    [data-testid="stSidebar"] button[kind="secondary"] {
        background-color: #1e293b !important;
        color: #cbd5e1 !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important; 
        font-weight: 600 !important; 
        width: 100% !important; 
        transition: all 0.2s;
    }
    [data-testid="stSidebar"] button[kind="secondary"]:hover {
        background-color: #334155 !important;
        color: #ffffff !important;
        border-color: #475569 !important;
    }
    [data-testid="stSidebar"] button[kind="primary"] {
        background-color: #0ea5e9 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
    }
    /* ======================================================== */
    
    /* Main Tabs Configuration */
    .stTabs [data-baseweb="tab-list"] { gap: 4px; background-color: transparent; border-bottom: 1px solid rgba(128, 128, 128, 0.2); }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important; border-radius: 4px 4px 0 0 !important; padding: 10px 20px !important;
        border: none !important; border-bottom: 2px solid transparent !important; transition: 0.2s ease;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: transparent !important; color: #0ea5e9 !important;
        border-color: #0ea5e9 !important; font-weight: 600 !important; box-shadow: none;
    }
</style>
""", unsafe_allow_html=True)

def get_translated_cluster_name(cluster_id: int) -> str:
    """Resolve mathematical cluster ID to string format."""
    if cluster_id == POPULAR_ID:
        return t("cluster_0")
    return t("cluster_1")

def render_movie_details(row: pd.Series, t_func: callable, tr_func: callable):
    """
    Build the HTML UI structure for movie details.
    
    Args:
        row (pd.Series): Series object from a single DataFrame row containing movie metadata.
        t_func (callable): Function for local string translation.
        tr_func (callable): Function for description translation.
    """
    col1, col2 = st.columns([3, 1])
    cluster_name = get_translated_cluster_name(row['cluster'])
    
    with col1:
        # Prevent Streamlit code render bugs by composing strings on a single line without indentation/enters
        badges_html = ""
        if 'expert_score' in row:
            badges_html += f"<span class='movie-badge badge-expert'>{t_func('expert_score_label')}: {row['expert_score']:.2f}</span> "
        badges_html += f"<span class='movie-badge badge-rating'>Rating: {row['rating']}</span> "
        badges_html += f"<span class='movie-badge badge-runtime'>Runtime: {row['runtime']} {t_func('runtime_unit')}</span> "
        badges_html += f"<span class='movie-badge badge-cluster'>Cluster: {cluster_name}</span>"
        
        genres_html = " ".join([f"<span class='movie-badge'>{g.strip()}</span>" for g in str(row['genres']).split(',')])
        
        # Combine all HTML elements without Markdown line breaks
        detail_html = (
            f"<div class='card-title'>{row['title']}</div>"
            f"<div style='margin-bottom: 12px;'>{badges_html}</div>"
            f"<div style='margin-bottom: 16px;'>{genres_html}</div>"
            f"<div class='movie-plot'>{tr_func(row['plot'])}</div>"
        )
        st.markdown(detail_html, unsafe_allow_html=True)
        
        # Render metadata natively to avoid HTML color conflicts in Light/Dark mode
        st.markdown(f"**{t_func('director_label')}:** {row['directors']}")
        st.markdown(f"**{t_func('writer_label')}:** {row.get('writers', '-')}")
        st.write("")
        
        link_val = str(row.get('link', '')).strip()
        if pd.notna(row.get('link')) and link_val:
            match = re.search(r'href=[\'"]?([^\'" >]+)', link_val)
            if match: link_val = match.group(1)
            
            if link_val.startswith('http'): safe_link = link_val
            elif 'imdb.com' in link_val.lower() or 'www.' in link_val.lower(): safe_link = f"https://{link_val}"
            else: safe_link = f"https://www.imdb.com/find?q={urllib.parse.quote(link_val)}"
            
            safe_link = urllib.parse.quote(safe_link, safe=":/=?&")
            imdb_html = f'<a href="{safe_link}" target="_blank" rel="noopener noreferrer" style="display: inline-block; background-color: #0284c7; color: #ffffff !important; padding: 8px 18px; border-radius: 4px; text-decoration: none; font-weight: 500; font-size: 0.9em; letter-spacing: 0.5px;">{t_func("imdb_link")}</a>'
            st.markdown(imdb_html, unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color: #64748b; font-size: 0.9em; font-weight: 500;'>{t_func('no_imdb')}</span>", unsafe_allow_html=True)

    with col2:
        if pd.notna(row['poster']) and str(row['poster']).strip():
            st.markdown(f"""
                <div class="poster-container">
                    <img src="{row['poster']}" alt="Poster">
                </div>
            """, unsafe_allow_html=True)
        else:
            st.caption(t_func("no_poster"))

@st.dialog("Movie Details", width="large")
def movie_detail_modal(row_dict: dict):
    """Event handler to open the modal component for a specific movie."""
    row = pd.Series(row_dict)
    render_movie_details(row, t, tr)

def render_movie_grid(df: pd.DataFrame, prefix: str):
    """
    Iterate DataFrame mapping into a responsive 4-column grid card interface.
    
    Args:
        df (pd.DataFrame): Data subset ready to render.
        prefix (str): Unique namespace prefix for buttons to distinguish tab sources (expert/search/cluster).
    """
    cols = st.columns(4) 
    for i, (_, row) in enumerate(df.iterrows()):
        with cols[i % 4]:
            with st.container(border=True):
                poster_url = row['poster'] if pd.notna(row.get('poster')) and str(row['poster']).strip() else ""
                
                if poster_url:
                    st.markdown(f"""
                        <div class="poster-container">
                            <img src="{poster_url}" onerror="this.style.display='none'">
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                        <div class="poster-container">
                            <div style='position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); color:#475569; font-weight:600;'>No Poster</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                expert_display = f"<div style='font-size: 11px; color: #d97706; font-weight: 700; text-align: center; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px;'>{t('expert_score_label')}: {row['expert_score']:.2f}</div>" if 'expert_score' in row else ""
                
                st.markdown(f"{expert_display}<div class='grid-title'>{row['title']}</div>", unsafe_allow_html=True)
                
                cluster_name = get_translated_cluster_name(row['cluster'])
                st.markdown(f"<div style='font-size: 12px; color: #64748b; text-align: center; margin-bottom: 12px; font-weight: 500;'>{cluster_name}</div>", unsafe_allow_html=True)
                
                safe_key = str(row['title']).replace(" ", "_")
                if st.button(t("detail_btn"), key=f"btn_{prefix}_{i}_{safe_key}", use_container_width=True):
                    movie_detail_modal(row.to_dict())

# Navigation & Sidebar Controller
st.sidebar.title(t("sidebar_title"))
st.sidebar.markdown(f"**{t('language')}**")

col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("English", use_container_width=True, type="primary" if st.session_state.language == "en" else "secondary"):
        st.session_state.language = "en"
        st.rerun()
with col2:
    if st.button("Indonesia", use_container_width=True, type="primary" if st.session_state.language == "id" else "secondary"):
        st.session_state.language = "id"
        st.rerun()

st.sidebar.divider()

selected_genres = st.sidebar.multiselect(
    t("select_genres"), options=all_genres, default=st.session_state.selected_genres,
    help=t("genres_help"), key="selected_genres"
)

rating_min = st.sidebar.slider(t("min_rating"), 0.0, 10.0, float(st.session_state.rating_min), 0.1, key="rating_min")
votes_min = st.sidebar.slider(t("min_votes"), 0, 1_000_000, st.session_state.votes_min, 5_000, key="votes_min")

preferred_cluster = st.sidebar.selectbox(
    t("preferred_cluster"),
    options=[None, POPULAR_ID, HIDDEN_GEM_ID],
    format_func=lambda x: t("any_cluster") if x is None else get_translated_cluster_name(x),
    key="preferred_cluster"
)

st.sidebar.divider()
if st.sidebar.button(t("reset_button"), on_click=reset_filters, use_container_width=True):
    st.toast(t("reset_success"))

st.markdown(f"""
<div class="title-banner">
    <h1>{t("app_title")}</h1>
    <p>{t("app_desc")}</p>
</div>
""", unsafe_allow_html=True)

# Execute global dataset pre-filtering
if selected_genres:
    mask = movies[selected_genres].all(axis=1)
    filtered_movies = movies[mask].reset_index(drop=True)
    st.success(t("found_movies_genre", n=len(filtered_movies)))
else:
    filtered_movies = movies.copy()

tab1, tab2, tab3, tab4 = st.tabs([t("tab_expert"), t("tab_similar"), t("tab_clusters"), t("tab_search")])

# Tab 1: Bayesian Scoring Pipeline
with tab1:
    st.header(t("expert_header"))
    st.markdown(f"*{t('expert_desc')}*")
    st.divider()

    def bayesian_expert_system(df_source: pd.DataFrame, prefs: dict) -> pd.DataFrame:
        """
        Calculate Bayesian score based on specific quartile thresholds.
        
        Args:
            df_source (pd.DataFrame): Raw reference data.
            prefs (dict): Filter configuration (min rating, votes, cluster, genres).
            
        Returns:
            pd.DataFrame: DataFrame containing the top 12 results with the 'expert_score' column.
        """
        df = df_source.copy()
        
        if prefs['genres']: df = df[df[prefs['genres']].all(axis=1)]
        if prefs['cluster'] is not None: df = df[df['cluster'] == prefs['cluster']]
        if prefs['rating_min'] > 0: df = df[df['rating'] >= prefs['rating_min']]
        if prefs['votes_min'] > 0: df = df[df['votes'] >= prefs['votes_min']]
        
        if df.empty: return df
            
        C = df['rating'].mean()
        if pd.isna(C): C = 0 
        
        m = df['votes'].quantile(0.70)
        if pd.isna(m) or m == 0: m = 1 
        
        def bayesian_weighted_rating(row):
            v = row['votes']
            R = row['rating']
            return (v / (v + m) * R) + (m / (v + m) * C)
            
        df['expert_score'] = df.apply(bayesian_weighted_rating, axis=1)
        df = df.sort_values('expert_score', ascending=False)
        return df.head(12) 

    prefs = {
        'rating_min': rating_min, 'votes_min': votes_min,
        'genres': selected_genres, 'cluster': preferred_cluster
    }
    results = bayesian_expert_system(movies, prefs)

    if not results.empty:
        st.subheader(t("top_recommendations", n=len(results)))
        render_movie_grid(results, prefix="expert")
    else:
        st.warning(t("no_results"))

# Tab 2: O(N) Cosine Similarity Inference
with tab2:
    st.header(t("similar_header"))
    st.markdown(f"*{t('similar_desc')}*")
    st.divider()

    def get_recommendations(title: str, tfidf_matrix) -> pd.DataFrame:
        """
        Real-time similarity calculation strictly on 1 index (target movie)  
        against all sparse matrix indices. 
        """
        matching = movies[movies['title'] == title]
        if matching.empty:
            st.error(t("movie_not_found", title=title))
            return pd.DataFrame()
        
        idx = matching.index[0]
        
        sim_scores_array = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
        sim_scores_list = list(enumerate(sim_scores_array))
        sim_scores_sorted = sorted(sim_scores_list, key=lambda x: x[1], reverse=True)[1:13]
        
        indices = [i[0] for i in sim_scores_sorted]
        return movies.iloc[indices]

    if not filtered_movies.empty:
        choice = st.selectbox(t("choose_movie"), sorted(filtered_movies['title'].tolist()))
        if choice:
            similar = get_recommendations(choice, tfidf_matrix)
            if not similar.empty:
                st.subheader(t("top_similar", title=choice))
                render_movie_grid(similar, prefix="similar")
            else:
                st.info(t("no_similar"))
    else:
        st.info(t("no_movies_available"))

# Tab 3: Data Clustering Review
with tab3:
    st.header(t("clusters_header"))
    
    col1, col2 = st.columns(2)
    with col1:
        cluster_genres = st.multiselect(t("clusters_genres"), all_genres, help=t("clusters_genres_help"))
    with col2:
        sort_option = st.selectbox(t("sort_votes"), [t("sort_top"), t("sort_bottom")])

    st.divider()

    base = movies.copy()
    if cluster_genres:
        base = base[base[cluster_genres].all(axis=1)].reset_index(drop=True)

    if not base.empty:
        cluster_ids = [POPULAR_ID, HIDDEN_GEM_ID]
        cluster_tabs = st.tabs([get_translated_cluster_name(cid) for cid in cluster_ids])
        
        for tab, cid in zip(cluster_tabs, cluster_ids):
            with tab:
                if cid == POPULAR_ID: 
                    info = cluster_map['popular_centroid']
                else: 
                    info = cluster_map['hidden_gem_centroid']
                    
                st.caption(t("centroid_explanation", rating=info['rating'], votes=info['votes']))
                
                df_cluster = base[base['cluster'] == cid].copy()
                df_cluster = df_cluster.sort_values("votes", ascending=(sort_option == t("sort_bottom")))
                
                render_movie_grid(df_cluster.head(48), prefix=f"cluster_{cid}")
    else:
        st.info(t("no_results"))

# Tab 4: Index-based Search Query
with tab4:
    st.header(t("search_header"))
    st.markdown(f"*{t('search_desc')}*")
    
    search_query = st.text_input("Search Query", placeholder=t("search_placeholder"), key="search_query", label_visibility="collapsed")
    st.divider()
    
    if search_query:
        q = search_query.strip().lower()
        mask = movies['search_index'].str.contains(q, na=False)
        hasil = movies[mask].sort_values("rating", ascending=False)
        
        st.success(t("search_results", n=len(hasil), query=search_query))
        render_movie_grid(hasil.head(32), prefix="search")
    else:
        st.info("Masukkan kata kunci untuk mulai mencari..." if st.session_state.language == "id" else "Type a keyword to start searching...")