import pywintypes
import win32gui
import win32api
import win32con
from thread_handler import ThreadHandler


class ProcessHandler:
    process_list = []
    target = None
    thread = None
    key_list = []

    def refresh_process_list(self):

        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title != "":
                    item = (hwnd, title, win32gui.GetClassName(hwnd))
                    self.process_list.append(item)

        self.process_list.clear()
        win32gui.EnumWindows(winEnumHandler, None)
        return self.process_list

    def set_target(self, index):
        self.target = self.process_list[index][0]

    def press_keys(self):
        for key in self.key_list.values():
            print("key pressed: {} {}".format(self.target, key["keycode"]))
            win32api.SendMessage(self.target, win32con.WM_KEYDOWN, key["keycode"], 0)
            win32api.SendMessage(self.target, win32con.WM_KEYUP, key["keycode"], 0)

    def start(self, key_list):
        print("starting")
        self.key_list = key_list
        self.thread = ThreadHandler(self.press_keys)
        self.thread.start()

# if __name__ == '__main__':
#     print(refresh_process_list())

