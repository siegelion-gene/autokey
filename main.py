from mainframe import MainFrame
from tkinter import Tk
from process_controller import ProcessHandler

root = Tk()
ph = ProcessHandler()
frame = MainFrame(root)
frame.append_callback("list_process", ph.refresh_process_list)
frame.append_callback("selected_process", ph.set_target)
frame.append_callback("start", ph.start)

root.geometry("300x300")
root.mainloop()