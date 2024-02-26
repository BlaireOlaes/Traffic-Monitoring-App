import cv2
import tkinter as tk
import tkinter.font as tkFont
from PIL import Image, ImageTk
import numpy as np
import threading
import time
import datetime
import mysql.connector
import subprocess
from tkinter import ttk

# Load YOLOv4 weights and configuration
net = cv2.dnn.readNet("dnn_model/yolov3-416.weights", "dnn_model/yolov3-416.cfg")

# Load YOLOv4 classes
classes = []
with open('dnn_model/classes.txt', 'r') as f:
    classes = f.read().strip().split('\n')

layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Initialize the video capture
video = 'testvid/4k highway.mp4'
cap = cv2.VideoCapture(video)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# Initialize Tkinter
app = tk.Tk()
app.title("Traffic Detection")
app.configure(bg="#232323")

# Toggle Fullscreen
app.attributes('-fullscreen', True)  # can be set to True


def toggle_fullscreen(event=None):
    state = app.attributes('-fullscreen')
    app.attributes('-fullscreen', not state)


# Toggle Stop Program
def stop_program(event):
    app.quit()


app.bind('z', toggle_fullscreen)
app.bind('x', stop_program)

for i in range(8):
    app.grid_rowconfigure(i, weight=1)
    app.grid_columnconfigure(i, weight=1)

app.grid_rowconfigure(2, weight=4)


# time
def update_time_label():
    current_time = datetime.datetime.now().strftime("%I:%M%p : %m/%d/%y")
    time_label.config(text=current_time)
    app.after(1000, update_time_label)


# Labels
title_font = tkFont.Font(family="Inter", size=15, weight="bold")

title_label = tk.Label(app, text="Traffic Monitoring System", width=20, height=1,
                       fg="#EB5E28", bg="#232323", font=title_font, anchor="w")
title_label.grid(row=0, column=0, columnspan=8, sticky="nsew")

cam_location = tk.Label(app, text="CAM 30 Highway 1", width=20, padx=20, height=1,
                        fg="white", bg="#232323", font=title_font, anchor="w")
cam_location.grid(row=1, column=0, columnspan=8, sticky="nsew")

time_label = tk.Label(app, text="", width=20, height=1, fg="white", padx=250, bg="#232323", font=title_font, anchor="e")
time_label.grid(row=1, column=1, columnspan=8, sticky="nsew")
update_time_label()

# Screen
main_background = tk.Canvas(app, width=1920, height=1080, background="#232323")
main_background.grid(row=2, column=0, rowspan=4, columnspan=4, sticky="nsew")

# Define the desired video size (720p)
video_width = 1280
video_height = 780

border_color = "#EB5E28"

video_frame = tk.Frame(main_background, background="#232323", padx=10, pady=5)  # Adding padding
video_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="nsew")  # Place it within main_background

vid_widget = tk.Label(video_frame, width=video_width, height=video_height, background="#232323",
                      highlightbackground=border_color, highlightthickness=5)  # Adding border
vid_widget.pack(fill="both", expand=True)

# Fonts
text_font = tkFont.Font(family="Inter", size=16, weight="bold")
stats_font = tkFont.Font(family="Inter", size=12, weight="bold")
stats2_font = tkFont.Font(family="Inter", size=15, weight="bold")

# Vehicle Model Panel
labels_label = tk.Label(app, text="Vehicle Model Count", fg="white", bg="#232323", font=text_font, justify="center")
labels_label.grid(row=2, column=4, sticky="n")
vehicle_label = tk.Label(app, text="Vehicle", width=20, background="#FFFFFF", height=5, font=stats_font,
                         highlightbackground=border_color, highlightthickness=3, justify="left")
vehicle_label.grid(row=2, column=4, sticky="n", padx=10, pady=30)



