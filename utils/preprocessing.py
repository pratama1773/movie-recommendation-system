"""
Data Pipeline & Machine Learning Preprocessing Layer.
This module is responsible for loading raw data, extracting NLP features,
and training the Unsupervised Learning model (K-Means) before it is consumed by the UI.

The architecture is designed to prevent I/O bottlenecks and Memory Leaks (OOM) 
by avoiding O(N^2) spatial matrix computation on the server/startup side.
"""

import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

def load_and_preprocess_data(file_path: str, sep: str = ';', encoding: str = 'utf-8') -> dict:
    """
    Loads the CSV dataset, normalizes null values, performs K-Means segmentation, 
    and prepares the TF-IDF (Term Frequency-Inverse Document Frequency) spatial index.
    
    Computation Procedure (Pipeline):
    1. I/O Validation (Fail-fast mechanism).
    2. Unsupervised Segmentation (K-Means Clustering).
    3. Multi-genre extraction (OHE/One-Hot Encoding).
    4. Narrative text vectorization (CBF - Content Based Filtering).
    5. O(1) search index compilation for the UI.
    
    Args:
        file_path (str): Location of the dataset file in the local system.
        sep (str, optional): CSV column separator. Defaults to ';'.
        encoding (str, optional): Character decoding format. Defaults to 'utf-8'.
        
    Returns:
        dict: Structured data payload packed in a dictionary, containing:
            - 'movies': Final annotated pd.DataFrame.
            - 'tfidf_matrix': scipy.sparse.csr_matrix (Highly memory efficient).
            - 'all_genres': List of unique string genres.
            - 'cluster_map': Dict containing mathematical cluster ID mapping.
            
    Raises:
        FileNotFoundError: If the CSV path is invalid.
        ValueError: If mandatory columns are missing.
    """
    
    # IO OPERATIONS & SANITIZATION
    try:
        movies = pd.read_csv(file_path, sep=sep, encoding=encoding)
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found in the system.")
    except Exception as e:
        raise Exception(f"I/O Exception while reading DataFrame: {e}")
    
    # Validate data schema integrity (Prevents runtime crashes in UI)
    required_columns = ['title', 'genres', 'directors', 'writers', 'rating', 'votes', 'runtime', 'link', 'poster', 'plot']
    missing_columns = [col for col in required_columns if col not in movies.columns]
    if missing_columns:
        raise ValueError(f"Flawed dataset schema. Missing columns: {missing_columns}")
    
    # UNSUPERVISED LEARNING (K-MEANS CLUSTERING)
    # Normalize matrix dimensions (Rating 0-10 vs millions of Votes) using Min-Max
    scaler = MinMaxScaler()
    scaled_features = scaler.fit_transform(movies[['rating', 'votes']])
    
    # Initialize and fit model (K=2) with a fixed stochastic seed
    kmeans_model = KMeans(n_clusters=2, random_state=42)
    movies['cluster'] = kmeans_model.fit_predict(scaled_features)
    
    # Mathematically Evaluate Centroids (Resolving Stochastic Blindness)
    # Convert normalized space coordinates back to actual values
    centroids = scaler.inverse_transform(kmeans_model.cluster_centers_)
    
    # Dynamically resolve cluster IDs based on absolute popularity parameter (votes)
    if centroids[0][1] > centroids[1][1]:
        popular_id, hidden_gem_id = 0, 1
    else:
        popular_id, hidden_gem_id = 1, 0
        
    # Map the state dictionary so the UI (app.py) doesn't need to perform 
    # mathematical model evaluation processes.
    cluster_map = {
        'popular_id': popular_id,
        'hidden_gem_id': hidden_gem_id,
        'popular_centroid': {'rating': centroids[popular_id][0], 'votes': centroids[popular_id][1]},
        'hidden_gem_centroid': {'rating': centroids[hidden_gem_id][0], 'votes': centroids[hidden_gem_id][1]}
    }
    
    # Static labeling per dataframe row to simplify UI rendering
    movies['cluster_label'] = movies['cluster'].map({
        popular_id: "Popular",
        hidden_gem_id: "Hidden Gem"
    })
    
    # FEATURE EXTRACTION (ONE-HOT ENCODING GENRE)
    # Convert CSV genre strings into lists and filter empty spaces
    movies['genre_list'] = movies['genres'].fillna('').apply(lambda x: [g.strip() for g in x.split(',') if g.strip()])
    all_genres = sorted({g for sublist in movies['genre_list'] for g in sublist if g})
    
    # Build binary feature columns (1/0) for filtering efficiency
    for g in all_genres:
        movies[g] = movies['genre_list'].apply(lambda x: int(g in x))
    
    # CONTENT-BASED FILTERING (TF-IDF VECTORIZATION)
    # Build a single giant composite string representing the movie's narrative identity
    movies['combined_features'] = (
        movies['genres'].fillna('') + ' ' +
        movies['directors'].fillna('') + ' ' +
        movies['writers'].fillna('') + ' ' +
        movies['plot'].fillna('')  # Adding the plot is crucial for semantic accuracy
    )
    
    # Convert composite string into TF-IDF vectors (removing english stop words)
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['combined_features'])
    # Note: Cosine Similarity is NOT computed here to prevent O(N^2) Space complexity.
    
    # O(1) SEARCH INDEXING
    # Pre-compute (lowercase) search features into a single composite string column.
    # This removes I/O overhead on the UI, preventing the need for 'OR' (|) operations at runtime.
    movies['search_index'] = (
        movies['title'].fillna('') + ' ' +
        movies['genres'].fillna('') + ' ' +
        movies['directors'].fillna('') + ' ' +
        movies['plot'].fillna('')
    ).str.lower()
    
    # Return Structured Payload
    return {
        'movies': movies,
        'tfidf_matrix': tfidf_matrix,
        'all_genres': all_genres,
        'cluster_map': cluster_map
    }