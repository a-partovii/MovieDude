try:
    import sqlite3
    from rich.console import Console
    console = Console()
except ImportError as error: # Colored error message with ANSI codes
    print("\033[1;33m""⚠️  Failed to import modules ""\033[0m", error)
    
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
            console.print("[red]❌ Username not found. Please try again.[/red]\n")
        elif user['password'] != password:
            console.print("❌ [red]Incorrect password. Please try again.[/red]\n")
        else:
            console.print(f"\n✅ Welcome, [yellow]{user['name']}[/yellow]")
            cursor.close()
            conn.close()
            return user_id
