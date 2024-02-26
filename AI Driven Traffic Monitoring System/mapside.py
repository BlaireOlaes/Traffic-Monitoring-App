import tkinter as tk
from tkinter import Canvas, Button, Label
from PIL import Image, ImageTk
import subprocess

def toggle_fullscreen(event=None):
    state = root.attributes('-fullscreen')
    root.attributes('-fullscreen', not state)

def stop_program(event):
    root.quit()

class MapApp:
    print("Map Side")

    def __init__(self, root):
        self.root = root
        self.root.title("Map Application")
        self.root.geometry("1920x1080")
        self.root.attributes('-fullscreen', True)
        self.root.bind('<KeyPress-Escape>', toggle_fullscreen)
        self.root.bind('x', stop_program)
        self.map_image = Image.open("map/Map Tac.png")
        zoom_factor = 0.8
        new_size = (int(self.map_image.width * zoom_factor), int(self.map_image.height * zoom_factor))
        self.map_photo = self.resize_image(self.map_image, new_size)

        self.map_canvas = Canvas(root, width=1920, height=1080)
        self.map_canvas.pack()

        # Display map image on canvas
        self.map_canvas.create_image(0, 0, anchor=tk.NW, image=self.map_photo)

        # Create landmarks
        self.landmark1 = Canvas(root, width=10, height=10, bg="#00ECC2", highlightthickness=2, highlightbackground='black')
        self.landmark1_window = self.map_canvas.create_window(720, 257, anchor=tk.NW, window=self.landmark1)

        self.landmark2 = Canvas(root, width=10, height=10, bg="#00ECC2", highlightthickness=2, highlightbackground='black')
        self.landmark2_window = self.map_canvas.create_window(856, 815, anchor=tk.NW, window=self.landmark2)

        # names to landmarks
        self.landmark1_name = "Landmark1"
        self.landmark2_name = "Landmark2"

        # Add event handler for landmark click
        self.landmark1.bind("<Button-1>", lambda event, landmark=self.landmark1_name: self.landmark_clicked(event, landmark))
        self.landmark2.bind("<Button-1>", lambda event, landmark=self.landmark2_name: self.landmark_clicked(event, landmark))

        self.logout_button = Button(root, width=13, height=1, text="Logout", command=self.logout,background="#00ECC2",
                                    highlightthickness=1, highlightbackground='black',  font=("Helvetica", 13, 'bold'))
        self.logout_button_window = self.map_canvas.create_window(1370, 820, anchor=tk.NW, window=self.logout_button)

    def landmark_clicked(self, event, landmark_name):

        print(f"Clicked Landmark Name: {landmark_name}")


        if landmark_name == "Landmark1":
            self.execute_code_userside()
        elif landmark_name == "Landmark2":
            self.execute_code_adminside()

    def execute_code_userside(self):

        print("Executing code for userside...")
        subprocess.Popen(["python", "userside.py"])

    def execute_code_adminside(self):

        print("Executing code for userside2...")
        subprocess.Popen(["python", "userside2.py"])

    def logout(self):
        root.destroy()
        subprocess.call(["python", "main.py"])

    def resize_image(self, image, size):
        return ImageTk.PhotoImage(image.resize(size, Image.LANCZOS))


if __name__ == "__main__":
    root = tk.Tk()
    app = MapApp(root)
    root.mainloop()
