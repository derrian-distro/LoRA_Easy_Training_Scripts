import argparse
import os.path
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

import popup_modules
import sd_scripts.networks.resize_lora as resize


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--save_precision", type=str, default=None,
                        choices=[None, "float", "fp16", "bf16"],
                        help="precision in saving, float if omitted / 保存時の精度、未指定時はfloat")
    parser.add_argument("--new_rank", type=int, default=4,
                        help="Specify rank of output LoRA / 出力するLoRAのrank (dim)")
    parser.add_argument("--save_to", type=str, default=None,
                        help="destination file name: ckpt or safetensors file / 保存先のファイル名、ckptまたはsafetensors")
    parser.add_argument("--model", type=str, default=None,
                        help="LoRA model to resize at to new rank: ckpt or "
                             "safetensors file / 読み込むLoRAモデル、ckptまたはsafetensors")
    parser.add_argument("--device", type=str, default=None,
                        help="device to use, cuda for GPU / 計算を行うデバイス、cuda でGPUを使う")
    parser.add_argument("--verbose", action="store_true",
                        help="Display verbose resizing information / rank変更時の詳細情報を出力する")
    parser.add_argument("--dynamic_method", type=str, default=None,
                        choices=[None, "sv_ratio", "sv_fro", "sv_cumulative"],
                        help="Specify dynamic resizing method, --new_rank is used as a hard limit for max rank")
    parser.add_argument("--dynamic_param", type=float, default=None,
                        help="Specify target for dynamic reduction")

    args_list = []
    cont = True
    while cont:
        args = ["--save_precision=fp16"]
        ret = messagebox.askyesno(message="Do you want to use your graphics card to resize? if you have a lower end"
                                          "card (4-6gb vram) then I suggest you select no.")
        if ret:
            args.append("--device=cuda")
        model = popup_modules.ask_file("Select your model to reduce", ["safetensors"])
        args.append(f"--model={model}")

        button = popup_modules.ButtonBox("Select how you want to resize the LoRA. Default is Fixed",
                                         ['Fixed', 'sv_ratio', 'sv_fro', 'sv_cumulative'])
        if button.current_value in {"", "Fixed"}:
            fixed = True
        else:
            args.append(f"--dynamic_method={button.current_value}")
            fixed = False

        if fixed:
            rank = None
            while not rank:
                rank = simpledialog.askinteger(title="New Dim Size",
                                               prompt="What dim do you want to reduce the model to.\n"
                                                      "keep in mind that you can only reduce using "
                                                      "this method")
                if not rank:
                    rank = messagebox.askretrycancel(message="Do you want to cancel converting?")
                    if not rank:
                        exit()
                    rank = None
                    continue
            args.append(f"--new_rank={rank}")
        else:
            ret = None
            while not ret:
                ret = simpledialog.askfloat(title="Dynamic Value", prompt="Set the value for the dynamic resizing.")
                if not ret:
                    ret = messagebox.askyesno(message="Do you want to cancel resizing?")
                    if not ret:
                        exit()
                    ret = None
                    continue
                args.append(f"--dynamic_param={ret}")
            ret = None
            while not ret:
                ret = simpledialog.askinteger(title="Max Dim Size", prompt="Select the max dim size for the resize")
                if not ret:
                    ret = messagebox.askyesno(message="Do you want to cancel resizing?")
                    if not ret:
                        exit()
                    ret = None
                    continue
                args.append(f"--new_rank={ret}")

        output_folder = popup_modules.ask_dir("What folder do you want your output to be in?")
        file_name = None
        while not file_name:
            file_name = simpledialog.askstring(title="output name", prompt="What would you like your output files "
                                                                           "to be named?")
            if not file_name:
                file_name = messagebox.askretrycancel(message="Do you want to cancel resizing?")
                if not file_name:
                    exit()
                file_name = None
                continue
        args.append(f"--save_to={os.path.join(output_folder, file_name + '.safetensors')}")
        ret = messagebox.askyesno(message="Do you want to print out extra information?")
        if ret:
            args.append("--verbose")
        args = parser.parse_args(args)
        args_list.append(args)
        ret = messagebox.askyesno(message="Do you want to queue another resizing?")
        if not ret:
            cont = False
    for args in args_list:
        resize.args = args
        resize.resize(args)


if __name__ == "__main__":
    main()
