try:
    import sqlite3
    from termcolor import colored

except ImportError as error:
    print("⚠️ Modules could not be imported: ", error)
    
def login(db_file):
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    while True:
        user_id = input("Enter user ID: ").strip()
        password = input("Enter password: ").strip()

        cursor.execute("SELECT * FROM Users WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()

        if not user:
            print("❌ Username not found. Please try again.\n")
        elif user['password'] != password:
            print("❌ Incorrect password. Please try again.\n")
        else:
            print("\n✅ Welcome,",colored(f"{user['name']}", "yellow"))
            cursor.close()
            conn.close()
            return user_id
