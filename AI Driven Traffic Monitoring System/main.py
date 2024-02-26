import tkinter as tk
import tkinter.font as tkFont
import mysql.connector
import subprocess
from tkinter import messagebox

def showlogin():
    print("Loginside")


    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '1234',
        'database': 'traffic_db',
    }

    root = tk.Tk()
    root.title("Login Page")
    root.configure(bg="#202124", width=100, height=100)

    # Toggle Fullscreen
    root.attributes('-fullscreen', True)

    def toggle_fullscreen(event=None):
        state = root.attributes('-fullscreen')
        root.attributes('-fullscreen', not state)

    # Stop Program
    def stop_program(event):
        root.quit()

    root.bind('<KeyPress-Escape>', toggle_fullscreen)
    root.bind('x', stop_program)

    for i in range(8):
        root.grid_rowconfigure(i, weight=1)
        root.grid_columnconfigure(i, weight=1)

    root.grid_rowconfigure(2, weight=4)

    def Close_login():
        root.destroy()



    def login():
        username = entry_username.get()
        password = entry_password.get()

        if not username or not password:
            messagebox.showerror("Login Failed", "Username and Password cannot be empty")
            return

        # Connect to the MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Check if the username and password exist in the user_accounts table
        query = "SELECT * FROM users_accounts WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        # Check if the username and password exist in the admin_accounts table
        query_admin = "SELECT * FROM admin_accounts WHERE username=%s AND password=%s"
        cursor.execute(query_admin, (username, password))
        admin = cursor.fetchone()

        # Close the database connection
        connection.close()

        if user:
            root.destroy()
            subprocess.call(["python", "mapside.py"])
        elif admin:
            root.destroy()
            subprocess.call(["python", "adminside.py"])
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password")
            cursor.close()


    font = tkFont.Font(family="Helvetica", size=15, weight="bold")
    button_font = tkFont.Font(family="Helvetica", size=10, weight="bold")

    app_label = tk.Label(root, text="TacTMS", fg="#00ECC2", bg="#202124",  font=("Helvetica", 50, "bold"))
    app_label.pack(pady=105)

    label_username = tk.Label(root, text="USERNAME", width=20, fg="#00ECC2", bg="#202124", font=font,
                              anchor="s")
    label_username.pack()
    entry_username = tk.Entry(root, width=20, fg="#232323", bg="white", font=font, justify="center")
    entry_username.pack()
    label_password = tk.Label(root, text="PASSWORD", width=20, fg="#00ECC2", bg="#202124", font=font, anchor="n")
    label_password.pack()
    entry_password = tk.Entry(root, show="*", width=20, fg="#232323", bg="white",
                              font=font, justify="center")
    entry_password.pack()

    # place the login button
    login_button = tk.Button(root, text="LOGIN", command=login, width=20, height=2, bg="#00ECC2",
                             fg="black", font=button_font)
    login_button.pack(pady=20)

    close_button = tk.Button(root, text="EXIT", command=Close_login, width=20, height=2, bg="#FF0303", fg="black",
                             font=button_font)
    close_button.pack()

    # Tkinter main loop
    root.mainloop()

showlogin()