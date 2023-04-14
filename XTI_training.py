import os.path
from tkinter import messagebox

import popup_modules
import popup_questions
import sys
import subprocess
import json_functions


def main():
    save = messagebox.askyesno(message="Do you want to save a json file of your configuration?")
    if not save:
        save_path = None
        load = messagebox.askyesno(message="Do you want to load a json file of your configuration?")
    else:
        save_path = popup_modules.ask_dir("Select where to save the json to")
        load = False
    if not load:
        args = popup_questions.ask_xti_questions()
        if save:
            json_functions.save_json(save_path, args)
    else:
        args = json_functions.load_xti_json(popup_modules.ask_file("Select the json file to load.", ['json']))
    parsed_args = []
    for key, value in args.items():
        if not value:
            continue
        if isinstance(value, bool):
            parsed_args.append(f'--{key}')
        else:
            parsed_args.append(f"--{key}={value}")
    python = sys.executable
    subprocess.check_call([python, os.path.join("sd_scripts", "train_textual_inversion_XTI.py")] + parsed_args)


if __name__ == "__main__":
    main()
