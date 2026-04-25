Movie Recommendation System Using K-Means Clustering, Content-Based Filtering, and Bayesian Probability

This project is an advanced, web-based movie recommendation system developed for academic research purposes.
The system aims to help users select movies efficiently by reducing information overload caused by the massive scale of available digital content.

Moving beyond static rules, the application implements three independent and mathematically driven recommendation approaches, optimized for memory efficiency and deployed as an interactive web application using Streamlit.

Project Objective

The main objective of this project is to develop a robust movie recommendation system that provides highly accurate, bias-free, and relevant movie suggestions using different machine learning and statistical techniques.

The system is designed to:

Group movies dynamically based on popularity and ratings.

Recommend similar movies based on deep content characteristics (including plot narratives).

Provide personalized recommendations ranked by Bayesian mathematical probability to eliminate bias from low-vote anomalies.

Recommendation Methods

The system implements three core recommendation engines, each accessible through a modular tab in the application.

1. Dynamic K-Means Clustering

K-Means Clustering (Unsupervised Learning) is used to segment movies based on numerical features:

IMDb rating

Number of votes

The data is normalized using MinMaxScaler before clustering. Based on validation metrics (Elbow Method, Silhouette Score), the optimal number of clusters is set to two.
To prevent stochastic blindness (randomly flipped labels upon retraining), the system dynamically evaluates the centroids at runtime.

The resulting clusters are definitively interpreted as:

Popular Movies (Higher average votes)

Hidden Gems (Lower average votes, potentially high ratings)

2. Content-Based Filtering (On-the-Fly Inference)

Content-Based Filtering is utilized to recommend movies most similar to a selected title.

To maximize semantic accuracy, multiple attributes are combined into a single text vector:

Genres

Directors

Writers

Plot / Summary

The similarity between movies is calculated using TF-IDF vectorization. To prevent $O(N^2)$ memory leak (Out of Memory issues on large datasets), the Cosine Similarity is calculated linearly $O(N)$ on-the-fly only against the chosen movie's index.

3. Bayesian Expert System

Replacing traditional and rigid IF-THEN rules, the system now utilizes a Bayesian Weighted Average to rank movies objectively. This is the same statistical approach used by major platforms like IMDb for their Top 250 lists.

Users input their Hard Filters (minimum rating, minimum votes, preferred genres, and cluster). The system then calculates the macro-parameters of the valid subset and ranks the movies using the Bayesian probability formula:

W = (v / (v+m) * R) + (m / (v+m) * C)

Where:

W = Weighted Rating (Expert Score)

v = Number of votes for the movie

m = Minimum votes required to be listed (calculated dynamically at the 70th percentile)

R = Average rating of the movie

C = Mean rating across the entire valid dataset

This ensures a documentary with a 9.5 rating from only 100 votes doesn't unjustly outrank an acclaimed masterpiece with an 8.5 rating from 1,000,000 votes.

Features

Objective Ranking: Personalized recommendations using Bayesian Probability mathematics.

Deep Content Similarity: Recommendations evaluating genres, directors, and plot narratives.

Exploratory Clustering: Unsupervised segmentation for Popular Movies vs Hidden Gems.

O(1) Indexed Fast Search: Highly optimized search engine looking through pre-compiled string index.

Memory Optimized: Sparse matrix handling and linear similarity calculations to save RAM.

Bilingual UI: Native support for English and Indonesian using real-time translation caching.

Technologies Used

Python (Core Logic)

Streamlit (Frontend/UI)

Pandas & NumPy (Data Manipulation)

Scikit-learn (Machine Learning Pipeline: K-Means, TF-IDF, MinMaxScaler)

deep-translator (I18N Localization)

Dataset Source

The dataset used in this project consists of 5000 movies.

Movie IDs and titles were obtained from IMDb (https://www.imdb.com).

Additional movie attributes (genres, year, rating, votes, runtime, directors, writers, links, posters, and plot summaries) were retrieved via the OMDb API (https://www.omdbapi.com).

The dataset was collected, heavily sanitized, and structured for academic and experimental purposes.

Dataset Attributes

The dataset expects the following schema:

id: unique IMDb movie identifier

title: movie title

genres: movie genres

release_year: year of release

rating: average IMDb rating

votes: number of user votes

runtime: movie duration in minutes

directors: movie directors

writers: movie writers

link: IMDb movie page URL

poster: movie poster image URL

plot: short movie plot description

Project Structure

movie-recommendation-system/
├── app.py                  # Main Streamlit frontend interface
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
├── data/
│   └── movie.csv           # Source dataset
└── utils/
    └── preprocessing.py    # Data pipeline & Machine learning models


Installation and Usage

To run the application locally on your machine:

Clone the repository

git clone [https://github.com/pratama1773/movie-recommendation-system.git](https://github.com/pratama1773/movie-recommendation-system.git)


Navigate to the project directory

cd movie-recommendation-system


Install required dependencies

pip install -r requirements.txt


Run the application

streamlit run app.py


Authors

Indra Pratama

Muhammad Dzikri Multazam

Ridho Fathoni Zidan