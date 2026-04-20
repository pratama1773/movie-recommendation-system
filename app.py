import streamlit as st
import pandas as pd
import functools
import urllib.parse
import re
from deep_translator import GoogleTranslator

# Konfigurasi antarmuka halaman utama aplikasi
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Fungsi terjemahan teks dengan lru_cache untuk optimasi performa
@functools.lru_cache(maxsize=10000)
def tr(text):
    """Menerjemahkan teks ke Bahasa Indonesia jika preferensi bahasa pengguna adalah 'id'."""
    if not text or pd.isna(text):
        return ""
    if st.session_state.get("language", "en") == "id":
        try:
            return GoogleTranslator(source='auto', target='id').translate(str(text))
        except:
            return str(text)  # Mengembalikan teks asli sebagai fallback apabila API gagal
    return str(text)

# Kamus lokalisasi untuk dukungan antarmuka multibahasa
TRANSLATIONS = {
    "en": {
        "app_title": "Movie Recommendation System",
        "app_desc": "Discover your next favorite movie using content similarity, clustering, and a simple expert system.",
        "sidebar_title": "Filters & Settings",
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
        "top_similar": "Top 10 movies similar to {title}",
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
        "search_results": "Found {n} movies for keyword: '{query}'",
        "genres_label": "Genres",
        "director_label": "Director(s)",
        "writer_label": "Writers",
        "runtime_label": "Runtime",
        "runtime_unit": "min",
        "plot_label": "Plot",
        "cluster_label": "Cluster",
        # Inline CSS diterapkan pada tautan untuk menjamin render tombol berfungsi
        "imdb_link": '<a href="{link}" target="_blank" rel="noopener noreferrer" style="display: inline-block; background-color: #1d4ed8; color: #ffffff !important; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.9em; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">View on IMDB</a>',
        "no_imdb": "<span style='color: #94a3b8; font-size: 0.9em;'>IMDB Link Not Available</span>",
        "no_poster": "No poster",
        "poster_error": "Poster unavailable",
        "no_movies_genre": "No genre filter applied – showing all movies.",
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
        "app_desc": "Temukan film favorit berikutnya menggunakan kemiripan konten, pengelompokan, dan sistem pakar.",
        "sidebar_title": "Filter & Pengaturan",
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
        "top_similar": "10 Film paling mirip dengan {title}",
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
        "search_results": "Ditemukan {n} film untuk kata kunci: '{query}'",
        "genres_label": "Genre",
        "director_label": "Sutradara",
        "writer_label": "Penulis",
        "runtime_label": "Durasi",
        "runtime_unit": "menit",
        "plot_label": "Sinopsis",
        "cluster_label": "Cluster",
        # Inline CSS diterapkan pada tautan untuk menjamin render tombol berfungsi
        "imdb_link": '<a href="{link}" target="_blank" rel="noopener noreferrer" style="display: inline-block; background-color: #1d4ed8; color: #ffffff !important; padding: 8px 16px; border-radius: 6px; text-decoration: none; font-weight: 600; font-size: 0.9em; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">Lihat di IMDB</a>',
        "no_imdb": "<span style='color: #94a3b8; font-size: 0.9em;'>Link IMDB Tidak Tersedia</span>",
        "no_poster": "Tanpa poster",
        "poster_error": "Poster tidak tersedia",
        "no_movies_genre": "Tidak ada filter genre – menampilkan semua film.",
        "found_movies_genre": "Ditemukan {n:,} film sesuai genre yang dipilih.",
        "no_results": "Tidak ada film yang cocok dengan filter saat ini.",
        "no_similar": "Tidak ada film serupa ditemukan.",
        "no_movies_available": "Tidak ada film tersedia dengan filter genre saat ini.",
        "movie_not_found": "Film '{title}' tidak ditemukan.",
        "detail_btn": "Detail",
        "dialog_title": "Detail Film"
    }
}

# Fungsi akses dinamis untuk mengambil frasa terjemahan berdasarkan bahasa aktif
def t(key, **kwargs):
    lang = st.session_state.get("language", "en")
    text = TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
    return text.format(**kwargs) if kwargs else text

# Manajemen session state untuk pengaturan bahasa bawaan
if "language" not in st.session_state:
    st.session_state.language = "en"

# Modul untuk memuat dan memproses dataset film beserta model machine learning
from utils.preprocessing import load_and_preprocess_data

