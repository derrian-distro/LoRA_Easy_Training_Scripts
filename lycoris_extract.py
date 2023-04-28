import os.path
import subprocess
import sys

from tkinter import simpledialog

import popup_modules


def main():
    # Static values are in order of base model, extract model, device, v2, safetensors,
    # mode, sparce_bias, sparcity, cp decomp
    # safetensors and sparce_bias will not be asked
    static_values = ['base', 'extract', 'cpu', False, True, 'fixed', False, 0.98, False]
    # contains three lists, one for normal dim, one for conv dim, and one for the filename
    variable_values = [[], [], []]

    static_values[2] = 'cpu' if popup_modules.messagebox.askyesno(message="Do you want to use your cpu?") else 'cuda'
    static_values[3] = True if popup_modules.messagebox.askyesno(message="Are you extracting from a SD2.x model?") else False
    button = popup_modules.ButtonBox("Select the extraction method, default is fixed",
                                     ['fixed', 'threshold', 'ratio', 'quantile'])
    static_values[5] = 'fixed' if button.current_value == '' else button.current_value
    static_values[7] = True if popup_modules.messagebox.askyesno(message="Do you want to enable cp decomposition?") else False
    static_values[1] = popup_modules.ask_file("Select the model to be extracted from", ['ckpt', 'safetensors'])
    static_values[0] = popup_modules.ask_file("Select the base model to compare to", ['ckpt', 'safetensors'])
    output_folder = popup_modules.ask_dir("Select the output folder")
    output_name = simpledialog.askstring("Output Name", "What name do you want your outputs to be named?")
    multi_run = popup_modules.messagebox.askyesno(message="Do you want to do multiple extractions on the same model?")
    if multi_run:
        if popup_modules.messagebox.askyesno(message="Do you want to provide a txt file that contains "
                                                     "a list of extractions to do?"):
            popup_modules.messagebox.showinfo(message="Make sure each line has only two numbers on it seperated by "
                                                      "a space. example in the examples folder.")
            txt_file = popup_modules.ask_file("Select the txt file you want to use", ['txt'])
            with open(txt_file, 'r') as f:
                for line in f.readlines():
                    values = line.split(' ')
                    values[1] = values[1].split('\n')[0]
                    variable_values[0].append(values[0])
                    variable_values[1].append(values[1])
                    file_name = os.path.join(output_folder, f'{output_name}-{static_values[5]}-{values[0]}-{values[1]}.safetensors')
                    variable_values[2].append(file_name)
        else:
            ret = popup_modules.ask_value("List of linear values", "Write any number of linear "
                                                                   "values seperated by a space", 'string')
            if not ret:
                return
            linear = ret.split(' ')
            ret = popup_modules.ask_value("List of conv values", f"Write an equal number of conv "
                                                                 f"values to linear values({len(linear)})", 'string')
            if not ret:
                return
            conv = ret.split(' ')
            if len(linear) != len(conv):
                print("linear and conv values do not match, quitting.")
                return
            for i in range(len(conv)):
                variable_values[0].append(linear[i])
                variable_values[1].append(conv[i])
                file_name = os.path.join(output_folder, f"{output_name}-{static_values[5]}-{linear[i]}-{conv[i]}.safetensors")
                variable_values[2].append(file_name)
    else:
        prompt = "Dim" if static_values[5] == 'fixed' else static_values[5]
        ask_type = 'int' if prompt == 'Dim' else 'float'
        linear = popup_modules.ask_value(f"Linear {prompt}",
                                         f"What linear {prompt.lower()} do you want to extract with?", ask_type)
        if not linear:
            return
        conv = popup_modules.ask_value(f"conv {prompt}", f"what conv {prompt.lower()} do you want to extract with?",
                                       ask_type)
        if not conv:
            return
        variable_values[0].append(linear)
        variable_values[1].append(conv)
        file_name = os.path.join(output_folder, f"{output_name}-{static_values[5]}-{linear}-{conv}.safetensors")
        variable_values[2].append(file_name)
    run_extract(static_values, variable_values)


def run_extract(statics, variables):
    python = sys.executable
    args = [f"--device={statics[2]}"]
    if statics[3]:
        args.append("--is_v2")
    if statics[4]:
        args.append("--safetensors")
    args.append(f"--mode={statics[5]}")
    if statics[6]:
        args.append("--use_sparse_bias")
        args.append(f"--sparsity={statics[7]}")
    if not statics[8]:
        args.append("--disable_cp")
    for i in range(len(variables[0])):
        linear = f"--linear_{'dim' if statics[5] == 'fixed' else statics[5]}={variables[0][i]}"
        conv = f"--conv_{'dim' if statics[5] == 'fixed' else statics[5]}={variables[1][i]}"
        try:
            subprocess.check_call([python, os.path.join(os.curdir, "LyCORIS", "tools", "extract_locon.py"),
                                   statics[0], statics[1], variables[2][i]] + args + [linear, conv])
        except:
            print("One or more of the inputs were incorrect, skipping")


if __name__ == "__main__":
    main()
