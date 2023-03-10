import os.path
import subprocess
import sys

import popup_modules
from tkinter import simpledialog


def main():
    args = [popup_modules.ask_file("Select base model to merge to", {"ckpt", "safetensors"}),
            popup_modules.ask_file("Select the LoCon or Loha model to merge with", {"safetensors", 'pt', 'ckpt'})]
    output_dir = popup_modules.ask_dir("Select the output folder")
    name = simpledialog.askstring(title="Output Name", prompt="What do you want to name the output model?")
    if not name:
        print("no name given, quitting...")
        quit(0)
    args.append(os.path.join(output_dir, f"{name}.safetensors"))
    if popup_modules.messagebox.askyesno("v2", "Are you merging to a SD2.x based model?"):
        args.append("--is_v2")
    if popup_modules.messagebox.askyesno("Device type", "Do you want to use GPU?"):
        args.append("--device=cuda")
    weight = simpledialog.askfloat("Merge Weight", "how much of the LoCon or Loha do you want to merge? "
                                                   "0-1, default is 1")
    if weight and 1 > weight > 0:
        args.append(f"--weight={weight}")
    button = popup_modules.ButtonBox("What save precision do you want? Cancel will save as fp16", ['float', 'fp16'])
    if button.current_value in {"", "fp16"}:
        args.append("--dtype=fp16")
    args.insert(0, sys.executable)
    args.insert(1, os.path.join(os.curdir, 'LyCORIS', 'tools', 'merge.py'))
    subprocess.check_call(args)


if __name__ == "__main__":
    main()
