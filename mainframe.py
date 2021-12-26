from tkinter import Frame, Button, Label, BOTTOM, DISABLED, NORMAL
from tkinter.ttk import Combobox


class MainFrame:
    hotkeys = {}
    strategies = {}

    def __init__(self, master):
        self.master = master
        self.frame = Frame(master, name="main")
        self.frame.pack()

        self.callbacks = {}
        self.set_strategies()
        self.register_hotkey(['hotkey_1', 'hotkey_2'])

        self.init_ui()
        self.register_event()

    def init_ui(self):
        frame = self.frame
        lbl = Label(frame, text="Process")
        cmb = Combobox(frame, width="25", name="process")

        lbl.grid(row=0, column=0)
        cmb.grid(row=0, column=1, columnspan=2)

        for i, hotkey in enumerate(self.hotkeys.items()):
            k, v = hotkey
            btn = Button(frame, text="", name=k, width=15)

            lbl = Label(frame, text=k)
            lbl.grid(row=i + 1, column=0)
            btn.grid(row=i + 1, column=1)

        btn_quit = Button(frame, text="QUIT", fg="red", command=frame.quit)

        btn_stop = Button(frame, text="STOP")

        btn_start = Button(frame, text="START", name="start")

        btn_quit.grid(row=3, column=2)
        btn_stop.grid(row=3, column=1)
        btn_start.grid(row=3, column=0)

    def set_strategies(self):
        self.strategies.update({"38": MainFrame.strategy_wheel})
        self.strategies.update({"2": MainFrame.strategy_key})

    def register_hotkey(self, hotkey_list):
        for hotkey_name in hotkey_list:
            d = {
                hotkey_name: {
                    "keytype": None,
                    "keycode": None,
                    "keyname": None,
                }
            }
            self.hotkeys.update(d)

    def register_event(self):
        cmb = self.frame.children["process"]
        cmb.bind("<Button-1>", self.refresh_process)
        cmb.bind("<<ComboboxSelected>>", self.get_selected_process)

        for k in self.hotkeys.keys():
            btn = self.frame.children[k]
            btn.config(command=lambda widget=btn: self.set_hotkey(widget))

        btn_start = self.frame.children["start"]
        btn_start.config(command=self.start)

    def append_callback(self, name, func):
        self.callbacks[name] = func

    def upgrade_hotkey(self, hotkey_name, keytype, keycode, keyname):
        hotkey_info = self.hotkeys.get(hotkey_name)
        if hotkey_info:
            hotkey_info['keytype'] = keytype
            hotkey_info['keycode'] = keycode
            hotkey_info['keyname'] = keyname

    def get_hotkeys(self):
        return self.hotkeys

    def refresh_process(self, event):
        cmb = event.widget
        cmb.selection_clear()
        cmb.config(values=self.callbacks.get("list_process")())

    def get_selected_process(self, event):
        self.callbacks.get("selected_process")(event.widget.current())

    def start(self):
        self.callbacks.get("start")(self.hotkeys)

    @staticmethod
    def strategy_wheel(event):
        if event.delta == 120:
            return "wheelup"
        elif event.delta == -120:
            return "wheeldown"

    @staticmethod
    def strategy_key(event):
        return event.keysym

    def set_disable(self, boolean=True):
        for child in self.frame.winfo_children():
            if boolean:
                child.configure(state=DISABLED)
            else:
                child.configure(state=NORMAL)

    def set_hotkey(self, btn):
        btn.configure(text="press a key", state=DISABLED, bg="yellow")
        self.set_disable()

        def change_hotkey(event):
            hotkey = self.strategies[event.type](event)
            self.upgrade_hotkey(str(btn).split(".")[-1], str(event.type), event.keycode, hotkey)
            btn.configure(state=NORMAL, text=str(hotkey), bg="grey")
            self.master.unbind("<Key>")
            self.master.unbind("<MouseWheel>")
            self.set_disable(False)

        self.master.bind("<Key>", change_hotkey)
        self.master.bind("<MouseWheel>", change_hotkey)
