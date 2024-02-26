import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
import mysql.connector
import subprocess

def toggle_fullscreen(event=None):
    state = root.attributes('-fullscreen')
    root.attributes('-fullscreen', not state)

def stop_program(event):
    root.quit()


class TrafficApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Traffic App")
        self.root.geometry("1920x1080")
        self.root.attributes('-fullscreen', True)
        self.root.bind('<KeyPress-Escape>', toggle_fullscreen)
        self.root.bind('x', stop_program)
        self.current_table = None  # current table being displayed
        self.create_dashboard()



    def create_dashboard(self):
        style = ttk.Style()
        style.configure("TFrame", background="#202124")
        style.configure("TButton", padding=(30, 15), background="#202124", foreground="#00ECC2", font=('Helvetica', 12, 'bold'))
        style.configure("TEntry", padding=(30, 15))
        style.configure("Treeview.Heading", font=('Helvetica', 13, 'bold'))
        style.configure("Treeview", font=('Helvetica', 13))
        style.configure("TEntry", background="#202124")
        style.configure("Red.TButton", foreground="red")






        self.dashboard_frame = ttk.Frame(self.root)
        self.dashboard_frame.pack(fill="both", expand=True)

        self.user_button = ttk.Button(self.dashboard_frame, text="USERS", command=self.show_users)
        self.user_button.grid(row=1, column=0, padx=50, pady=10, sticky='nsw')

        self.admin_button = ttk.Button(self.dashboard_frame, text="ADMIN", command=self.show_admin)
        self.admin_button.grid(row=1, column=1, padx=50, pady=10, sticky='nsw')

        self.daily_history_button = ttk.Button(self.dashboard_frame, text="DAILY HISTORY", command=self.show_daily_history)
        self.daily_history_button.grid(row=1, column=2, padx=50, pady=10, sticky='nsw')

        self.weekly_history_button = ttk.Button(self.dashboard_frame, text="WEEKLY HISTORY", command=self.show_weekly_history)
        self.weekly_history_button.grid(row=1, column=3, padx=50, pady=10, sticky='nsw')

        self.monthly_history_button = ttk.Button(self.dashboard_frame, text="MONTHLY HISTORY",
                                                      command=self.show_monthly_history)
        self.monthly_history_button.grid(row=1, column=4, padx=50, pady=10, sticky='nsw')

        self.add_button = ttk.Button(self.dashboard_frame, text="ADD", command=self.add_entry)
        self.add_button.grid(row=3, column=0, padx=50, pady=10, sticky='nsw')

        self.edit_button = ttk.Button(self.dashboard_frame, text="EDIT", command=self.edit_entry)
        self.edit_button.grid(row=3, column=1, padx=50, pady=10, sticky='nsw')

        self.delete_button = ttk.Button(self.dashboard_frame, text="DELETE", command=self.delete_entry)
        self.delete_button.grid(row=3, column=2, padx=50, pady=10, sticky='nsw')


        self.search_button = ttk.Button(self.dashboard_frame, text="SEARCH", command=self.search_entries)
        self.search_button.grid(row=3, column=3,padx=50 ,  pady=10, sticky='nsw')

        search_frame = ttk.Frame(self.dashboard_frame)
        search_frame.grid(row=3, column=4, sticky='nsew')

        self.search_label = ttk.Label(search_frame, text="SEARCH:", font=('Helvetica', 13, 'bold'),
                                      background="#202124", foreground='#00ECC2')
        self.search_label.grid(row=0, column=0, sticky='nse')

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=('Helvetica', 13, 'bold'))
        self.search_entry.grid(row=0, column=1, pady=10, sticky='nsw')

        self.logout_button = ttk.Button(self.dashboard_frame, text="LOGOUT", command=self.logout, style="Red.TButton")
        self.logout_button.grid(row=4, column=0, padx=50, pady=70, sticky='nsw')

        self.table_frame = ttk.Frame(self.dashboard_frame)
        self.table_frame.grid(row=2, column=0, columnspan=10, pady=10, padx=10, sticky='nsw')

        self.admin = ttk.Label(self.dashboard_frame, text="TacTMS ADMIN", font=('Helvetica', 20, 'bold'),
                                      background="#202124", foreground='#00ECC2')
        self.admin.grid(row=0, column=0, sticky='nw', padx=10,pady=30)






    def logout(self):
        root.destroy()
        subprocess.call(["python", "main.py"])


    def disable_buttons(self):
        self.add_button.state(['disabled'])
        self.edit_button.state(['disabled'])


    def enable_buttons(self):
        self.add_button.state(['!disabled'])
        self.edit_button.state(['!disabled'])
        self.delete_button.state(['!disabled'])

    def show_daily_history(self):
        self.current_table = "traffic_history"
        self.clear_table()
        self.create_table(self.current_table,
                          ["ID", "Cam Location", "Date Time", "Daily Congestion", "Congestion Time"])
        self.add_data_to_table(self.current_table)
        self.disable_buttons()
    def show_weekly_history(self):
        self.current_table = "traffic_history_weekly"
        self.clear_table()
        self.create_table(self.current_table,
                          ["ID", "Cam Location", "Start Date", "End Date", "Date Time", "Weekly Congestion", "Total Congestion Time"])
        self.add_data_to_table(self.current_table)
        self.disable_buttons()


    def show_monthly_history(self):
        self.current_table = "traffic_history_monthly"
        self.clear_table()
        self.create_table(self.current_table,
                          ["ID", "Cam Location", "Start Date", "End Date", "Date Time", "Monthly Congestion", "Total Congestion Time"])
        self.add_data_to_table(self.current_table)
        self.disable_buttons()

    def show_users(self):
        self.current_table = "users_accounts"
        self.clear_table()
        self.create_table(self.current_table, ["ID", "First Name", "Last Name", "Username", "Password"])
        self.add_data_to_table(self.current_table)
        self.enable_buttons()

    def show_admin(self):
        self.current_table = "admin_accounts"
        self.clear_table()
        self.create_table(self.current_table, ["ID", "First Name", "Last Name", "Username", "Password"])
        self.add_data_to_table(self.current_table)
        self.enable_buttons()

    def clear_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

    def create_table(self, table_name, columns):

        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=20)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=200, anchor="center")
        self.tree.pack(side="left", fill="y")

        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def add_data_to_table(self, table_name):
        connection = self.connect_to_database()

        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        for row in rows:
            self.tree.insert("", "end", values=row, iid=row[0])

        connection.close()

    def add_entry(self):
        entry_data = self.get_entry_data()
        if entry_data:
            connection = self.connect_to_database()

            cursor = connection.cursor()
            cursor.execute(
                f"INSERT INTO {self.current_table} (firstname, lastname, username, password) VALUES (%s, %s, %s, %s)",
                entry_data
            )

            connection.commit()
            connection.close()

            # Refresh the dashboard after adding an entry
            if self.current_table == "admin_accounts":
                self.show_admin()
            else:
                self.show_users()

    def edit_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        entry_values = self.tree.item(selected_item[0])['values']  # Get the values of the selected item
        entry_id = entry_values[0]



        entry_data = self.get_entry_data(edit=True)
        if entry_data:
            connection = self.connect_to_database()

            cursor = connection.cursor()

            password = entry_data[3] if entry_data[3] else self.get_password_for_id(entry_id)
            cursor.execute(
                f"UPDATE {self.current_table} SET firstname=%s, lastname=%s, username=%s, password=%s WHERE id=%s",
                (entry_data[0], entry_data[1], entry_data[2], password, entry_id)
            )

            connection.commit()
            connection.close()

            # Refresh the dashboard after editing an entry
            if self.current_table == "admin_accounts":
                self.show_admin()
            else:
                self.show_users()

    def delete_entry(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        entry_values = self.tree.item(selected_item[0])['values']
        entry_id = entry_values[0]

        connection = self.connect_to_database()

        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {self.current_table} WHERE id=%s", (entry_id,))

        connection.commit()
        connection.close()

        if self.current_table == "admin_accounts":
            self.show_admin()
        elif self.current_table == "traffic_history":
            self.show_daily_history()
        elif self.current_table == "traffic_history_weekly":
            self.show_weekly_history()
        elif self.current_table == "traffic_history_monthly":
            self.show_monthly_history()
        else:
            self.show_users()

    def search_entries(self):

        match self.current_table:

            case "traffic_history":
                    search_term = self.search_var.get()
                    if not search_term:
                        return

                    connection = self.connect_to_database()

                    cursor = connection.cursor()
                    cursor.execute(
                        f"SELECT * FROM {self.current_table} WHERE id LIKE %s OR cam_location LIKE %s OR date_time LIKE %s OR daily_congestion LIKE %s OR congestion_time LIKE %s",
                        (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%",
                         f"%{search_term}%")
                    )
                    self.clear_table()
                    self.create_table(self.current_table,
                                      ["ID", "Cam Location", "Date Time", "Daily Congestion", "Congestion Time"])
                    rows = cursor.fetchall()
                    for row in rows:
                        self.tree.insert("", "end", values=row)
                    connection.close()

            case "traffic_history_weekly":
                search_term = self.search_var.get()
                if not search_term:
                    return

                connection = self.connect_to_database()

                cursor = connection.cursor()
                cursor.execute(
                    f"SELECT * FROM {self.current_table} WHERE id LIKE %s OR cam_location LIKE %s OR date_time LIKE "
                    f"%s OR weekly_congestion LIKE %s OR total_congestion_time LIKE %s OR  start_date LIKE %s OR "
                    f"end_date LIKE %s",
                    (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%",
                     f"%{search_term}%",f"%{search_term}%",f"%{search_term}%")
                )

                self.clear_table()
                self.create_table(self.current_table,
                                  ["ID", "Cam Location", "Start Date", "End Date", "Date Time", "Weekly Congestion", "Total Congestion Time"])
                rows = cursor.fetchall()

                for row in rows:
                    self.tree.insert("", "end", values=row)

                connection.close()

            case "traffic_history_monthly":
                search_term = self.search_var.get()
                if not search_term:
                    return

                connection = self.connect_to_database()

                cursor = connection.cursor()
                cursor.execute(
                    f"SELECT * FROM {self.current_table} WHERE id LIKE %s OR cam_location LIKE %s OR date_time LIKE "
                    f"%s OR monthly_congestion LIKE %s OR total_congestion_time LIKE %s OR  start_date LIKE %s OR "
                    f"end_date LIKE %s",
                    (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%",
                     f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
                )

                self.clear_table()
                self.create_table(self.current_table,
                                  ["ID", "Cam Location", "Start Date", "End Date", "Date Time", "Monthly Congestion", "Total Congestion Time"])
                rows = cursor.fetchall()

                for row in rows:
                    self.tree.insert("", "end", values=row)

                connection.close()



            case _:
                search_term = self.search_var.get()
                if not search_term:
                    return

                connection = self.connect_to_database()

                cursor = connection.cursor()
                cursor.execute(
                    f"SELECT * FROM {self.current_table} WHERE id LIKE %s OR firstname LIKE %s OR lastname LIKE %s OR username LIKE %s OR password LIKE %s",
                    (f"%{search_term}%",f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%")
                )

                self.clear_table()
                self.create_table(self.current_table, ["ID", "First Name", "Last Name", "Username", "Password"])
                rows = cursor.fetchall()

                for row in rows:
                    self.tree.insert("", "end", values=row)

                connection.close()





    def get_entry_data(self, edit=False):
        popup = simpledialog.Toplevel(self.root)
        popup.title("Enter Data")

        ttk.Label(popup, text="First Name:").grid(row=0, column=0, padx=10, pady=10)
        ttk.Label(popup, text="Last Name:").grid(row=1, column=0, padx=10, pady=10)
        ttk.Label(popup, text="Username:").grid(row=2, column=0, padx=10, pady=10)
        ttk.Label(popup, text="Password:").grid(row=3, column=0, padx=10, pady=10)

        first_name_var = tk.StringVar()
        last_name_var = tk.StringVar()
        username_var = tk.StringVar()
        password_var = tk.StringVar()

        ttk.Entry(popup, textvariable=first_name_var).grid(row=0, column=1, padx=10, pady=10)
        ttk.Entry(popup, textvariable=last_name_var).grid(row=1, column=1, padx=10, pady=10)
        ttk.Entry(popup, textvariable=username_var).grid(row=2, column=1, padx=10, pady=10)


        password_entry = ttk.Entry(popup, textvariable=password_var, show="*")
        password_entry.grid(row=3, column=1, padx=10, pady=10)

        if edit:

            first_name_var.set(self.tree.item(self.tree.selection())['values'][1])
            last_name_var.set(self.tree.item(self.tree.selection())['values'][2])
            username_var.set(self.tree.item(self.tree.selection())['values'][3])
            password_var.set(self.tree.item(self.tree.selection())['values'][4])

        def save_data():
            return first_name_var.get(), last_name_var.get(), username_var.get(), password_var.get()

        ttk.Button(popup, text="Save", command=popup.destroy).grid(row=4, column=0, columnspan=2, pady=10)

        self.root.wait_window(popup)
        return save_data()

    def get_password_for_id(self, entry_id):
        connection = self.connect_to_database()
        cursor = connection.cursor()

        cursor.execute(f"SELECT password FROM {self.current_table} WHERE id=%s", (int(entry_id),))
        password = cursor.fetchone()[0]

        connection.close()
        return password

    def connect_to_database(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="1234",
            database="traffic_db"
        )
print("AdminSide")
if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficApp(root)
    root.mainloop()
