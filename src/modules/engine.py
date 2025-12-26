try:
    import sqlite3
    import pandas as pd
    import numpy as np
    from sklearn.preprocessing import MultiLabelBinarizer
    from sklearn.metrics import pairwise_distances
    from modules.watched_movies import catch_watched_movies
except ImportError as error:  # Colored error message with ANSI codes
    print("\033[1;33m""⚠️  Failed to import modules ""\033[0m", error)

def movie_recommender(db_path: str, user_id: str, recommendation_input, filter_watched: bool, filter_top_rank: bool) -> list[str]:
    '''
    Recommends movies based on user input, using Jaccard similarity on genres and keywords.
    returns List of top 10 recommended movie titles.
    recommendation_input: [[genres], [keywords]]
    '''
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(
        "SELECT movie_id, title, genres, keywords, final_score FROM Movies_sorted",
        conn
    )
    conn.close()
    
    # filter out watched movies (if true)
    if filter_watched:
        watched = catch_watched_movies(db_path, user_id)
        df = df[~df["movie_id"].isin(watched)]

    # Pre-process features
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
    
    encoded_matrix = np.hstack(encoded_features).astype(bool)

    user_vector = np.hstack([encoders[col].transform([val]) 
        for col, val in zip(features, recommendation_input)]).astype(bool)

    # Compute similarities and store in DataFrame
    distances = pairwise_distances(
        encoded_matrix, 
        user_vector.reshape(1, -1), 
        metric="jaccard"
    )
    similarities = 1 - distances.flatten()

    # The old version which was too slow
    # similarities = [jaccard_score(user_vector, encoded_matrix[i]) for i in range(len(encoded_matrix))]

    df["similarity"] = similarities

    #  If True sort by "final_score" and "similarity" then return top 10 
    if filter_top_rank:
        top_list = df.sort_values(by=["similarity", "final_score"], ascending=[False, False]).head(10)
    else:
        # sort by "similarity" and return top 10
        top_list = df.sort_values(by="similarity", ascending=False).head(10)

    recommen_movies = top_list["title"].tolist()
    return recommen_movies

