# Movie Recommendation System Using K-Means Clustering, Content-Based Filtering, and Rule-Based Expert System

This project is a web-based movie recommendation system developed for academic research purposes.  
The system aims to help users select movies efficiently by reducing information overload caused by the large number of available movies on digital platforms.

The application implements three independent recommendation approaches and is deployed as an interactive web application using Streamlit.

---

## Project Objective

The main objective of this project is to develop a movie recommendation system that can provide accurate and relevant movie suggestions using different recommendation techniques.

The system is designed to:
1. Group movies based on popularity and ratings
2. Recommend similar movies based on content characteristics
3. Provide rule-based recommendations based on user preferences

---

## Recommendation Methods

The system implements three recommendation methods, each available through a separate tab in the application.

### K-Means Clustering

K-Means Clustering is used to group movies based on numerical features, specifically:
1. IMDb rating
2. Number of votes

The data is normalized using MinMaxScaler before clustering.  
Based on validation using the Elbow Method, Silhouette Score, and Davies–Bouldin Index, the optimal number of clusters is set to two.

The resulting clusters are interpreted as:
1. Popular Movies
2. Less-Popular Movies

---

### Content-Based Filtering

Content-Based Filtering is used to recommend movies similar to a selected movie.

Movie attributes such as:
1. genres
2. directors
3. writers  

are combined into a single text feature.  
The similarity between movies is calculated using TF-IDF vectorization and Cosine Similarity.

The system returns the top-N most similar movies based on content similarity scores.

---

### Rule-Based Expert System

The Rule-Based Expert System generates recommendations using predefined IF–THEN rules based on user preferences.

The rules consider:
1. Minimum rating
2. Minimum number of votes
3. Selected genres
3. Selected movie cluster

A special rule is applied:
If rating ≥ 8.0 and votes ≥ 10000, movies are prioritized from the popular movie cluster.

The final recommendation consists of the top 10 movies that satisfy all applied rules.

---

## Features

1. Rule-based movie recommendation using IF–THEN logic  
2. Similar movie recommendation using content similarity  
3. Movie clustering exploration based on popularity  
4. Movie search by title, genre, director, writer, or plot keywords  

---

## Technologies Used

- Python  
- Streamlit  
- Pandas  
- NumPy  
- Scikit-learn  
- deep-translator

---

## Dataset Source

The dataset used in this project consists of 5000 movies.

Movie IDs and titles were obtained from IMDb.  
Additional movie attributes such as genres, release year, rating, votes, runtime, directors, writers, links, posters, and plot summaries were retrieved using the OMDb API.

IMDb: https://www.imdb.com  
OMDb API: https://www.omdbapi.com  

The dataset was collected, processed, and structured for academic and experimental purposes.

---

## Dataset Attributes

The dataset contains the following attributes:

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

---

## Project Structure

```text
movie-recommendation-system/
├── app.py
├── preprocessing.py
├── requirements.txt
├── README.md

---

## Installation and Usage

To run the application locally:

1. Clone the repository
git clone https://github.com/pratama1773/movie-recommendation-system.git

2. Navigate to the project directory  
cd movie-recommendation-system

3. Install required dependencies  
pip install -r requirements.txt

4. Run the application  
streamlit run app.py

---

## Author

Indra Pratama
Muhammad Dzikri Multazam
Ridho Fathoni Zidan