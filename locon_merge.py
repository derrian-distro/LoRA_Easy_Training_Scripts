import os.path

import popup_modules
from tkinter import simpledialog
from locon.locon.utils import merge_locon
from locon.locon.kohya_model_utils import (
    load_models_from_stable_diffusion_checkpoint,
    save_stable_diffusion_checkpoint,
    load_file
)

import torch


def main():
    base_model = popup_modules.ask_file("Select base model to merge to", {'ckpt', 'safetensors'})
    locon_model = popup_modules.ask_file("Select the LoCon model to merge with", {'safetensors', 'pt', 'ckpt'})
    output_name = popup_modules.ask_dir("Select the output location for your merged model")
    name = simpledialog.askstring(title="Output Name", prompt="What do you want to name the output model?")
    if not name:
        print("no name given, quitting...")
        quit(0)
    output_name = os.path.join(output_name, f"{name}.safetensors")
    safetensor = locon_model.split(".")[-1] in {"safetensors"}
    weight = simpledialog.askfloat("Merge Weight", "what percent do you want to merge? 0-1, default is 1")
    if not weight:
        weight = 1.0
    v2 = popup_modules.messagebox.askyesno("V2", "Are you merging to a SD2.x based model?")
    device = 'cuda'
    d_type = torch.float16

    # print(base_model, locon_model, output_name, safetensor, weight, v2, device, d_type)

    base = load_models_from_stable_diffusion_checkpoint(v2, base_model)
    if safetensor:
        locon = load_file(locon_model)
    else:
        locon = torch.load(locon_model)

    merge_locon(
        base,
        locon,
        weight,
        device
    )

    save_stable_diffusion_checkpoint(
        v2, output_name,
        base[0], base[2],
        None, 0, 0, d_type,
        base[1]
    )


if __name__ == "__main__":
    main()
