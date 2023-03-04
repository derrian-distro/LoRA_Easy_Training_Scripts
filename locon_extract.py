import os.path
from tkinter import simpledialog

import torch
from safetensors.torch import save_file

import popup_modules
from locon.locon.utils import extract_diff
from locon.locon.kohya_model_utils import load_models_from_stable_diffusion_checkpoint


def main():
    base_model = ""
    db_model = ""
    output_name = ""

    lora_rank = 80
    conv_rank = 48

    use_threshold = False
    use_threshold_conv = False
    linear_threshold = 0.07
    conv_threshold = 0.45

    ret = popup_modules.ask_file("Select the model you want to extract", ['ckpt', 'safetensors'])
    db_model = ret
    ret = popup_modules.ask_file("Select the base model you want to compare to", ['ckpt', 'safetensors'])
    base_model = ret

    ret = popup_modules.ask_dir("Select the output folder")
    name = simpledialog.askstring(title="Name", prompt='What is the name of the output model? Don\'t put an extension')
    output_name = os.path.join(ret, f'{name if name else "out"}.safetensors')

    button = popup_modules.ButtonBox("Do you want to select dims or use thresholds?\n"
                                     "Default is dims", ['dims', 'thresholds'])
    if button.current_value in {"", "dims"}:
        ret = simpledialog.askinteger(title="Dims", prompt="Select the dim size you want to save at\nDefault is 80")
        lora_rank = 80 if not ret else ret
        ret = simpledialog.askinteger(title="Dims", prompt="Select the Conv Dim size you want to save at\n"
                                                           "Default is 48")
        conv_rank = 48 if not ret else ret
    else:
        use_threshold = True
        use_threshold_conv = True
        ret = simpledialog.askfloat(title="Thresholds", prompt="Select the threshold for your normal lora layers\n"
                                                               "Default is 0.07")
        linear_threshold = 0.07 if not ret else ret
        ret = simpledialog.askfloat(title="Thresholds", prompt="Select the threshold for your conv lora layers\n"
                                                               "Default is 0.45")
        conv_threshold = 0.45 if not ret else ret
    base = load_models_from_stable_diffusion_checkpoint(False, base_model)
    db = load_models_from_stable_diffusion_checkpoint(False, db_model)
    state_dict = extract_diff(
        base, db,
        lora_rank, conv_rank,
        use_threshold,
        use_threshold_conv,
        linear_threshold,
        conv_threshold,
        "cuda"
    )
    save_file(state_dict, output_name)


if __name__ == "__main__":
    main()
