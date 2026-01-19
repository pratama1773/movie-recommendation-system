import streamlit as st
import pandas as pd
import functools
from deep_translator import GoogleTranslator  

# FUNGSI TERJEMAHAN
@functools.lru_cache(maxsize=10000)
def tr(text):
    """Translate text ke Bahasa Indonesia hanya saat bahasa Indonesia dipilih"""
    if not text or pd.isna(text):
        return ""
    if st.session_state.get("language", "en") == "id":
        try:
            return GoogleTranslator(source='auto', target='id').translate(str(text))
        except:
            return str(text)  # fallback kalau error
    return str(text)


# MULTI-LANGUAGE DICTIONARY & FUNCTION
TRANSLATIONS = {
    "en": {
        "app_title": "Movie Recommendation System",
        "app_desc": "Discover your next favorite movie using content similarity, clustering, and a simple expert system.",
        "sidebar_title": "Movie Recommendation System",
        "select_genres": "Select genre(s)",
        "genres_help": "Movies must belong to ALL selected genres",
        "min_rating": "Minimum Rating",
        "min_votes": "Minimum Votes",
        "preferred_cluster": "Preferred Cluster",
        "any_cluster": "Any Cluster",
        "cluster_0": "Popular Movie",
        "cluster_1": "Less-Popular Movie",
        "reset_button": "Reset All Filters",
        "reset_success": "All filters have been reset!",
        "language": "Language",
        "tab_expert": "Expert System",
        "tab_similar": "Similar Movies",
        "tab_clusters": "Explore Clusters",
        "tab_search": "Search",
        "expert_header": "Expert System Recommendations",
        "expert_desc": "Personalized recommendations based on your rating, popularity, and cluster preferences.",
        "top_recommendations": "Top {n} Recommendations",
        "similar_header": "Content-Based Recommendations",
        "similar_desc": "Find movies most similar to the one you love.",
        "choose_movie": "Choose a movie",
        "top_similar": "Top 10 movies similar to **{title}**",
        "clusters_header": "Movie Clusters",
        "clusters_genres": "Select genre(s) for Clusters:",
        "clusters_genres_help": "Filter movies shown in both clusters. Leave empty to see all genres.",
        "sort_votes": "Sort movies by votes:",
        "sort_top": "Top",
        "sort_bottom": "Bottom",
        "cluster_0_name": "Popular Movies",
        "cluster_1_name": "Less-Popular Movies",
        "centroid_explanation": "**Centroid:** Avg rating ≈ {rating:.2f} | Avg votes ≈ {votes:,.0f}",
        "search_header": "Search Movies",
        "search_desc": "Search movies by title, genre, director, or keywords in the plot.",
        "search_placeholder": "e.g. Inception, Nolan, superhero, love, zombie...",
        "search_results": "Found **{n}** movies for keyword: `{query}`",
        "genres_label": "Genres",
        "director_label": "Director(s)",
        "writer_label": "Writers",
        "runtime_label": "Runtime",
        "runtime_unit": "min",
        "plot_label": "Plot",
        "cluster_label": "Cluster",
        "imdb_link": "*IMDB Link:* {link}",
        "no_imdb": "*IMDB Link:* Not available",
        "no_poster": "No poster",
        "poster_error": "Poster unavailable",
        "no_movies_genre": "No genre filter applied – showing all movies.",
        "found_movies_genre": "Found **{n:,}** movies matching selected genre(s).",
        "no_results": "No movies match the current filters.",
        "no_similar": "No similar movies found.",
        "no_movies_available": "No movies available with the current genre filter.",
        "movie_not_found": "Movie '{title}' not found.",
    },
    "id": {
        "app_title": "Sistem Rekomendasi Film",
        "app_desc": "Temukan film favorit berikutnya menggunakan **kemiripan konten**, **pengelompokan**, dan **sistem pakar sederhana**.",
        "sidebar_title": "Sistem Rekomendasi Film",
        "select_genres": "Pilih genre",
        "genres_help": "Film harus termasuk SEMUA genre yang dipilih",
        "min_rating": "Rating Minimum",
        "min_votes": "Minimum Votes",
        "preferred_cluster": "Cluster yang Diinginkan",
        "any_cluster": "Semua Cluster",
        "cluster_0": "Film Populer Berkualitas",
        "cluster_1": "Permata Tersembunyi Berkualitas",
        "reset_button": "Reset Semua Filter",
        "reset_success": "Semua filter telah direset!",
        "language": "Bahasa",
        "tab_expert": "Sistem Pakar",
        "tab_similar": "Film Serupa",
        "tab_clusters": "Jelajahi Cluster",
        "tab_search": "Cari Film",
        "expert_header": "Rekomendasi Sistem Pakar",
        "expert_desc": "Rekomendasi personal berdasarkan rating, popularitas, dan preferensi cluster Anda.",
        "top_recommendations": "Rekomendasi Teratas ({n})",
        "similar_header": "Rekomendasi Berdasarkan Konten",
        "similar_desc": "Temukan film yang paling mirip dengan yang Anda sukai.",
        "choose_movie": "Pilih film",
        "top_similar": "10 Film paling mirip dengan **{title}**",
        "clusters_header": "Kelompok Film",
        "clusters_genres": "Pilih genre untuk Cluster:",
        "clusters_genres_help": "Filter film di kedua cluster. Kosongkan untuk melihat semua genre.",
        "sort_votes": "Urutkan berdasarkan votes:",
        "sort_top": "Teratas",
        "sort_bottom": "Terendah",
        "cluster_0_name": "Film Populer",
        "cluster_1_name": "Film Kurang Populer",
        "centroid_explanation": "**Centroid:** Rata-rata rating ≈ {rating:.2f} | Rata-rata votes ≈ {votes:,.0f}",
        "search_header": "Cari Film",
        "search_desc": "Cari film berdasarkan judul, genre, sutradara, atau kata kunci di sinopsis.",
        "search_placeholder": "contoh: Inception, Nolan, superhero, cinta, zombie...",
        "search_results": "Ditemukan **{n}** film untuk kata kunci: `{query}`",
        "genres_label": "Genre",
        "director_label": "Sutradara",
        "writer_label": "Penulis",
        "runtime_label": "Durasi",
        "runtime_unit": "menit",
        "plot_label": "Sinopsis",
        "cluster_label": "Cluster",
        "imdb_link": "*Link IMDB:* {link}",
        "no_imdb": "*Link IMDB:* Tidak tersedia",
        "no_poster": "Tanpa poster",
        "poster_error": "Poster tidak tersedia",
        "no_movies_genre": "Tidak ada filter genre – menampilkan semua film.",
        "found_movies_genre": "Ditemukan **{n:,}** film sesuai genre yang dipilih.",
        "no_results": "Tidak ada film yang cocok dengan filter saat ini.",
        "no_similar": "Tidak ada film serupa ditemukan.",
        "no_movies_available": "Tidak ada film tersedia dengan filter genre saat ini.",
        "movie_not_found": "Film '{title}' tidak ditemukan.",
    }
}

