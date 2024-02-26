from cx_Freeze import setup, Executable

setup(name="Object Detection Software",
      version="0.1",
      description="Thi Detect Objects made by Nero",
      excutables=[Executable("main.py")])