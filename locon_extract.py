import os.path
import subprocess
import sys
from tkinter import simpledialog

import popup_modules


def main():
    args = []
    safe = False

    args.append(f"--device="
                f"{'cpu' if popup_modules.messagebox.askyesno(message='Do you want to use your cpu?') else 'cuda'}")
    args.insert(0, f"{popup_modules.ask_file('Select the model you want to extract from', ['ckpt', 'safetensors'])}")
    args.insert(0, f"{popup_modules.ask_file('Select the base model you want to compare to', ['ckpt', 'safetensors'])}")

    ret = popup_modules.messagebox.askyesno(message="Are you extracting from a SD2.x model?")
    if ret:
        args.append(f"--is_v2")

    ret = popup_modules.messagebox.askyesno(message="Do you want to save as safetensors?")
    if ret:
        safe = True
        args.append("--safetensors")
    ret = popup_modules.ask_dir("Select the output folder")
    name = simpledialog.askstring(title="Name", prompt='What is the name of the output model? Don\'t put an extension')
    output_name = os.path.join(ret, f'{name if name else "out"}.{"safetensors" if safe else "pt"}')
    args.insert(2, f"{output_name}")

    button = popup_modules.ButtonBox("What mode do you want? Default is fixed",
                                     ['fixed', 'threshold', 'ratio', 'percentile'])
    if button.current_value in {"", 'fixed'}:
        mode = 'fixed'
        args.append("--mode=fixed")
    elif button.current_value in {"threshold"}:
        mode = 'threshold'
        args.append("--mode=threshold")
    elif button.current_value in {"ratio"}:
        mode = 'ratio'
        args.append("--mode=ratio")
    else:
        mode = 'percentile'
        args.append("--mode=percentile")

    if mode == 'fixed':
        ret = simpledialog.askinteger(title="LoRA Dim", prompt="What dim do you want? Default is 1")
        args.append(f"--linear_dim={ret if ret else 1}")
        ret = simpledialog.askinteger(title="LoCon Dim", prompt="What LoCon dim do you want? Default is 1")
        args.append(f"--conv_dim={ret if ret else 1}")
    elif mode == 'threshold':
        ret = simpledialog.askfloat(title="LoRA threshold",
                                    prompt="What threshold do you want for LoRA? Default is 0.07")
        args.append(f"--linear_threshold={ret if ret else 0.07}")
        ret = simpledialog.askfloat(title="LoCon threshold",
                                    prompt="What threshold do you want for LoCon? Default is 0.45")
        args.append(f"--conv_threshold={ret if ret else 0.45}")
    elif mode == 'ratio':
        ret = simpledialog.askfloat(title="LoRA ratio", prompt="What ratio do you want for LoRA? Default is 5")
        args.append(f"--linear_ratio={ret if ret else 5}")
        ret = simpledialog.askfloat(title="LoCon ratio", prompt="What ratio do you want for LoCon? Default is 5")
        args.append(f"--conv_ratio={ret if ret else 5}")
    else:
        ret = simpledialog.askfloat(title="LoRA percentile",
                                    prompt="What percentile do you want for LoRA? Default is 70")
        args.append(f"--linear_percentile={ret if ret else 70}")
        ret = simpledialog.askfloat(title="LoCon percentile",
                                    prompt="What percentile do you want for LoCon? Default is 70")
        args.append(f"--conv_percentile={ret if ret else 70}")
    python = sys.executable
    args.insert(0, python)
    args.insert(1, os.path.join(os.curdir, "locon", "extract_locon.py"))
    subprocess.check_call(args)


if __name__ == "__main__":
    main()