def t(key, **kwargs):
    lang = st.session_state.get("language", "en")
    text = TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
    return text.format(**kwargs) if kwargs else text

# Inisialisasi bahasa
if "language" not in st.session_state:
    st.session_state.language = "en"


# Masukin Dataset
from utils.preprocessing import load_and_preprocess_data

try:
    data = load_and_preprocess_data("data/movie.csv", sep=';', encoding='utf-8')
    movies       = data['movies']
    cosine_sim   = data['cosine_sim']
    all_genres   = data['all_genres']
    scaler       = data['scaler']
    kmeans_model = data['kmeans_model']
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

centroids = scaler.inverse_transform(kmeans_model.cluster_centers_)
centroid_info = {i: {'rating': centroids[i][0], 'votes': centroids[i][1]} for i in range(len(centroids))}

if 'movies_original' not in st.session_state:
    st.session_state.movies_original = movies.copy()

# SESSION STATE DEFAULTS
defaults = {'selected_genres': [], 'rating_min': 0.0, 'votes_min': 0, 'preferred_cluster': None}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

def reset_filters():
    for key, val in defaults.items():
        st.session_state[key] = val

# CUSTOM CSS 
st.markdown("""
<style>
    /* BANNER  */
.title-banner {
    background: url('https://images.unsplash.com/photo-1518676590629-3dcbd9c5a5c9?w=1920') center/cover no-repeat,
                linear-gradient(rgba(0, 31, 63, 0.85), rgba(0, 31, 63, 0.85)),
                #001f3f;
    padding: 1.6rem 2rem !important;
    border-radius: 18px;
    text-align: center;
    margin-bottom: 2.5rem;
    border-bottom: 5px solid #FFD700;
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    max-width: 100%;
}
.title-banner h1 {
    color: #FFD700 !important;
    font-size: 2rem !important;
    font-weight: 900 !important;
    margin: 0 !important;
    letter-spacing: 2px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    text-shadow: 0 0 20px rgba(255,215,0,0.4);
    line-height: 1.2;
}
.title-banner p {
    color: #ffffff !important;
    font-size: 1rem !important;
    margin: 0.7rem 0 0 0 !important;
    opacity: 0.95;
    font-weight: 500;
}
        /* TAB BAR */
.stTabs [data-baseweb="tab-list"] {
    background: linear-gradient(135deg, #001f3f) !important;  
    border-radius: 15px 15px 0 0 !important;
    padding: 12px 5px !important;
    border: 3px solid #FFD700 !important;
    gap: 5px;
}

.stTabs [data-baseweb="tab"] {
    background: #1034A6 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    padding: 14px 28px !important;
    transition: all 0.4s ease !important;
    backdrop-filter: blur(4px);
}

/* HOVER */
.stTabs [data-baseweb="tab"]:hover {
    background: #FFD700 !important;
    color: #000000 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 15px rgba(255, 215, 0, 0.6) !important;
    font-weight: 900 !important;
}
.stTabs [data-baseweb="tab"]:hover * {
    color: #000000 !important;
}

/* Tab yang aktif tetap seperti semula */
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background: #FFD700 !important;
    color: #000000 !important;
    font-weight: 900 !important;
    box-shadow: 0 0 20px rgba(255, 215, 0, 0.7), 0 6px 15px rgba(0, 0, 0, 0.4) !important;
    transform: translateY(-3px);
}

.stTabs [data-baseweb="tab-panel"] * {
    color: #000000 !important;
}

.stTabs [data-baseweb="tab-panel"] {
    background: #ffffff !important;
    border-radius: 0 0 16px 16px !important;
    padding: 2.5rem 2rem !important;
    min-height: 500px;
    border: 3px solid #FFD700 !important;
    border-top: none !important;
    z-index:-1;
}


    

    /* LINK & POSTER */
    section[data-testid="stExpander"] a {color: #1034A6 !important; text-decoration: none !important; font-weight: 700;}
    section[data-testid="stExpander"] a:hover {color: #1034A6 !important; text-decoration: underline !important;}
    section[data-testid="stExpander"] img {
        border: 3px solid #1034A6 !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.7) !important;
        textalign: justify;
    }
    section[data-testid="stExpander"] img:hover {transform: scale(1.05);}

    /* SIDEBAR */
   [data-testid="stSidebar"] {background-color: #001f3f;}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] label, [data-testid="stSidebar"] p {color: white !important;}
[data-testid="stSidebar"] button[kind="secondary"] {
    background-color: #1034A6 !important; 
    color: white !important; 
    border: none !important;
    border-radius: 8px !important; 
    font-weight: 600 !important; 
    width: 100% !important;
}
[data-testid="stSidebar"] button[kind="secondary"]:hover {
    background-color: #FFD700 !important; 
    box-shadow: 0 4px 8px rgba(0,0,0,0.2) !important;
    color: black !important;                     /* Teks jadi hitam saat hover */
}
[data-testid="stSidebar"] button[kind="secondary"]:hover p,
[data-testid="stSidebar"] button[kind="secondary"]:hover div {
    color: black !important;                     /* Pastikan semua elemen teks ikut hitam */
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title(t("sidebar_title"))

st.sidebar.markdown( t("language"))
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.button("English", use_container_width=True):
        st.session_state.language = "en"
        st.rerun()
with col2:
    if st.button("Indonesia", use_container_width=True):
        st.session_state.language = "id"
        st.rerun()

st.sidebar.markdown("---")

selected_genres = st.sidebar.multiselect(
    t("select_genres"), options=all_genres, default=st.session_state.selected_genres,
    help=t("genres_help"), key="selected_genres"
)
rating_min = st.sidebar.slider(t("min_rating"), 0.0, 10.0, float(st.session_state.rating_min), 0.1, key="rating_min")
votes_min = st.sidebar.slider(t("min_votes"), 0, 1_000_000, st.session_state.votes_min, 5_000, key="votes_min")
preferred_cluster = st.sidebar.selectbox(
    t("preferred_cluster"),
    options=[None, 0, 1],
    format_func=lambda x: t("any_cluster") if x is None else (t("cluster_0") if x == 0 else t("cluster_1")),
    key="preferred_cluster"
)

if st.sidebar.button(t("reset_button"), on_click=reset_filters, use_container_width=True):
    st.success(t("reset_success"))

# Halaman utama
st.markdown(f"""
<div class="title-banner">
    <h1>{t("app_title")}</h1>
    <p>{t("app_desc")}</p>
</div>
""", unsafe_allow_html=True)


if selected_genres:
    mask = movies[selected_genres].all(axis=1)
    filtered_movies = movies[mask].reset_index(drop=True)
    st.success(t("found_movies_genre", n=len(filtered_movies)))
else:
    filtered_movies = movies.copy()
    st.info(t("no_movies_genre"))

tab1, tab2, tab3, tab4 = st.tabs([t("tab_expert"), t("tab_similar"), t("tab_clusters"), t("tab_search")])

# TAB 1: Expert System
with tab1:
    st.header(t("expert_header"))
    st.markdown(t("expert_desc"))

    prefs = {
        'rating_min': rating_min, 'votes_min': votes_min,
        'genres': selected_genres, 'cluster': preferred_cluster
    }

    def expert_system_recommendations(prefs):
        df = movies.copy()
        if prefs['rating_min'] > 0: df = df[df['rating'] >= prefs['rating_min']]
        if prefs['votes_min'] > 0: df = df[df['votes'] >= prefs['votes_min']]
        if prefs['genres']: df = df[df[prefs['genres']].all(axis=1)]
        if prefs['cluster'] is not None: df = df[df['cluster'] == prefs['cluster']]
        if prefs['rating_min'] >= 8.0 and prefs['votes_min'] >= 10_000:
            df = df[df['cluster'] == 1]
        return df.head(10)

    results = expert_system_recommendations(prefs)

    if not results.empty:
        st.subheader(t("top_recommendations", n=len(results)))
        for _, row in results.iterrows():
            with st.expander(f"**{row['title']}** {row['rating']} ({row['votes']:,} votes)"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(
                        f"""
                        <div style="
                            text-align: justify;
                            line-height: 1.7;
                            color: #6B7280;
                            font-size: 14px;
                        ">
                            {tr(row['plot'])}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.write(f"**{t('genres_label')}:** {row['genres']}")
                    st.write(f"**{t('director_label')}:** {row['directors']}")
                    st.write(f"**{t('runtime_label')}:** {row['runtime']} {t('runtime_unit')}")
                    cluster_name = t("cluster_0") if row['cluster'] == 0 else t("cluster_1")
                    st.write(f"**{t('cluster_label')}:** {cluster_name}")
                    st.markdown(t("imdb_link", link=row['link']) if pd.notna(row.get('link')) and row['link'].strip() else t("no_imdb"), unsafe_allow_html=True)
                with col2:
                    if pd.notna(row['poster']) and row['poster'].strip():
                        try: st.image(row['poster'], use_container_width=True)
                        except: st.write(t("poster_error"))
                    else:
                        st.write(t("no_poster"))
    else:
        st.warning(t("no_results"))

# TAB 2: Similar Movies
with tab2:
    st.header(t("similar_header"))
    st.markdown(t("similar_desc"))

    def get_recommendations(title, cosine_sim=cosine_sim):
        matching = movies[movies['title'] == title]
        if matching.empty:
            st.error(t("movie_not_found", title=title))
            return pd.DataFrame()
        idx = matching.index[0]
        sim_scores = sorted(enumerate(cosine_sim[idx]), key=lambda x: x[1], reverse=True)[1:11]
        indices = [i[0] for i in sim_scores]
        return movies.iloc[indices][['title','genres','directors','writers','rating','votes','runtime','cluster','plot','poster','link']]

    if not filtered_movies.empty:
        choice = st.selectbox(t("choose_movie"), sorted(filtered_movies['title'].tolist()))
        if choice:
            similar = get_recommendations(choice)
            if not similar.empty:
                st.subheader(t("top_similar", title=choice))
                for _, row in similar.iterrows():
                    with st.expander(f"**{row['title']}** {row['rating']} ({row['votes']:,} votes)"):
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(
                                f"""
                                <div style="
                                    text-align: justify;
                                    line-height: 1.7;
                                    color: #6B7280;
                                    font-size: 14px;
                                ">
                                    {tr(row['plot'])}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                            st.write(f"**{t('genres_label')}:** {row['genres']}")
                            st.write(f"**{t('director_label')}:** {row['directors']}")
                            st.write(f"**{t('runtime_label')}:** {row['runtime']} {t('runtime_unit')}")
                            cluster_name = t("cluster_0") if row['cluster'] == 0 else t("cluster_1")
                            st.write(f"**{t('cluster_label')}:** {cluster_name}")
                            st.markdown(t("imdb_link", link=row['link']) if pd.notna(row.get('link')) and row['link'].strip() else t("no_imdb"), unsafe_allow_html=True)
                        with col2:
                            if pd.notna(row['poster']) and row['poster'].strip():
                                try: st.image(row['poster'], use_container_width=True)
                                except: st.write(t("poster_error"))
                            else:
                                st.write(t("no_poster"))
            else:
                st.info(t("no_similar"))
    else:
        st.info(t("no_movies_available"))

# TAB 3: Explore Clusters
with tab3:
    st.header(t("clusters_header"))
    cluster_genres = st.multiselect(t("clusters_genres"), all_genres, help=t("clusters_genres_help"))
    sort_option = st.selectbox(t("sort_votes"), [t("sort_top"), t("sort_bottom")])

    base = movies.copy()
    if cluster_genres:
        base = base[base[cluster_genres].all(axis=1)].reset_index(drop=True)

    if not base.empty:
        cluster_tabs = st.tabs([f"Cluster {i}" for i in sorted(base['cluster'].unique())])
        for tab, cid in zip(cluster_tabs, sorted(base['cluster'].unique())):
            with tab:
                st.subheader(t("cluster_0_name") if cid == 0 else t("cluster_1_name"))
                info = centroid_info[cid]
                st.write(t("centroid_explanation", rating=info['rating'], votes=info['votes']))
                
                df_cluster = base[base['cluster'] == cid].copy()
                df_cluster = df_cluster.sort_values("votes", ascending=(sort_option == t("sort_bottom")))
                
                for _, row in df_cluster.iterrows():
                    with st.expander(f"{row['title']} {row['rating']} (Votes: {row['votes']:,})"):
                        st.markdown(f"**{t('genres_label')}:** {row['genres']}")
                        st.markdown(f"**{t('director_label')}:** {row['directors']}")
                        st.markdown(f"**{t('writer_label')}:** {row['writers']}")
                        st.markdown(f"**{t('runtime_label')}:** {row['runtime']} {t('runtime_unit')}")
                        st.markdown(
                        f"""
                        <div style="
                            text-align: justify;
                            line-height: 1.7;
                            color: #6B7280;
                            font-size: 14px;
                        ">
                            {tr(row['plot'])}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    else:
        st.info(t("no_results"))

# TAB 4: Search
with tab4:
    st.header(t("search_header"))
    st.markdown(t("search_desc"))

    search_query = st.text_input("", placeholder=t("search_placeholder"), key="search_query")
    
    if search_query:
        q = search_query.strip().lower()
        mask = (
            movies['title'].str.lower().str.contains(q, na=False) |
            movies['genres'].str.lower().str.contains(q, na=False) |
            movies['directors'].str.lower().str.contains(q, na=False) |
            movies['plot'].str.lower().str.contains(q, na=False)
        )
        hasil = movies[mask].sort_values("rating", ascending=False)
        
        st.write(t("search_results", n=len(hasil), query=search_query))
        for _, row in hasil.iterrows():
            with st.expander(f"**{row['title']}** {row['rating']} ({row['votes']:,} votes)"):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(
                        f"""
                        <div style="
                            text-align: justify;
                            line-height: 1.7;
                            color: #6B7280;
                            font-size: 14px;
                        ">
                            {tr(row['plot'])}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.write(f"**{t('genres_label')}:** {row['genres']}")
                    st.write(f"**{t('director_label')}:** {row['directors']}")
                    st.write(f"**{t('runtime_label')}:** {row['runtime']} {t('runtime_unit')}")
                    st.markdown(t("imdb_link", link=row['link']) if pd.notna(row.get('link')) and row['link'].strip() else t("no_imdb"), unsafe_allow_html=True)
                with col2:
                    if pd.notna(row['poster']) and row['poster'].strip():
                        try: st.image(row['poster'], use_container_width=True)
                        except: st.write(t("poster_error"))
                    else:
                        st.write(t("no_poster"))
    else:
        st.info("Masukkan kata kunci untuk mulai mencari..." if st.session_state.language == "id" else "Type a keyword to start searching...")