# Vehicle Count Panel
labels_label = tk.Label(app, text="Total Vehicle Count", fg="white", bg="#232323", font=text_font, justify="center")
labels_label.grid(row=2, column=4, sticky="n", padx=0, pady=170)
stats_label = tk.Label(app, text="Stats", width=17, height=3, background="#FFFFFF", font=stats2_font,
                       highlightbackground=border_color, highlightthickness=3, justify="center")
stats_label.grid(row=2, column=4, sticky="n", padx=10, pady=200)

# Congestion Panel
labels_label = tk.Label(app, text="Congestion Level", fg="white", bg="#232323", font=text_font, justify="center")
labels_label.grid(row=2, column=4, sticky="n", padx=0, pady=300)
congestion_label = tk.Label(app, text="Congestion", width=17, height=3, font=stats2_font,
                            background="#FFFFFF", highlightbackground=border_color, highlightthickness=3,
                            justify="center")
congestion_label.grid(row=2, column=4, sticky="n", padx=10, pady=330)

# Congestion Duration Panel
labels_label = tk.Label(app, text="Traffic Duration", fg="white", bg="#232323", font=text_font, justify="center")
labels_label.grid(row=2, column=4, sticky="s", padx=0, pady=300)
duration_label = tk.Label(app, text="Duration", width=17, height=3, font=stats2_font, background="#FFFFFF",
                          highlightbackground=border_color, highlightthickness=3, justify="center")
duration_label.grid(row=2, column=4, sticky="s", padx=10, pady=220)


def view_traffic_history():
    # Create a new window to display traffic history
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'), foreground="#EB5E28")
    style.configure("Treeview", font=('Helvetica', 9), rowheight=50, background="#232323", fieldbackground="#232323",
                    foreground="white")

    history_window = tk.Toplevel(app)
    history_window.title("Daily Traffic History")

    # Set the position of the window (adjust the values as needed)
    window_x = 100  # X-coordinate of the window
    window_y = 100  # Y-coordinate of the window
    history_window.geometry(f"+{window_x}+{window_y}")

    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="1234",
        database="traffic_db"
    )
    mycursor = mydb.cursor()

    # Execute a SELECT query to fetch data from the traffic_history table
    mycursor.execute("SELECT id, cam_location, date_time, daily_congestion, congestion_time FROM traffic_history")
    data = mycursor.fetchall()

    # Create a treeview widget to display the data
    tree = ttk.Treeview(history_window,
                        columns=("ID", "Cam Location", "Date/Time", "Daily Congestion", "Congestion Time"),
                        show='headings')
    tree.heading("#1", text="ID")
    tree.heading("#2", text="Cam Location")
    tree.heading("#3", text="Date/Time")
    tree.heading("#4", text="Daily Congestion")
    tree.heading("#5", text="Congestion Time")

    tree.pack()

    # Adjust the width of columns based on content
    for col in ("ID", "Cam Location", "Date/Time", "Daily Congestion", "Congestion Time"):
        tree.column(col, width=200, anchor='center')

    # Insert data into the treeview
    for row in data:
        tree.insert("", "end", values=row)

    mydb.close()

    frame = tk.Frame(history_window)
    frame.pack(side="bottom")
    button_font = tkFont.Font(family='Helvetica', size=12, weight='bold')

    daily_button = tk.Button(frame, text="Daily", width=20, height=3, bg="#EB5E28", fg="black", font=button_font,
                             command=view_traffic_history)
    daily_button.pack(side="left", padx=10, pady=10)

    weekly_button = tk.Button(frame, text="Weekly", width=20, height=3, bg="#EB5E28", fg="black", font=button_font,
                              command=view_traffic_weekly_history)
    weekly_button.pack(side="left", padx=10, pady=10)

    # Create a monthly button
    monthly_button = tk.Button(frame, text="Monthly", width=20, height=3, bg="#EB5E28", fg="black", font=button_font,
                               command=view_traffic_monthly_history)
    monthly_button.pack(side="left", padx=10, pady=10)


