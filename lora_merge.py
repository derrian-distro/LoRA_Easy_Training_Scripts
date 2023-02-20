import pkg_resources
import subprocess
import sys
import argparse
import os
from functools import partial
from tkinter import messagebox as mb, \
    filedialog as fd, \
    simpledialog as sd, ttk
import tkinter as tk
try:
    import lora
except ModuleNotFoundError as error:
    required = {"lora"}
    installed = {p.key for p in pkg_resources.working_set}
    missing = required - installed
    if missing:
        print("Failed to find lora, installing...")
        python = sys.executable
        subprocess.check_call([python, "-m", "pip", "install", *missing], stdout=subprocess.DEVNULL)
import networks.svd_merge_lora as merge


def main():
    args = ["--save_precision=fp16"]
    button = ButtonBox("Which mode do you want to run in?", ["cpu", "gpu"])
    if button.current_value != "":
        args.append("--device=cuda")

    button = ButtonBox("Select the precision you want to merge at.\nfloat is recommended\ncancel will default to float",
                       ["float", "fp16", "bf16"])
    args.append("--precision=" + button.current_value if button.current_value else "float")

    models = []
    cont = True
    while cont:
        ret = ask_path("Select a LoRA to merge with", [("safetensors", ".safetensors"), ("ckpt", ".ckpt")])
        models.append(ret)
        ret = mb.askyesno(message="Do you want to add another model?")
        if not ret:
            cont = False
    print(models)
    args.append("--models")
    args += models

    slider = SliderBox("Use the sliders below to set the percentage that will be merged from each model.\n",
                       [os.path.split(s)[-1] for s in models], "Closing this window will set every value to 0.5\n"
                                                               "Do you want to cancel?")
    if slider.not_selected:
        args.append(f"--ratios")
        args += ['0.5' for _ in range(0, len(models))]
    else:
        args.append(f"--ratios")
        args += slider.get_values()

    ret = sd.askinteger(title="New Dim", prompt="What dim do you want the resulting merge to be in?\n"
                                                "Cancel will default to 8")
    args.append(f"--new_rank={ret if ret else 8}")

    ret = ask_path("Select the output folder")
    cont = True
    while cont:
        name = sd.askstring(title="Output Name", prompt="What do you want to name the merged model? "
                                                        "Do not include an extension")
        if not name:
            rt = mb.askretrycancel(message="Are you sure you want to quit merging?")
            if rt:
                quit()
        else:
            args.append(f"--save_to={os.path.join(ret, name)}.safetensors")
            cont = False
    merge.args = parser.parse_args(args)
    merge.merge(merge.args)


def ask_path(message: str, file_types=None):
    ret = ""
    while ret == "":
        mb.showinfo(message=message)
        if file_types:
            ret = fd.askopenfilename(filetypes=file_types)
        else:
            ret = fd.askdirectory()
        if not ret:
            ret = mb.askyesno(message="Do you want to cancel merging?")
            if ret:
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
            ret = mb.askyesno(message=cancel_message)
            if ret:
                self.not_selected = True
                self.window.quit()
                self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", del_window)
        tk.Label(text=label, master=self.window, pady=10).pack()
        for index, slider in enumerate(slider_name_list):
            self.slider_values.append(tk.DoubleVar(value=0.0, name=f"{index}"))
            self.slider_values[-1].trace_add("write", self.test_print)
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

    def test_print(self, *in_vals):
        pos = int(in_vals[0])
        trunc_value = '{value:.2f}'.format(value=self.slider_values[pos].get())
        self.slider_values[pos].set(float(trunc_value))
        self.slider_labels[pos]['text'] = trunc_value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # button box needed
    parser.add_argument("--save_precision", type=str, default=None,
                        choices=[None, "float", "fp16", "bf16"],
                        help="precision in saving, same to merging if omitted / "
                             "保存時に精度を変更して保存する、省略時はマージ時の精度と同じ")
    # always set to float
    parser.add_argument("--precision", type=str, default="float",
                        choices=["float", "fp16", "bf16"],
                        help="precision in merging (float is recommended) / "
                             "マージの計算時の精度（floatを推奨）")
    # file dialog to output folder followed by simpledialog.string for name
    parser.add_argument("--save_to", type=str, default=None,
                        help="destination file name: ckpt or safetensors file / "
                             "保存先のファイル名、ckptまたはsafetensors")
    # any number of file dialogs for the models
    parser.add_argument("--models", type=str, nargs='*',
                        help="LoRA models to merge: ckpt or safetensors file / "
                             "マージするLoRAモデル、ckptまたはsafetensors")
    # slider box needed
    parser.add_argument("--ratios", type=float, nargs='*',
                        help="ratios for each model / それぞれのLoRAモデルの比率")
    # simpledialog.int
    parser.add_argument("--new_rank", type=int, default=4,
                        help="Specify rank of output LoRA / 出力するLoRAのrank (dim)")
    # yesno for cuda
    parser.add_argument("--device", type=str, default=None, help="device to use, cuda for GPU / "
                                                                 "計算を行うデバイス、cuda でGPUを使う")
    main()
