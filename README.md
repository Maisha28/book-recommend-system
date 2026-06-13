# BookMind

BookMind is a book recommendation system built using collaborative filtering. It helps readers discover new books based on the preferences of similar readers.The project uses a user-book rating matrix and cosine similarity to generate personalized recommendations. Simply select a book, and BookMind suggests similar books that readers with comparable interests have enjoyed.

## Tech Stack

* Python
* Pandas
* NumPy
* Scikit-Learn
* Streamlit

## How It Works

1. User selects a book from the collection.
2. The system finds books with similar reader engagement patterns.
3. Cosine similarity is used to measure similarity between books.
4. The top matching books are displayed along with their covers and match scores.

## Live Demo

Try the application here:

https://book-recommendation-system-maisha-book-mind.streamlit.app/

## Project Structure

BookMind/
│
├── app.py
├── requirements.txt
│
└── model/
    ├── pt.pkl
    ├── books.pkl
    └── similarity_scores.pkl

## Future Improvements

* Hybrid recommendation system
* Personalized user profiles
* Genre-based filtering
* Advanced search and recommendations
* Larger recommendation dataset