def view_traffic_weekly_history():
    # Create a new window to display traffic history
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'), foreground="#EB5E28")
    style.configure("Treeview", font=('Helvetica', 9), rowheight=50, background="#232323", fieldbackground="#232323",
                    foreground="white")

    history_window = tk.Toplevel(app)
    history_window.title("Weekly Traffic History")

    # Set the position of the window (adjust the values as needed)
    window_x = 100  # X-coordinate of the window
    window_y = 100  # Y-coordinate of the window
    history_window.geometry(f"+{window_x}+{window_y}")

    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="1234",
        database="traffic_db"
    )
    mycursor = mydb.cursor()

    # Execute a SELECT query to fetch data from the traffic_history table
    mycursor.execute(
        "SELECT id, cam_location, start_date, end_date, date_time, weekly_congestion, total_congestion_time FROM traffic_history_weekly")
    data = mycursor.fetchall()

    # Create a treeview widget to display the data
    tree = ttk.Treeview(history_window, columns=(
    "ID", "Cam Location", "Start Date", "End Date", "Date/Time", "Weekly Congestion", "Total Congestion Time"),
                        show='headings')
    tree.heading("#1", text="ID")
    tree.heading("#2", text="Cam Location")
    tree.heading("#3", text="Start Date")
    tree.heading("#4", text="End Date")
    tree.heading("#5", text="Date/Time")
    tree.heading("#6", text="Weekly Congestion")
    tree.heading("#7", text="Total Congestion Time")

    tree.pack()

    # Adjust the width of columns based on content
    for col in (
    "ID", "Cam Location", "Start Date", "End Date", "Date/Time", "Weekly Congestion", "Total Congestion Time"):
        tree.column(col, width=200, anchor='center')

    # Insert data into the treeview
    for row in data:
        tree.insert("", "end", values=row)

    mydb.close()

    frame = tk.Frame(history_window)
    frame.pack(side="bottom")
    button_font = tkFont.Font(family='Helvetica', size=12, weight='bold')

    daily_button = tk.Button(frame, text="Daily", width=20, height=3, bg="#EB5E28", fg="black", font=button_font,
                             command=view_traffic_history)
    daily_button.pack(side="left", padx=10, pady=10)

    weekly_button = tk.Button(frame, text="Weekly", width=20, height=3, bg="#EB5E28", fg="black", font=button_font,
                              command=view_traffic_weekly_history)
    weekly_button.pack(side="left", padx=10, pady=10)

    # Create a monthly button
    monthly_button = tk.Button(frame, text="Monthly", width=20, height=3, bg="#EB5E28", fg="black", font=button_font,
                               command=view_traffic_monthly_history)
    monthly_button.pack(side="left", padx=10, pady=10)


def view_traffic_monthly_history():
    # Create a new window to display traffic history
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'), foreground="#EB5E28")
    style.configure("Treeview", font=('Helvetica', 9), rowheight=50, background="#232323", fieldbackground="#232323",
                    foreground="white")

    history_window = tk.Toplevel(app)
    history_window.title("Monthly Traffic History")

    # Set the position of the window (adjust the values as needed)
    window_x = 100  # X-coordinate of the window
    window_y = 100  # Y-coordinate of the window
    history_window.geometry(f"+{window_x}+{window_y}")

    # Connect to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="1234",
        database="traffic_db"
    )
    mycursor = mydb.cursor()

    # Execute a SELECT query to fetch data from the traffic_history table
    mycursor.execute(
        "SELECT id, cam_location, start_date, end_date, date_time, monthly_congestion, total_congestion_time FROM traffic_history_monthly")
    data = mycursor.fetchall()

    # Create a treeview widget to display the data
    tree = ttk.Treeview(history_window, columns=(
    "ID", "Cam Location", "Start Date", "End Date", "Date/Time", "Monthly Congestion", "Total Congestion Time"),
                        show='headings')
    tree.heading("#1", text="ID")
    tree.heading("#2", text="Cam Location")
    tree.heading("#3", text="Start Date")
    tree.heading("#4", text="End Date")
    tree.heading("#5", text="Date/Time")
    tree.heading("#6", text="Monthly Congestion")
    tree.heading("#7", text="Total Congestion Time")

    tree.pack()

    # Adjust the width of columns based on content
    for col in (
    "ID", "Cam Location", "Start Date", "End Date", "Date/Time", "Monthly Congestion", "Total Congestion Time"):
        tree.column(col, width=200, anchor='center')

    # Insert data into the treeview
    for row in data:
        tree.insert("", "end", values=row)

    mydb.close()

    frame = tk.Frame(history_window)
    frame.pack(side="bottom")
    button_font = tkFont.Font(family='Helvetica', size=12, weight='bold')

    daily_button = tk.Button(frame, text="Daily", width=20, height=3, bg="#EB5E28", fg="black", font=button_font,
                             command=view_traffic_history)
    daily_button.pack(side="left", padx=10, pady=10)

    weekly_button = tk.Button(frame, text="Weekly", width=20, height=3, bg="#EB5E28", fg="black", font=button_font,
                              command=view_traffic_weekly_history)
    weekly_button.pack(side="left", padx=10, pady=10)

    # Create a monthly button
    monthly_button = tk.Button(frame, text="Monthly", width=20, height=3, bg="#EB5E28", fg="black", font=button_font,
                               command=view_traffic_monthly_history)
    monthly_button.pack(side="left", padx=10, pady=10)


