try:
    import sqlite3
    import pandas as pd
    from sklearn.preprocessing import MinMaxScaler
    from collections import Counter
    from itertools import chain

except ImportError as error:
    # Colored error message with ANSI codes
    print("\033[1;33m""⚠️  Failed to import modules: ""\033[0m", error)

def find_user_interests(db_path, user_id):
    # Number of each feature to return
    top_n_genres = 6 
    top_n_keywords = 10

    # Giving weight to features as their value in the processing
    col1 = "user_rate"
    col2 = "liked"
    w1 = 0.75
    w2 = 0.25

    conn = sqlite3.connect(db_path)
    query = '''
    SELECT ud.user_id, ud.movie_id, ud.user_rate, ud.liked, ms.genres, ms.keywords
    FROM Users_data ud
    JOIN Movies_sorted ms ON ud.movie_id = ms.movie_id
    WHERE ud.user_id = ?
    '''
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()

    if df.empty:
        print(f"No activity found for user '{user_id}' in Users_data.")
        return [], []

    # Normalize user ratings
    scaler = MinMaxScaler()
    df["normalized_rate"] = scaler.fit_transform(df[[col1]])
    df["like_weight"] = df[col2].astype(int)

    # Calculate the final score combining normalized rating and like weight
    df["final_score"] = w1 * df["normalized_rate"] + w2 * df["like_weight"]
    # Sort the DataFrame by the final score in descending order
    df = df.sort_values(by="final_score", ascending=False)
    top_list = len(df) // 3 
    df = df.head(top_list)

    # convert to lowercase and split by comma+space
    df["genres"] = df["genres"].str.lower().str.split(", ")
    df["keywords"] = df["keywords"].str.lower().str.split(", ")

    top_genres = Counter(chain.from_iterable(df["genres"].dropna())).most_common(top_n_genres)
    top_keywords = Counter(chain.from_iterable(df["keywords"].dropna())).most_common(top_n_keywords)

    return [g[0] for g in top_genres], [k[0] for k in top_keywords]