try:
    data = load_and_preprocess_data("data/movie.csv", sep=';', encoding='utf-8')
    movies       = data['movies']
    cosine_sim   = data['cosine_sim']
    all_genres   = data['all_genres']
    scaler       = data['scaler']
    kmeans_model = data['kmeans_model']
except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")
    st.stop()

# Dekode centroid untuk kebutuhan tampilan informasi klaster
centroids = scaler.inverse_transform(kmeans_model.cluster_centers_)
centroid_info = {i: {'rating': centroids[i][0], 'votes': centroids[i][1]} for i in range(len(centroids))}

if 'movies_original' not in st.session_state:
    st.session_state.movies_original = movies.copy()

# Inisialisasi variabel filter bawaan pada manajemen state aplikasi
defaults = {'selected_genres': [], 'rating_min': 0.0, 'votes_min': 0, 'preferred_cluster': None}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Fungsi untuk mereset seluruh filter kembali ke nilai bawaan
def reset_filters():
    for key, val in defaults.items():
        st.session_state[key] = val

# Konfigurasi gaya visual kustom tingkat lanjut (CSS)
st.markdown("""
<style>
    /* Elemen banner utama aplikasi */
    .title-banner {
        background: linear-gradient(135deg, rgba(15, 32, 39, 0.85), rgba(32, 58, 67, 0.85), rgba(44, 83, 100, 0.85)), 
                    url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1920&q=80') center/cover no-repeat;
        padding: 3rem 2rem;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 2rem;
        border-bottom: 4px solid #0ea5e9;
        box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    }
    .title-banner h1 {
        color: #ffffff !important;
        font-size: 2.8rem !important;
        font-weight: 800 !important;
        margin: 0 0 10px 0 !important;
        letter-spacing: 1px;
    }
    .title-banner p {
        color: #bae6fd !important;
        font-size: 1.1rem !important;
        margin: 0 !important;
        font-weight: 400;
    }

    /* Modifikasi visual untuk label atau badge atribut film */
    .movie-badge {
        display: inline-block;
        padding: 0.35em 0.8em;
        font-size: 0.85em;
        font-weight: 600;
        border-radius: 6px;
        margin-right: 0.5em;
        margin-bottom: 0.6em;
        letter-spacing: 0.5px;
        color: #e2e8f0 !important;
        background-color: #334155 !important;
        border: 1px solid #475569;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }

    /* Penataan tipografi untuk deskripsi dan sinopsis film */
    .movie-plot {
        text-align: justify;
        line-height: 1.6;
        color: #f8fafc !important; 
        font-size: 15px;
        margin-top: 1.2rem;
        margin-bottom: 1.2rem;
        padding: 16px;
        background-color: #1e293b !important; 
        border-left: 4px solid #64748b;
        border-radius: 4px 8px 8px 4px;
    }
    
    /* Penataan teks informasi krusial (sutradara dan penulis) */
    .movie-meta { 
        font-size: 1em; 
        margin-bottom: 8px;
    }
    .movie-meta strong { 
        font-weight: 800;
    }
    
    /* Penataan elemen judul utama pada dialog antarmuka */
    .card-title {
        font-size: 1.8rem;
        font-weight: 800;
        margin-top: 0;
        margin-bottom: 1.2rem;
        border-bottom: 2px solid rgba(128,128,128,0.2);
        padding-bottom: 0.5rem;
    }

    /* Konstruksi visual untuk poster dengan rasio aspek standar */
    .poster-container {
        width: 100%;
        padding-top: 150%; 
        position: relative;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        background-color: #333;
        margin-bottom: 15px;
    }
    .poster-container img {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        object-fit: cover; 
        transition: transform 0.3s ease;
    }
    .poster-container:hover img {
        transform: scale(1.05);
    }
    
    /* Pemotongan teks judul yang panjang pada kartu grid */
    .grid-title {
        font-weight: 700;
        font-size: 15px;
        height: 45px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        text-align: center;
        margin-bottom: 5px;
    }
    
    /* Konfigurasi visual untuk panel kendali atau sidebar */
    [data-testid="stSidebar"] {
        background-color: #001f3f !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: white !important;
    }
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
        color: black !important; 
    }
    [data-testid="stSidebar"] button[kind="secondary"]:hover p,
    [data-testid="stSidebar"] button[kind="secondary"]:hover div {
        color: black !important; 
    }
    
    /* Integrasi antarmuka navigasi tabulasi (Tabs) bergaya modern */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e293b !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        border: 1px solid #334155 !important;
        color: #cbd5e1 !important;
        transition: 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover { background-color: #334155 !important; color: white !important; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
        color: #ffffff !important;
        border-color: #0ea5e9 !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 10px rgba(14, 165, 233, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# Fungsi modul komposit untuk merender konten detail sebuah film
def render_movie_details(row, t_func, tr_func):
    col1, col2 = st.columns([3, 1])
    
    genres_html = "".join([f'<span class="movie-badge badge-genre">{g.strip()}</span>' for g in str(row['genres']).split(',')])
    cluster_name = t_func("cluster_0") if row['cluster'] == 0 else t_func("cluster_1")
    
    with col1:
        st.markdown(f"""
            <div class='card-title'>{row['title']}</div>
            <div>
                <span class="movie-badge badge-rating">Rating: {row['rating']}</span>
                <span class="movie-badge badge-runtime">Runtime: {row['runtime']} {t_func('runtime_unit')}</span>
                <span class="movie-badge badge-cluster">Cluster: {cluster_name}</span>
                <br>
                {genres_html}
            </div>
            <div class="movie-plot">{tr_func(row['plot'])}</div>
            <div class="movie-meta"><strong>{t_func('director_label')}:</strong> {row['directors']}</div>
            <div class="movie-meta"><strong>{t_func('writer_label')}:</strong> {row.get('writers', '-')}</div>
            <br>
        """, unsafe_allow_html=True)
        
        # Eksekusi dan validasi tautan eksternal film 
        link_val = str(row.get('link', '')).strip()
        if pd.notna(row.get('link')) and link_val:
            # Mencari nilai URL di dalam tag HTML jika data berupa anchor link HTML
            match = re.search(r'href=[\'"]?([^\'" >]+)', link_val)
            if match:
                link_val = match.group(1)
            
            if link_val.startswith('http'):
                safe_link = link_val
            elif 'imdb.com' in link_val.lower() or 'www.' in link_val.lower():
                safe_link = f"https://{link_val}"
            else:
                # Fallback: Jika tautan tidak valid atau hanya berisi teks judul, arahkan ke pencarian IMDB
                safe_link = f"https://www.imdb.com/find?q={urllib.parse.quote(link_val)}"
            
            # Sanitasi URL (mengganti spasi dengan %20) agar tidak merusak tag HTML button pada Streamlit
            safe_link = urllib.parse.quote(safe_link, safe=":/=?&")
            st.markdown(t_func("imdb_link", link=safe_link), unsafe_allow_html=True)
        else:
            st.markdown(t_func("no_imdb"), unsafe_allow_html=True)

    with col2:
        if pd.notna(row['poster']) and str(row['poster']).strip():
            st.markdown(f"""
                <div class="poster-container">
                    <img src="{row['poster']}" alt="Poster">
                </div>
            """, unsafe_allow_html=True)
        else:
            st.caption(t_func("no_poster"))

# Modul perantara untuk membuka jendela popup berbasis modal
@st.dialog("Dialog Modal", width="large")
def movie_detail_modal(row_dict):
    row = pd.Series(row_dict)
    render_movie_details(row, t, tr)

# Fungsi utama untuk merender elemen film dalam kisi grid responsif
def render_movie_grid(df, prefix):
    # Tata letak pembagian 4 kolom untuk optimalisasi ukuran visual poster
    cols = st.columns(4) 
    for i, (_, row) in enumerate(df.iterrows()):
        with cols[i % 4]:
            with st.container(border=True):
                # Ekstraksi dan penanganan ketersediaan data poster film
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
                            <div style='position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); color:#aaa; font-weight:bold;'>No Poster</div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Render label film dan atribut sekunder
                st.markdown(f"<div class='grid-title'>{row['title']}</div>", unsafe_allow_html=True)
                
                cluster_name = t("cluster_0") if row['cluster'] == 0 else t("cluster_1")
                st.markdown(f"<div style='font-size: 13px; color: #888; text-align: center; margin-bottom: 12px;'>{cluster_name}</div>", unsafe_allow_html=True)
                
                # Pembuatan kunci status tombol unik dan pemicu fungsi modal
                safe_key = str(row['title']).replace(" ", "_")
                if st.button(t("detail_btn"), key=f"btn_{prefix}_{i}_{safe_key}", use_container_width=True):
                    movie_detail_modal(row.to_dict())

# Integrasi komponen interaktif panel navigasi lateral (Sidebar)
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
    options=[None, 0, 1],
    format_func=lambda x: t("any_cluster") if x is None else (t("cluster_0") if x == 0 else t("cluster_1")),
    key="preferred_cluster"
)

st.sidebar.divider()
if st.sidebar.button(t("reset_button"), on_click=reset_filters, use_container_width=True):
    st.toast(t("reset_success"))

# Inisialisasi susunan visual konten wilayah halaman utama
st.markdown(f"""
<div class="title-banner">
    <h1>{t("app_title")}</h1>
    <p>{t("app_desc")}</p>
</div>
""", unsafe_allow_html=True)

# Validasi filter komprehensif untuk dataset yang dirender
if selected_genres:
    mask = movies[selected_genres].all(axis=1)
    filtered_movies = movies[mask].reset_index(drop=True)
    st.success(t("found_movies_genre", n=len(filtered_movies)))
else:
    filtered_movies = movies.copy()

tab1, tab2, tab3, tab4 = st.tabs([t("tab_expert"), t("tab_similar"), t("tab_clusters"), t("tab_search")])

# Tabulasi 1: Implementasi logika algoritma Sistem Pakar (Expert System)
with tab1:
    st.header(t("expert_header"))
    st.markdown(f"*{t('expert_desc')}*")
    st.divider()

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
        return df.head(12) # Retensi kuantitas keluaran maksimum sejumlah 12 indeks grid

    results = expert_system_recommendations(prefs)

    if not results.empty:
        st.subheader(t("top_recommendations", n=len(results)))
        render_movie_grid(results, prefix="expert")
    else:
        st.warning(t("no_results"))

# Tabulasi 2: Pemrosesan evaluasi Kesamaan Konten (Content-Based Filtering)
with tab2:
    st.header(t("similar_header"))
    st.markdown(f"*{t('similar_desc')}*")
    st.divider()

    def get_recommendations(title, cosine_sim=cosine_sim):
        matching = movies[movies['title'] == title]
        if matching.empty:
            st.error(t("movie_not_found", title=title))
            return pd.DataFrame()
        idx = matching.index[0]
        sim_scores = sorted(enumerate(cosine_sim[idx]), key=lambda x: x[1], reverse=True)[1:13]
        indices = [i[0] for i in sim_scores]
        return movies.iloc[indices][['title','genres','directors','writers','rating','votes','runtime','cluster','plot','poster','link']]

    if not filtered_movies.empty:
        choice = st.selectbox(t("choose_movie"), sorted(filtered_movies['title'].tolist()))
        if choice:
            similar = get_recommendations(choice)
            if not similar.empty:
                st.subheader(t("top_similar", title=choice))
                render_movie_grid(similar, prefix="similar")
            else:
                st.info(t("no_similar"))
    else:
        st.info(t("no_movies_available"))

# Tabulasi 3: Visualisasi model segmentasi data (Clustering)
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
        cluster_tabs = st.tabs([f"Cluster {i}" for i in sorted(base['cluster'].unique())])
        for tab, cid in zip(cluster_tabs, sorted(base['cluster'].unique())):
            with tab:
                st.subheader(t("cluster_0_name") if cid == 0 else t("cluster_1_name"))
                info = centroid_info[cid]
                st.caption(t("centroid_explanation", rating=info['rating'], votes=info['votes']))
                
                df_cluster = base[base['cluster'] == cid].copy()
                df_cluster = df_cluster.sort_values("votes", ascending=(sort_option == t("sort_top")))
                
                # Eksekusi pembatasan jumlah indeks menjadi maksimum 48 data
                render_movie_grid(df_cluster.head(48), prefix=f"cluster_{cid}")
    else:
        st.info(t("no_results"))

# Tabulasi 4: Mekanisme manipulasi pencarian data kustom
with tab4:
    st.header(t("search_header"))
    st.markdown(f"*{t('search_desc')}*")
    
    search_query = st.text_input("Search Query", placeholder=t("search_placeholder"), key="search_query", label_visibility="collapsed")
    st.divider()
    
    if search_query:
        q = search_query.strip().lower()
        mask = (
            movies['title'].str.lower().str.contains(q, na=False) |
            movies['genres'].str.lower().str.contains(q, na=False) |
            movies['directors'].str.lower().str.contains(q, na=False) |
            movies['plot'].str.lower().str.contains(q, na=False)
        )
        hasil = movies[mask].sort_values("rating", ascending=False)
        
        st.success(t("search_results", n=len(hasil), query=search_query))
        
        # Menampilkan maksimum 32 hasil data pencarian kueri
        render_movie_grid(hasil.head(32), prefix="search")
    else:
        st.info("Masukkan kata kunci untuk mulai mencari..." if st.session_state.language == "id" else "Type a keyword to start searching...")