def Close():
    app.destroy()
    subprocess.call(["python", "testing.py"])
    # Close the current script


view_history_button = tk.Button(app, text="View Traffic History", command=view_traffic_history,
                                width=20, height=3, bg="#EB5E28", fg="black", font=stats_font)
view_history_button.grid(row=2, column=4, sticky="s", padx=10, pady=110)

close_button = tk.Button(app, text="Close", command=Close, width=20, height=3, bg="#FF0303", fg="black",
                         font=stats_font)
close_button.grid(row=2, column=4, sticky="s", padx=5, pady=0)

high_duration = 0
medium_duration = 0
low_duration = 0
free_duration = 0
current_status = None
start_time = None


def detect_objects():
    global high_duration, medium_duration, low_duration, current_status, free_duration, start_time
    statuscolor = ""
    start_time = None
    previous_status = ""
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        height, width, channels = frame.shape
        box_x, box_y, box_w, box_h = 0, 0, 1278, 720
        roi = frame[box_y:box_y + box_h, box_x:box_x + box_w]
        cv2.rectangle(frame, (box_x, box_y), (box_x + box_w, box_y + box_h), (statuscolor), 2)

        # Create a blob from the frame
        blob = cv2.dnn.blobFromImage(roi, scalefactor=0.00392, size=(416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        boxes = []
        confidences = []
        class_ids = []

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * box_w)
                    center_y = int(detection[1] * box_h)
                    w = int(detection[2] * box_w)
                    h = int(detection[3] * box_h)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        car_count = 0
        truck_count = 0
        bicycle_count = 0
        motorcycle_count = 0
        overall = 0
        status = ""
        current_time = time.time()

        for i in range(len(boxes)):
            if i in indexes:
                label = str(classes[class_ids[i]])
                confidence = confidences[i]

                if label == 'car':
                    car_count += 1
                    color = (0, 255, 0)
                    cv2.rectangle(roi, (boxes[i][0], boxes[i][1]),
                                  (boxes[i][0] + boxes[i][2], boxes[i][1] + boxes[i][3]),
                                  color, 2)
                    cv2.putText(roi, f'{label}: {confidence:.2f}', (boxes[i][0], boxes[i][1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                overall = car_count + truck_count + bicycle_count + motorcycle_count

                if label == 'truck':
                    truck_count += 1
                    color = (0, 0, 255)
                    cv2.rectangle(roi, (boxes[i][0], boxes[i][1]),
                                  (boxes[i][0] + boxes[i][2], boxes[i][1] + boxes[i][3]),
                                  color, 2)
                    cv2.putText(roi, f'{label}: {confidence:.2f}', (boxes[i][0], boxes[i][1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                overall = car_count + truck_count + bicycle_count + motorcycle_count

                if label == 'bicycle':
                    bicycle_count += 1
                    color = (0, 0, 255)
                    cv2.rectangle(roi, (boxes[i][0], boxes[i][1]),
                                  (boxes[i][0] + boxes[i][2], boxes[i][1] + boxes[i][3]),
                                  color, 2)
                    cv2.putText(roi, f'{label}: {confidence:.2f}', (boxes[i][0], boxes[i][1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                overall = car_count + truck_count + bicycle_count + motorcycle_count

                if label == 'motorbike':
                    motorcycle_count += 1
                    color = (0, 0, 255)
                    cv2.rectangle(roi, (boxes[i][0], boxes[i][1]),
                                  (boxes[i][0] + boxes[i][2], boxes[i][1] + boxes[i][3]),
                                  color, 2)
                    cv2.putText(roi, f'{label}: {confidence:.2f}', (boxes[i][0], boxes[i][1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                overall = car_count + truck_count + bicycle_count + motorcycle_count

                if overall >= 50:
                    status = "Heavy"
                    statuscolor = (0, 0, 255)

                elif overall >= 21:
                    status = "Moderate"
                    statuscolor = (255, 0, 0)

                elif overall >= 11:
                    status = "Light"
                    statuscolor = (0, 255, 0)

                else:
                    status = "Free Flow"
                    statuscolor = (255, 255, 255)

        if status != current_status:
            if start_time is None:
                start_time = current_time
            else:
                if current_status == "Heavy":
                    high_duration += current_time - start_time
                elif current_status == "Moderate":
                    medium_duration += current_time - start_time
                elif current_status == "Light":
                    low_duration += current_time - start_time

                elif current_status == "Free Flow":
                    free_duration += current_time - start_time

                start_time = current_time
                current_status = status

        duration = current_time - start_time

        car = f"Car Count: {car_count}"
        truck = f"Truck Count: {truck_count}"
        bicycle = f"Bicycle Count: {bicycle_count}"
        motorcycle = f"Motorcycle Count: {motorcycle_count}"
        traffic_overall = f"{overall}"
        traffic_status = f"{status}"

        vehicle_label.config(text=f"{car}\n{truck}\n{motorcycle}\n{bicycle}")
        stats_label.config(text=f"{traffic_overall}")
        congestion_label.config(text=f"{traffic_status}")
        duration_label.config(text=f"{duration:.2f}")


        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        frame_tk = ImageTk.PhotoImage(image=frame_pil)

        vid_widget.config(image=frame_tk)
        vid_widget.image = frame_tk

        previous_status = status


detect_thread = threading.Thread(target=detect_objects)
detect_thread.daemon = True
detect_thread.start()


def insert_daily_congestion(mydb, cam_location, current_time):
    global high_duration, medium_duration, low_duration, free_duration

    highest_duration = max(high_duration, medium_duration, low_duration, free_duration)
    congestion_values = {
        high_duration: "Heavy",
        medium_duration: "Moderate",
        low_duration: "Light",
        free_duration: "Free Flow"
    }
    highest_congestion = congestion_values[highest_duration]

    # Convert highest_duration_time to minutes
    highest_duration_minutes = int(highest_duration / 60)
    highest_duration_time_str = f"{highest_duration_minutes} minutes"

    # Database Query for daily congestion
    sql_daily = "INSERT INTO traffic_history (cam_location, date_time, daily_congestion, congestion_time) VALUES (%s, %s, %s, %s)"
    info_daily = (cam_location.cget("text"), current_time, highest_congestion, highest_duration_time_str)

    mycursor = mydb.cursor()
    mycursor.execute(sql_daily, info_daily)
    mydb.commit()

    high_duration = 0
    medium_duration = 0
    low_duration = 0
    free_duration = 0

    # Check if it's time for weekly analysis
    check_and_insert_weekly_data(mydb, cam_location)


def check_and_insert_weekly_data(mydb, cam_location):
    mycursor = mydb.cursor()

    # Modify the SQL query to select only unprocessed records
    sql_select_unprocessed_records = """
    SELECT id, daily_congestion, date_time, congestion_time, is_processed
    FROM traffic_history 
    WHERE cam_location = %s AND is_processed = FALSE
    ORDER BY id LIMIT 7
    """
    cam_location_text = cam_location.cget("text")

    while True:
        mycursor.execute(sql_select_unprocessed_records, (cam_location_text,))
        weekly_data = mycursor.fetchall()

        if not weekly_data or len(weekly_data) < 7:
            print("Not enough unprocessed data for another week.")
            break  # No more unprocessed data to process

        # Check if there is a complete week of unprocessed data
        if len(weekly_data) == 7:
            # Check if the data has already been processed
            if all(record[4] for record in weekly_data):
                print("Weekly data already processed. Skipping insertion.")
            else:
                # Count the occurrences of each congestion level and sum the congestion time
                congestion_count = {
                    "Heavy": 0,
                    "Moderate": 0,
                    "Light": 0,
                    "Free Flow": 0,
                }

                total_congestion_time = {
                    "Heavy": 0,
                    "Moderate": 0,
                    "Light": 0,
                    "Free Flow": 0,
                }

                for record in weekly_data:
                    daily_congestion, date_time, congestion_time_str = record[1], record[2], record[3]

                    # Ensure that the daily_congestion value is in the dictionary
                    if daily_congestion in congestion_count:
                        congestion_count[daily_congestion] += 1

                        # Check if congestion_time_str is not None before splitting
                        if congestion_time_str is not None:
                            # Assuming congestion_time_str is in the format "X minutes"
                            total_congestion_time[daily_congestion] += int(congestion_time_str.split(" ")[0])

                # Determine the most common congestion level for the specified time range
                most_common_congestion = max(congestion_count, key=congestion_count.get)

                # Database Query for weekly congestion
                sql_check_existing_data = """
                SELECT * FROM traffic_history_weekly 
                WHERE cam_location = %s AND start_date = %s AND end_date = %s
                """

                info_check_existing_data = (
                    cam_location_text,
                    weekly_data[0][2],  # Use the start date of the first record
                    (datetime.datetime.strptime(weekly_data[-1][2], "%I:%M%p : %m/%d/%y") + datetime.timedelta(
                        days=7)).strftime("%I:%M%p : %m/%d/%y"),  # Use the end date of the last record + 7 days
                )
                mycursor.execute(sql_check_existing_data, info_check_existing_data)
                existing_data = mycursor.fetchone()

                print("Start Date of Current Set:", weekly_data[0][2])
                print("Existing Data:", existing_data)

                if not existing_data:
                    # Weekly data doesn't exist, perform the insertion

                    # Database Query for weekly congestion
                    sql_weekly_insert = """
                    INSERT INTO traffic_history_weekly 
                    (cam_location, start_date, end_date, date_time, weekly_congestion, total_congestion_time) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    current_time = datetime.datetime.now().strftime("%I:%M%p : %m/%d/%y")
                    info_weekly_insert = (
                        cam_location_text,
                        weekly_data[0][2],  # Use the start date of the first record
                        weekly_data[-1][2],  # Use the end date of the last record
                        current_time,
                        most_common_congestion,
                        total_congestion_time[most_common_congestion],
                        # Use the total time for the most common congestion level
                    )

                    mycursor.execute(sql_weekly_insert, info_weekly_insert)
                    mydb.commit()
                    print("Weekly data inserted successfully.")

                    # Update the is_processed value after processing a record
                    for record in weekly_data:
                        record_ids = tuple(record[0] for record in weekly_data)
                        placeholders = ', '.join(
                            '%s' for _ in record_ids)  # Generate placeholders for the UPDATE statement
                        sql_update_is_processed = f"UPDATE traffic_history SET is_processed = TRUE WHERE id IN ({placeholders})"

                        mycursor.execute(sql_update_is_processed, record_ids)  # Execute the UPDATE statement
                        mydb.commit()

                else:
                    print("Weekly data already exists. Skipping insertion.")

        # Move to the next set of unprocessed 7 days
        mycursor.execute("""
            SELECT MIN(date_time) 
            FROM traffic_history 
            WHERE date_time > %s AND cam_location = %s AND is_processed = FALSE
        """, (weekly_data[-1][2], cam_location_text))
        next_set_start_date = mycursor.fetchone()[0]

        if next_set_start_date is not None:
            next_set_start_date = datetime.datetime.strptime(next_set_start_date,
                                                             "%I:%M%p : %m/%d/%y") + datetime.timedelta(days=1)

            mycursor.execute("""
                SELECT MAX(id) 
                FROM traffic_history 
                WHERE date_time = %s AND cam_location = %s AND is_processed = FALSE
            """, (next_set_start_date.strftime("%I:%M%p : %m/%d/%y"), cam_location_text))
            max_id = mycursor.fetchone()[0]

            if max_id is not None:
                # Update: Ensure we move to the next set of unprocessed 7 days
                mycursor.execute("""
                    UPDATE traffic_history 
                    SET is_processed = TRUE 
                    WHERE id <= %s AND cam_location = %s AND is_processed = FALSE
                """, (max_id, cam_location_text))
        else:
            print("Not enough unprocessed data for another week.")
            break  # No more unprocessed data to process

    # Close the cursor
    mycursor.close()

    check_and_insert_monthly_data(mydb, cam_location)


def check_and_insert_monthly_data(mydb, cam_location):
    mycursor = mydb.cursor()

    # Modify the SQL query to select only unprocessed records
    sql_select_unprocessed_records = """
        SELECT id, daily_congestion, date_time, congestion_time, is_processed_m
        FROM traffic_history 
        WHERE cam_location = %s AND is_processed_m = FALSE
        ORDER BY id LIMIT 30
        """
    cam_location_text = cam_location.cget("text")

    while True:
        mycursor.execute(sql_select_unprocessed_records, (cam_location_text,))
        monthly_data = mycursor.fetchall()

        if not monthly_data or len(monthly_data) < 30:
            print("Not enough unprocessed data for another month.")
            break  # No more unprocessed data to process

        # Check if there is a complete week of unprocessed data
        if len(monthly_data) == 30:
            # Check if the data has already been processed
            if all(record[4] for record in monthly_data):
                print("Monthly data already processed. Skipping insertion.")
            else:
                # Count the occurrences of each congestion level and sum the congestion time
                congestion_count = {
                    "Heavy": 0,
                    "Moderate": 0,
                    "Light": 0,
                    "Free Flow": 0,
                }

                total_congestion_time = {
                    "Heavy": 0,
                    "Moderate": 0,
                    "Light": 0,
                    "Free Flow": 0,
                }

                for record in monthly_data:
                    daily_congestion, date_time, congestion_time_str = record[1], record[2], record[3]

                    # Ensure that the daily_congestion value is in the dictionary
                    if daily_congestion in congestion_count:
                        congestion_count[daily_congestion] += 1

                        # Check if congestion_time_str is not None before splitting
                        if congestion_time_str is not None:
                            # Assuming congestion_time_str is in the format "X minutes"
                            total_congestion_time[daily_congestion] += int(congestion_time_str.split(" ")[0])

                # Determine the most common congestion level for the specified time range
                most_common_congestion = max(congestion_count, key=congestion_count.get)

                # Database Query for weekly congestion
                sql_check_existing_data = """
                    SELECT * FROM traffic_history_monthly
                    WHERE cam_location = %s AND start_date = %s AND end_date = %s
                    """

                info_check_existing_data = (
                    cam_location_text,
                    monthly_data[0][2],  # Use the start date of the first record
                    (datetime.datetime.strptime(monthly_data[-1][2], "%I:%M%p : %m/%d/%y") + datetime.timedelta(
                        days=30)).strftime("%I:%M%p : %m/%d/%y"),  # Use the end date of the last record + 30 days
                )
                mycursor.execute(sql_check_existing_data, info_check_existing_data)
                existing_data = mycursor.fetchone()

                print("Start Date of Current Set:", monthly_data[0][2])
                print("Existing Data:", existing_data)

                if not existing_data:
                    # Weekly data doesn't exist, perform the insertion

                    # Database Query for weekly congestion
                    sql_monthly_insert = """
                        INSERT INTO traffic_history_monthly
                        (cam_location, start_date, end_date, date_time, monthly_congestion, total_congestion_time) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """
                    current_time = datetime.datetime.now().strftime("%I:%M%p : %m/%d/%y")
                    info_monthly_insert = (
                        cam_location_text,
                        monthly_data[0][2],  # Use the start date of the first record
                        monthly_data[-1][2],  # Use the end date of the last record
                        current_time,
                        most_common_congestion,
                        total_congestion_time[most_common_congestion],
                        # Use the total time for the most common congestion level
                    )

                    mycursor.execute(sql_monthly_insert, info_monthly_insert)
                    mydb.commit()
                    print("Monthly data inserted successfully.")

                    # Update the is_processed value after processing a record
                    for record in monthly_data:
                        record_ids = tuple(record[0] for record in monthly_data)
                        placeholders = ', '.join(
                            '%s' for _ in record_ids)  # Generate placeholders for the UPDATE statement
                        sql_update_is_processed_m = f"UPDATE traffic_history SET is_processed_m = TRUE WHERE id IN ({placeholders})"

                        mycursor.execute(sql_update_is_processed_m, record_ids)  # Execute the UPDATE statement
                        mydb.commit()

                else:
                    print("Monthly data already exists. Skipping insertion.")

        # Move to the next set of unprocessed 7 days
        mycursor.execute("""
                SELECT MIN(date_time) 
                FROM traffic_history 
                WHERE date_time > %s AND cam_location = %s AND is_processed_m = FALSE
            """, (monthly_data[-1][2], cam_location_text))
        next_set_start_date = mycursor.fetchone()[0]

        if next_set_start_date is not None:
            next_set_start_date = datetime.datetime.strptime(next_set_start_date,
                                                             "%I:%M%p : %m/%d/%y") + datetime.timedelta(days=1)

            mycursor.execute("""
                    SELECT MAX(id) 
                    FROM traffic_history 
                    WHERE date_time = %s AND cam_location = %s AND is_processed_m = FALSE
                """, (next_set_start_date.strftime("%I:%M%p : %m/%d/%y"), cam_location_text))
            max_id = mycursor.fetchone()[0]

            if max_id is not None:
                # Update: Ensure we move to the next set of unprocessed 7 days
                mycursor.execute("""
                        UPDATE traffic_history 
                        SET is_processed_m = TRUE 
                        WHERE id <= %s AND cam_location = %s AND is_processed_m = FALSE
                    """, (max_id, cam_location_text))
        else:
            print("Not enough unprocessed data for another Month.")
            break  # No more unprocessed data to process

    # Close the cursor
    mycursor.close()


def execute_code():
    # Database Connection
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="1234",
        database="traffic_db",
    )

    current_time = datetime.datetime.now().strftime("%I:%M%p : %m/%d/%y")

    # Insert daily congestion data
    insert_daily_congestion(mydb, cam_location, current_time)

    # Check and insert weekly congestion data
    check_and_insert_weekly_data(mydb, cam_location)

    check_and_insert_monthly_data(mydb, cam_location)

    mydb.close()


def schedule_execution():
    now = datetime.datetime.now()
    desired_time = now.replace(hour=11, minute=15, second=0, microsecond=0)
    if now > desired_time:
        desired_time += datetime.timedelta(days=1)  # Set the time to the next day if it's already past 12:01 AM
    time_difference = (desired_time - now).total_seconds()
    app.after(int(time_difference * 1000), execute_code)


app.after(0, schedule_execution)
app.mainloop()

cap.release()
cv2.destroyAllWindows()


