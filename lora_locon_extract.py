import os.path
import sys
import subprocess
from tkinter import messagebox

import popup_modules


def main():
    args = {}
    dims = [[], []]
    args['device'] = 'cpu' if not messagebox.askyesno(message="Do you want to use your GPU?") else 'cuda'
    args['model_tuned'] = popup_modules.ask_file('Select the model to extract from', ['ckpt', 'safetensors'])
    args['model_org'] = popup_modules.ask_file('Select the model the tuned model was based on', ['ckpt', 'safetensors'])
    ret = messagebox.askyesno(message="Are you extracting from a SD2.x based model?")
    if ret:
        args['v2'] = True
    output_folder = popup_modules.ask_dir("Select your output folder")
    model_name = os.path.split(args['model_tuned'])[1].split('.')[0]
    output_name = popup_modules.ask_value("Output Name", "What do you want the output to be named?",
                                          mode='str', default=model_name)
    button = popup_modules.ButtonBox("Which save precision do you want? Default is fp16", ['Float', 'fp16', 'bf16'])
    args['save_precision'] = 'fp16' if button.current_value == '' else button.current_value
    ret = messagebox.askyesno(message="Do you want to do multiple resizes?")
    if ret:
        multi_run = True
        ret = messagebox.askyesno(message="Do you want to extract using a txt file?")
        if ret:
            from_file = True
            with open(popup_modules.ask_file("Select the txt file you want to use", ['txt'])) as f:
                for line in f.readlines():
                    vals = line.replace('\n', '').split(' ')
                    dims[0].append(vals[0])
                    if len(vals) > 1:
                        dims[1].append(vals[1])
            if 0 < len(dims[1]) != len(dims[0]):
                print("Inputs aren't equal, make sure to have the same number of both dims")
                quit()
        else:
            from_file = False
    else:
        multi_run = False
        from_file = False
    if not from_file and multi_run:
        lin = popup_modules.ask_value("Linear Dims", "Write down all of the linear dims you want to extract with. "
                                                     "seperate with a space", mode='str')
        dims[0] = lin.split(' ')
        not_equal = True
        conv = ''
        while not_equal:
            conv = popup_modules.ask_yes_no_to_value('Do you want to extract a LoCon?', 'LoCon Extract',
                                                     f"Write down all of the conv dims you want to use seperated by a "
                                                     f"space, equal to the amount of linear dims({len(lin)})",
                                                     mode='str', default=conv)
            if conv:
                dims[1] = conv.split(' ')
                if len(dims[0]) == len(dims[1]):
                    not_equal = False
    elif not from_file and not multi_run:
        dims[0].append(popup_modules.ask_value('Linear Dim', "What linear dim do you want to extract with?"))
        conv = popup_modules.ask_yes_no_to_value("Do you want to extract a LoCon?", "LoCon Extract",
                                                 'What conv dim do you want to extract with?')
        if conv:
            dims[1].append(conv)

    parsed_args = []
    for key, value in args.items():
        if not value:
            continue
        if isinstance(value, bool):
            parsed_args.append(f'--{key}')
        else:
            parsed_args.append(f"--{key}={value}")
    python = sys.executable
    for i in range(len(dims[0])):
        lin = dims[0][i]
        if len(dims[1]) > 0:
            conv = dims[1][i]
        else:
            conv = None
        name = f"{output_name}-{lin}" + ("" if not conv else f"-{conv}") + r".safetensors"
        output_path = os.path.join(output_folder, name)
        try:
            temp = [python, os.path.join('sd_scripts', 'networks', 'extract_lora_from_models.py'),
                    f'--save_to={output_path}', f'--dim={lin}']
            if conv:
                temp += [f"--conv_dim={conv}"]
            subprocess.check_call(temp + parsed_args)
        except subprocess.CalledProcessError:
            print("one or more of the inputs were incorrect, skipping...")


if __name__ == "__main__":
    main()
