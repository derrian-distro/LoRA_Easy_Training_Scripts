import subprocess
import os.path
import sys
from tkinter import simpledialog
from tkinter import messagebox

import popup_modules


def main():
    static_values = ['--save_precision=fp16', '--device=cpu', '--model=model', '--dynamic_method=mode',
                     '--save_to=output']
    variable_values = [[], [], []]
    ret = messagebox.askyesno(message="Do you want to use your graphics card to resize?")
    if ret:
        static_values[1] = '--device=cuda'
    ret = messagebox.askyesno(message="Do you want to print verbose output?")
    if ret:
        static_values.append('--verbose')
    button = popup_modules.ButtonBox("Select the save precision. default is fp16", ['float', 'fp16', 'bf16'])
    if button.current_value in {'float', "bf16"}:
        static_values[0] = f"--save_precision={button.current_value}"
    ret = popup_modules.ask_file("Select the model you want to resize", ['safetensors', 'pt', 'ckpt'])
    static_values[2] = f"--model={ret}"
    button = popup_modules.ButtonBox("Select how you want to resize the LoRA. Default is Fixed",
                                     ['Fixed', 'sv_ratio', 'sv_fro', 'sv_cumulative'])
    if button.current_value in {"", "Fixed"}:
        mode = "Fixed"
        static_values.pop(3)
        fixed = True
    else:
        mode = button.current_value
        static_values[3] = f"--dynamic_method={button.current_value}"
        fixed = False
    out_folder = popup_modules.ask_dir("Select the folder to output to")
    out_name = simpledialog.askstring(title="Output Name", prompt="What do you want outputs to be named?")

    multi_run = messagebox.askyesno(message="Do you want to resize multiple times?")
    if multi_run:
        ret = messagebox.askyesno(message="Do you want to provide a txt file that contains a list of resizes to do?")
        if ret:
            messagebox.showinfo(message="The text file must be in the format of either 'dynamic value max dim' or 'dim'"
                                        "\ndepending on if you want to do dynamic or fixed. one set per line."
                                        "\nExample txt file will be in the examples folder")
            file = popup_modules.ask_file("Select the txt file that contains the list.", ['txt'])
            with open(file) as f:
                for line in f.readlines():
                    values = line.split(' ')
                    if len(values) > 1:
                        values[1] = values[1].split('\n')[0]
                    else:
                        values[0] = values[0].split('\n')[0]
                    if fixed:
                        variable_values[0].append(f"--new_rank={values[0]}")
                        variable_values[2].append(f"--save_to={os.path.join(out_folder, f'{out_name}-{mode}-{values[0]}.safetensors')}")
                    if not fixed:
                        variable_values[0].append(f"--dynamic_param={values[0]}")
                        variable_values[1].append(f"--new_rank={values[1]}")
                        variable_values[2].append(f"--save_to={os.path.join(out_folder, f'{out_name}-{mode}-{values[0]}-{values[1]}.safetensors')}")
            if not fixed:
                run_resizes(static_values, variable_values[2], variable_values[1], variable_values[0])
            else:
                run_resizes(static_values, variable_values[2], variable_values[0])
            return

    if multi_run:
        if not fixed:
            dyn_param = simpledialog.askstring("List of Dynamic params", "Write down any number of dynamic params seperated by a space (usually a value between 0 and 1)")
            if dyn_param:
                dyn_param = dyn_param.split(" ")
                for param in dyn_param:
                    variable_values[0].append(f"--dynamic_param={param}")
            else:
                print("no params, quitting")
                quit()
            dyn_max = simpledialog.askstring("List of Max Ranks", f"Write down as many ({len(dyn_param)}) max rank values as you put in for dynamic params seperated by a space")
            if dyn_max:
                dyn_max = dyn_max.split(" ")
                if len(dyn_max) != len(dyn_param):
                    print("the params and maxes are not equal, quitting")
                    quit()
                for param in dyn_max:
                    variable_values[1].append(f"--new_rank={param}")
            for i in range(len(dyn_max)):
                variable_values[2].append(f"--save_to={os.path.join(out_folder, f'{out_name}-{mode}-{dyn_param[i]}-{dyn_max[i]}.safetensors')}")
        else:
            ranks = simpledialog.askstring("List of Ranks to resize", "Write down any number of ranks to resize to seperated by a space")
            if ranks:
                ranks = ranks.split(" ")
                for rank in ranks:
                    variable_values[0].append(f"--new_rank={rank}")
                    variable_values[2].append(f"--save_to={os.path.join(out_folder, f'{out_name}-{mode}-{rank}.safetensors')}")
        if not fixed:
            run_resizes(static_values, variable_values[2], variable_values[1], variable_values[0])
        else:
            run_resizes(static_values, variable_values[2], variable_values[0])
        return
    if not fixed:
        dyn_param = simpledialog.askfloat("Dynamic Param", "What value do you want to use for the dynamic param?")
        if dyn_param:
            variable_values[0].append(f"--dynamic_param={dyn_param}")
        else:
            print("No dynamic parameter given, quitting.")
            return
        dyn_max = simpledialog.askinteger("Max Dim", "What is the max dim size for the resize?")
        if dyn_max:
            variable_values[1].append(f"--new_rank={dyn_max}")
        else:
            print("no max parameter given, quitting.")
            return
        variable_values[2].append(
            f"--save_to={os.path.join(out_folder, f'{out_name}-{mode}-{dyn_param}-{dyn_max}.safetensors')}")
        run_resizes(static_values, variable_values[2], variable_values[1], variable_values[0])
        return
    rank = simpledialog.askinteger("New Dim", "What is the new dim size?")
    if rank:
        variable_values[0].append(f"--new_rank={rank}")
        variable_values[2].append(f"--save_to={os.path.join(out_folder, f'{out_name}-{mode}-{rank}.safetensors')}")
        run_resizes(static_values, variable_values[2], variable_values[0])
    else:
        print("New rank not given, quitting.")
        return


def run_resizes(static_values, output, fixed_dim, dynamic_value=None):
    python = sys.executable
    for i in range(len(fixed_dim)):
        if dynamic_value:
            args = static_values + [fixed_dim[i], dynamic_value[i], output[i]]
        else:
            args = static_values + [fixed_dim[i], output[i]]
        try:
            subprocess.check_call([python, os.path.join("sd_scripts", "networks", "resize_lora.py")] + args)
        except:
            print("One or more of the inputs were incorrect, skipping")


if __name__ == "__main__":
    main()
