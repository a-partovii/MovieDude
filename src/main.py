try:
    from scripts.login import login
    from modules import *
    from termcolor import colored

except ImportError as error:
    # Colored error message with ANSI codes
    print("\033[1;33m""⚠️  Failed to import modules: ""\033[0m", error)

sep_line = "-" * 50 # Graphicall seprator line in terminal

def main(): 
    # Set the path to the SQLite database
    db_path = "your/path/here/MovieDude.db" 
    user_id = login(db_path)

    # Features for controlling engine options
    filter_watched = True
    filter_top_rank = True

    print(colored(sep_line, "cyan"))
    print("1 : Discover Movies Based on Your Activities\n2 : Find Similar Movies by Given Movie Title")
    
    recommend_movies = []
    while True:
        choice = input("\nEnter your choice: ")
        if choice == "1" :
            print(colored(sep_line, "cyan"))
            recommmend_movies = movie_recommender(user_id, db_path, find_by_title(db_path), filter_watched, filter_top_rank)
            movie_recommender(user_id, db_path, find_user_interests(db_path, user_id), filter_watched, filter_top_rank)
            print_titles(recommend_movies)
            break
        elif choice == "2" :
            print(colored(sep_line, "cyan"))
            title_query = input("Enter a movie title to find similar recommendations: ").strip()
            recommmend_movies = movie_recommender(user_id, db_path, find_by_title(db_path, title_query), filter_watched, filter_top_rank)
            print_titles(recommend_movies)
            break
        else:
            print("Invalid option!")
        
def print_titles(recommend_movies):
    print("\nTop 10 Recommended Similar Movies: ")

    for i, title in enumerate(recommend_movies, 1):
        print(f"{i}. {title}")

if __name__ == "__main__":
    main()
input(">>>")