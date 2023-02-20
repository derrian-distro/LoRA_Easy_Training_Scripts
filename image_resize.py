import argparse
import tkinter as tk
from functools import partial
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import filedialog as fd
import tools.resize_images_to_resolution as resize
import os


def main():
    parser = argparse.ArgumentParser(
        description='Resize images in a folder to a specified max resolution(s) / '
                    '指定されたフォルダ内の画像を指定した最大画像サイズ（面積）以下にアスペクト比を維持したままリサイズします')
    parser.add_argument('src_img_folder', type=str, help='Source folder containing the images / 元画像のフォルダ')
    parser.add_argument('dst_img_folder', type=str,
                        help='Destination folder to save the resized images / リサイズ後の画像を保存するフォルダ')
    parser.add_argument('--max_resolution', type=str,
                        help='Maximum resolution(s) in the format "512x512,384x384, etc, etc" / 最大画像サイズをカンマ区切りで指定 ("512x512,384x384, etc, etc" など)',
                        default="512x512,384x384,256x256,128x128")
    parser.add_argument('--divisible_by', type=int,
                        help='Ensure new dimensions are divisible by this value / リサイズ後の画像のサイズをこの値で割り切れるようにします',
                        default=1)
    parser.add_argument('--interpolation', type=str, choices=['area', 'cubic', 'lanczos4'],
                        default='area', help='Interpolation method for resizing / リサイズ時の補完方法')
    parser.add_argument('--save_as_png', action='store_true', help='Save as png format / png形式で保存')
    parser.add_argument('--copy_associated_files', action='store_true',
                        help='Copy files with same base name to images (captions etc) / 画像と同じファイル名（拡張子を除く）のファイルもコピーする')

    args = ["--save_as_png", "--copy_associated_files", "--divisible_by=64"]
    args.insert(0, ask_path("Select your source image folder"))
    args.insert(1, ask_path("select your output image folder"))
    check = CheckBox("Select the sizes you want to resize to", ["832x832", "768x768", "512x512", "384x384",
                                                                "256x256", "128x128"],
                     "Closing this window will set the values to the defaults of: "
                     "512x512,384x384,256x256,128x128\nDo you want to cancel?")
    sizes: list[str] = []
    if not check.no_select:
        sizes += check.get_values()
    else:
        sizes += ["512x512", "384x384", "256x256", "128x128"]
    rad = RadioBox("Select which Interpolation method you want to use ot resize the images",
                   ["area", "cubic", "lanczos4"], "Closing this window will set the value to the default of lanczos4\n"
                                                  "Do you want to cancel?")
    if rad.get_value() == "":
        args.append(f"--interpolation=lanczos4")
    else:
        args.append(f"--interpolation={rad.get_value()}")
    args = parser.parse_args(args)
    for size in sizes:
        if not os.path.exists(os.path.join(args.dst_img_folder, size)):
            os.makedirs(os.path.join(args.dst_img_folder, size))
        resize.resize_images(args.src_img_folder, os.path.join(args.dst_img_folder, size), size,
                             args.divisible_by, args.interpolation, args.save_as_png, args.copy_associated_files)


def ask_path(message: str, file_types=None):
    ret = ""
    while ret == "":
        mb.showinfo(message=message)
        if file_types:
            ret = fd.askopenfilename(filetypes=file_types)
        else:
            ret = fd.askdirectory()
        if not ret:
            ret = mb.askretrycancel(message="Do you want to cancel converting?")
            if not ret:
                exit()
            ret = ""
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
            ret = mb.askyesno(message=cancel_message)
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


class RadioBox:
    def __init__(self, label: str, button_name_list: list[str], cancel_message: str):
        self.window = tk.Tk()
        self.button_list: list[ttk.Radiobutton] = []
        self.current_value = tk.StringVar()

        self.window.attributes("-topmost", True)
        self.window.resizable(False, False)
        self.window.eval('tk::PlaceWindow . center')

        def close_with_cancel():
            ret = mb.askyesno(message=cancel_message)
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


if __name__ == "__main__":
    main()
