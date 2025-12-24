try:
    import sqlite3
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import MultiLabelBinarizer
    from sklearn.metrics import jaccard_score
    from modules.watched_movies import catch_watched_movies
except ImportError as error: # Colored error message with ANSI codes
    print("\033[1;33m""⚠️  Failed to import modules ""\033[0m", error)

def movie_recommender(db_path, user_id, recommendation_input, filter_watched, filter_top_rank):
    '''
    Recommends movies based on user input using Jaccard similarity on genres and keywords.
    returns List of top 10 recommended movie titles.
    '''
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM Movies_sorted", conn)

    # Preprocess features
    features = ["genres", "keywords"]
    for col in features:
        df[col] = df[col].fillna("").str.lower().str.strip().str.split(",")
        df[col] = df[col].apply(lambda x: [item.strip() for item in x if item.strip()])

    # Binarization encoding
    encoders = {}
    encoded_features = []
    for col in features:
        mlb = MultiLabelBinarizer()
        encoded = mlb.fit_transform(df[col])
        encoded_features.append(encoded)
        encoders[col] = mlb
    encoded_matrix = np.hstack(encoded_features)

    user_vector = np.hstack([
        encoders[features[i]].transform([recommendation_input[i]]) for i in range(len(features))]).flatten()

    # filter watched movies (if true)
    if filter_watched:
        watched_movies = catch_watched_movies(db_path, user_id) if filter_watched else []
        df = df[~df["movie_id"].isin(watched_movies)]
        encoded_matrix = encoded_matrix[df.index]

    similarities = [jaccard_score(user_vector, encoded_matrix[i]) for i in range(len(encoded_matrix))]
    df["similarity"] = similarities

    # Get top 25 similar movies, then sort them by "final_score" (if True) and show top 10 by those scores
    top_list = df.sort_values(by="similarity", ascending=False).head(25)
    if filter_top_rank:
        top_list = top_list.sort_values(by="final_score", ascending=False).head(10)
    top_list = top_list.head(10)
    recommen_movies = top_list["title"].tolist()

    return recommen_movies

