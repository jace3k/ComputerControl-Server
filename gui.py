from _tkinter import TclError
from tkinter import Tk, Label, Button, Entry


class Gui:
    def __init__(self, master):
        self.master = master
        self.master.title("Podaj PIN")
        self.master.resizable(0, 0)
        self.master.geometry("300x100")
        self.master.bind('<Return>', self.set)

        def set_geometry(root):
            w = root.winfo_reqwidth()
            h = root.winfo_reqheight()
            ws = root.winfo_screenwidth()
            hs = root.winfo_screenheight()
            x = (ws / 2) - (w / 2)
            y = (hs / 2) - (h / 2)
            root.geometry('+%d+%d' % (x, y))

        set_geometry(self.master)

        self.number = 0

        self.entry = Entry(master)
        self.entry.focus_set()
        self.label = Label(master, text="Ustal pin do swojego komputera")
        self.button = Button(master, text="Start", command=self.set)

        self.label.pack()
        self.entry.pack()
        self.button.pack()

    def set(self, *_):
        self.master.quit()
        self.number = self.entry.get()


def get_pin():
    root = Tk()
    gui = Gui(root)
    root.mainloop()
    try:
        root.destroy()
        print('Pin: {} '.format(gui.number))
    except TclError:
        print('Do widzenia!')
    return gui.number
