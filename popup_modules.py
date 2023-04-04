import tkinter as tk
import os
from functools import partial
from tkinter import messagebox, ttk
from tkinter import filedialog
from tkinter import simpledialog


def ask_file(message, accepted_ext_list, file_path=None):
    messagebox.showinfo(message=message)
    res = ""
    initial_dir = ""
    initial_file = ""
    if file_path is not None:
        initial_dir = os.path.dirname(file_path) if os.path.exists(file_path) else ""
        initial_file = os.path.basename(file_path) if os.path.exists(file_path) else ""

    while res == "":
        res = filedialog.askopenfilename(title=message, initialdir=initial_dir, initialfile=initial_file)
        if res == "" or type(res) == tuple:
            ret = messagebox.askretrycancel(message="Do you want to to cancel training?")
            if not ret:
                exit()
            continue
        elif not os.path.exists(res):
            res = ""
            continue
        _, name = os.path.split(res)
        split_name = name.split(".")
        if split_name[-1] not in accepted_ext_list:
            res = ""
    return res


def ask_dir(message, dir_path=None):
    messagebox.showinfo(message=message)
    res = ""
    initial_dir = ""
    if dir_path is not None:
        initial_dir = dir_path if os.path.exists(dir_path) else ""
    while res == "":
        res = filedialog.askdirectory(title=message, initialdir=initial_dir)
        if res == "" or type(res) == tuple:
            ret = messagebox.askretrycancel(message="Do you want to to cancel training?")
            if not ret:
                exit()
            continue
        if not os.path.exists(res):
            res = ""
    return res


def ask_value(title, message, mode='int', repeat=True):
    cont = True
    while cont:
        if mode == 'int':
            ret = simpledialog.askinteger(title, message)
        elif mode == 'float':
            ret = simpledialog.askfloat(title, message)
        else:
            ret = simpledialog.askstring(title, message)
        if not ret and repeat:
            if messagebox.askyesno(message="Do you want to cancel?"):
                quit()
            continue
        return ret


class ButtonBox:
    def __init__(self, label: str, button_name_list: list[str]) -> None:
        self.window = tk.Tk()
        self.button_list = []
        self.current_value = ""

        self.window.attributes("-topmost", True)
        self.window.resizable(False, False)
        self.window.eval('tk::PlaceWindow . center')

        def del_window():
            self.window.quit()
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", del_window)
        tk.Label(text=label, master=self.window).pack()
        for button in button_name_list:
            self.button_list.append(ttk.Button(text=button, master=self.window,
                                               command=partial(self.set_current_value, button)))
            self.button_list[-1].pack()
        self.window.mainloop()

    def set_current_value(self, value):
        self.current_value = value
        self.window.quit()
        self.window.destroy()


class SliderBox:
    def __init__(self, label: str, slider_name_list: list[str], cancel_message: str) -> None:
        self.window = tk.Tk()
        self.slider_list: list[tk.Frame] = []
        self.slider_values: list[tk.DoubleVar] = []
        self.slider_labels: list[ttk.Label] = []
        self.not_selected: bool = False

        self.window.attributes("-topmost", True)
        self.window.resizable(False, False)
        self.window.eval("tk::PlaceWindow . center")

        def del_window():
            ret = messagebox.askyesno(message=cancel_message)
            if ret:
                self.not_selected = True
                self.window.quit()
                self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", del_window)
        tk.Label(text=label, master=self.window, pady=10).pack()
        for index, slider in enumerate(slider_name_list):
            self.slider_values.append(tk.DoubleVar(value=0.0, name=f"{index}"))
            self.slider_values[-1].trace_add("write", self.update_values)
            self.slider_list.append(tk.Frame(self.window))
            self.slider_list[-1].pack()
            ttk.Label(master=self.slider_list[-1], text=slider, width=30, anchor=tk.CENTER).grid(row=0, column=0)
            ttk.Scale(master=self.slider_list[-1], from_=0, to=1,
                      variable=self.slider_values[-1]).grid(row=1, column=0, padx=10)
            self.slider_labels.append(ttk.Label(master=self.slider_list[-1], text="0.00"))
            self.slider_labels[-1].grid(row=1, column=1)
        ttk.Button(master=self.window, text="Complete Selection", command=self.close_window).pack()
        self.window.mainloop()

    def close_window(self):
        self.window.quit()
        self.window.destroy()

    def get_values(self):
        return [str(s.get()) for s in self.slider_values]

    def update_values(self, *in_vals):
        pos = int(in_vals[0])
        trunc_value = '{value:.2f}'.format(value=self.slider_values[pos].get())
        self.slider_values[pos].set(float(trunc_value))
        self.slider_labels[pos]['text'] = trunc_value


class RadioBox:
    def __init__(self, label: str, button_name_list: list[str], cancel_message: str):
        self.window = tk.Tk()
        self.button_list: list[ttk.Radiobutton] = []
        self.current_value = tk.StringVar()

        self.window.attributes("-topmost", True)
        self.window.resizable(False, False)
        self.window.eval('tk::PlaceWindow . center')

        def close_with_cancel():
            ret = messagebox.askyesno(message=cancel_message)
            if ret:
                self.current_value.set("")
                self.window.quit()
                self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", close_with_cancel)
        tk.Label(text=label, master=self.window).pack()
        for button in button_name_list:
            self.button_list.append(ttk.Radiobutton(text=button, master=self.window,
                                                    value=button, variable=self.current_value))
            self.button_list[-1].pack()
        button = ttk.Button(text="Complete selection", master=self.window, command=self.del_window)
        button.pack()
        self.window.mainloop()

    def del_window(self):
        self.window.quit()
        self.window.destroy()

    def get_value(self):
        return self.current_value.get()


class CheckBox:
    def __init__(self, label: str, button_name_list: list[str], cancel_message: str):
        self.window: tk.Tk = tk.Tk()
        self.button_list: list[ttk.Checkbutton] = []
        self.selected_values: list[tk.StringVar] = []
        self.no_select = False

        self.window.attributes("-topmost", True)
        self.window.resizable(False, False)
        self.window.eval('tk::PlaceWindow . center')

        def del_window():
            ret = messagebox.askyesno(message=cancel_message)
            if ret:
                self.no_select = True
                self.window.quit()
                self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", del_window)
        tk.Label(text=label, master=self.window).pack()
        for button in button_name_list:
            self.selected_values.append(tk.StringVar())
            self.selected_values[-1].set("")
            self.button_list.append(ttk.Checkbutton(text=button, master=self.window, onvalue=button,
                                                    offvalue="", variable=self.selected_values[-1]))
            self.button_list[-1].pack()
        self.complete_button = ttk.Button(text="Complete selection", master=self.window, command=self.close_window)
        self.complete_button.pack()
        self.window.mainloop()

    def close_window(self):
        self.window.quit()
        self.window.destroy()

    def get_values(self):
        return [s.get() for s in self.selected_values if s.get() != ""]

