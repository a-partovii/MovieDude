try:
    from scripts.login import login
    from modules import *
    from termcolor import colored

except ImportError as error:
    print("⚠️ Modules could not be imported: ", error)

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
    
    while True:
        choice = input("\nEnter your choice: ")
        if choice == "1" :
            print(colored(sep_line, "cyan"))
            recommender_movies(user_id, db_path, find_user_interests(db_path, user_id), filter_watched, filter_top_rank)
            break
        elif choice == "2" :
            print(colored(sep_line, "cyan"))
            recommender_movies(user_id, db_path, find_by_title(db_path), filter_watched, filter_top_rank)
            break
        else:
            print("Invalid option!")
        

if __name__ == "__main__":
    main()
input(">>>")