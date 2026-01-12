import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_and_preprocess_data(file_path, sep=';', encoding='utf-8'):
    """
    Memuat dataset, validasi kolom, dan lakukan preprocessing awal.
    
    Args:
        file_path (str): Path ke file CSV dataset.
        sep (str): Separator CSV (default ';').
        encoding (str): Encoding file (default 'utf-8').
    
    Returns:
        dict: Berisi DataFrame movies yang sudah diproses, scaler, kmeans_model, tfidf_matrix, cosine_sim, dan all_genres.
    """
    # Load dataset dengan error handling
    try:
        movies = pd.read_csv(file_path, sep=sep, encoding=encoding)
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' tidak ditemukan. Pastikan path file benar.")
    except Exception as e:
        raise Exception(f"Error loading dataset: {e}")
    
    # Validasi kolom wajib
    required_columns = ['title', 'genres', 'directors', 'writers', 'rating', 'votes', 'runtime', 'link', 'poster', 'plot']
    missing_columns = [col for col in required_columns if col not in movies.columns]
    if missing_columns:
        raise ValueError(f"Kolom berikut hilang dari dataset: {missing_columns}")
    
    # Clustering menggunakan KMeans dengan 2 cluster berdasarkan 'rating' dan 'votes'
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(movies[['rating', 'votes']])
    kmeans_model = KMeans(n_clusters=2, random_state=42)
    movies['cluster'] = kmeans_model.fit_predict(scaled_features)
    
    # Preprocessing genre: ubah kolom 'genres' menjadi list, dan buat kolom biner
    movies['genre_list'] = movies['genres'].fillna('').apply(lambda x: [g.strip() for g in x.split(',') if g.strip()])
    all_genres = sorted({g for sublist in movies['genre_list'] for g in sublist if g})
    for g in all_genres:
        movies[g] = movies['genre_list'].apply(lambda x: int(g in x))
    
    # Preprocessing untuk CBF
    movies['combined_features'] = (
        movies['genres'].fillna('') + ' ' +
        movies['directors'].fillna('') + ' ' +
        movies['writers'].fillna('')
    )
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['combined_features'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    return {
        'movies': movies,
        'scaler': scaler,
        'kmeans_model': kmeans_model,
        'tfidf_matrix': tfidf_matrix,
        'cosine_sim': cosine_sim,
        'all_genres': all_genres
    }