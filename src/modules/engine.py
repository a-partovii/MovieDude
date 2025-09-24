try:
    import sqlite3
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import MultiLabelBinarizer
    from sklearn.metrics import jaccard_score
    from scripts.watched_movies import catch_watched_movies
    from termcolor import colored
    
except ImportError as error:
    print("⚠️ Modules could not be imported: ", error)

def recommender_movies(user_id, db_path, user_input, filter_watched, filter_top_rank):

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

    X = np.hstack(encoded_features)

    user_vector = np.hstack([
        encoders[features[i]].transform([user_input[i]]) for i in range(len(features))
    ]).flatten()

    # filter watched movies(if true)
    if filter_watched:
        watched_movies = catch_watched_movies(db_path, user_id) if filter_watched else []
        df = df[~df["movie_id"].isin(watched_movies)]
        X = X[df.index]

    similarities = [jaccard_score(user_vector, X[i]) for i in range(len(X))]
    df["similarity"] = similarities

    # Get top 25 similar movies, then sort by final_score(if True) and show top 10 by those score
    top_list = df.sort_values(by="similarity", ascending=False).head(25)
    if filter_top_rank:
        top_list = top_list.sort_values(by="final_score", ascending=False).head(10)
    top_list = top_list.head(10)
    titles = top_list["title"].tolist()


    print(colored("\nTop 10 Recommended Similar Movies:", "cyan"))
    for i, title in enumerate(titles, 1):
        print(f"{i}. {title}")
