import sqlite3

def find_by_title(db_path, title):
        '''
            Returns genres and keywords for a movie by title from the SQLite database.
        '''
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()

                query = """
                SELECT genres, keywords
                FROM Movies_sorted
                WHERE title LIKE ?
                COLLATE NOCASE
                LIMIT 1
                """
                # Execute query to find the movie by title
                cursor.execute(query, (f"%{title}%",))
                result = cursor.fetchone()

                if result:
                    genres_raw, keywords_raw = result

                    genres = [g.strip().lower() for g in genres_raw.split(',') if g.strip()]
                    keywords = [k.strip().lower() for k in keywords_raw.split(',') if k.strip()]

                    return [genres, keywords]

                else:
                    print("No matching movie found.\n")
                    return 

        except sqlite3.Error as error:
            print(f"❌SQLite error: ", error)
            return 

