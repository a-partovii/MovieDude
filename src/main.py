try:
    from scripts.login import login
    from modules import *
    from rich.console import Console
    console = Console()
    sep_line = "[cyan]-[/cyan]" * 50 # Graphicall seprator line in terminal
except ImportError as error: # Colored error message with ANSI codes
    print("\033[1;33m""⚠️  Failed to import modules ""\033[0m", error)

def main(): 
    # Set the path to the SQLite database
    db_path = "YOUR/PATH/HERE/MovieDude.db"
    user_id = login(db_path)
    
    # Features for controlling engine options
    filter_watched = False
    filter_top_rank = False

    console.print(sep_line)
    console.print(
        "[bold]1[/bold] : Discover Movies Based on Your Activities\n"
        "[bold]2[/bold] : Find Similar Movies by Given Movie Title"
    )
    
    recommend_movies = []
    while True:
        choice = input("\nEnter your choice: ")
        if choice == "1" :
            console.print(sep_line)
            with console.status("Working..."):
                recommend_movies = movie_recommender(db_path, user_id, find_user_interests(db_path, user_id), filter_watched, filter_top_rank)
                print_titles(recommend_movies)
                break

        elif choice == "2" :
            console.print(sep_line)
            while True:
                title_query = input("Enter a movie title to find similar recommendations: ").strip()
                if recommendation_input:= find_by_title(db_path, title_query):
                    with console.status("Working..."):
                        recommend_movies = movie_recommender(db_path, user_id, recommendation_input, filter_watched, filter_top_rank)
                        print_titles(recommend_movies)
                    break
            break

        else:
            console.print("[yellow]Invalid option![/yellow] try again...")
        
def print_titles(recommend_titles):
    console.print("\n[cyan]Top 10 Recommended Similar Movies:[cyan] ")

    for i, title in enumerate(recommend_titles, 1):
        print(f"{i}. {title}")

if __name__ == "__main__":
    main()

input(">>>")
