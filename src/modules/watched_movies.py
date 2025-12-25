try:
    import sqlite3 
    import pandas as pd  
except ImportError as error: # Colored error message with ANSI codes
    print("\033[1;33m""⚠️  Failed to import modules ""\033[0m", error)

def catch_watched_movies(db_path, user_id):
    """
    Gets watched movie_id-s by user
    """
    try:
        with sqlite3.connect(db_path) as conn:
            query = "SELECT movie_id FROM Users_data WHERE user_id = ?"
            df = pd.read_sql(query, conn, params=(user_id,))
            return df['movie_id'].tolist()
        
    except Exception as error:
        print(f"Error: ", error)
        return []