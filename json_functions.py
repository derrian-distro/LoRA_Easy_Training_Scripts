import json
import os
import time


def save_json(path, obj: dict) -> None:
    # set these to None and False to prevent them from modifying the output when loaded back up
    obj['list_of_json_to_run'] = None
    obj['save_json_only'] = False
    fp = open(os.path.join(path, f"config-{time.time()}.json"), "w")
    json.dump(obj, fp=fp, indent=4)
    fp.close()


def load_json(path, obj: dict) -> dict:
    with open(path) as f:
        json_obj = json.loads(f.read())
    print("loaded json, setting variables...")
    ui_name_scheme = {"pretrained_model_name_or_path": "base_model", "logging_dir": "log_dir",
                      "train_data_dir": "img_folder", "reg_data_dir": "reg_img_folder",
                      "output_dir": "output_folder", "max_resolution": "train_resolution",
                      "lr_scheduler": "scheduler", "lr_warmup": "warmup_lr_ratio",
                      "train_batch_size": "batch_size", "epoch": "num_epochs",
                      "save_at_n_epochs": "save_every_n_epochs", "num_cpu_threads_per_process": "num_workers",
                      "enable_bucket": "buckets", "save_model_as": "save_as", "shuffle_caption": "shuffle_captions",
                      "resume": "load_previous_save_state", "network_dim": "net_dim",
                      "gradient_accumulation_steps": "gradient_acc_steps", "output_name": "change_output_name",
                      "network_alpha": "alpha", "lr_scheduler_num_cycles": "cosine_restarts",
                      "lr_scheduler_power": "scheduler_power"}

    for key in list(json_obj):
        if key in ui_name_scheme:
            json_obj[ui_name_scheme[key]] = json_obj[key]
            if ui_name_scheme[key] in {"batch_size", "num_epochs"}:
                try:
                    json_obj[ui_name_scheme[key]] = int(json_obj[ui_name_scheme[key]])
                except ValueError:
                    print(f"attempting to load {key} from json failed as input isn't an integer")
                    quit(1)

    for key in list(json_obj):
        if obj["json_load_skip_list"] and key in obj["json_load_skip_list"]:
            continue
        if key in obj:
            if key in {"keep_tokens"}:
                json_obj[key] = int(json_obj[key]) if json_obj[key] is not None else None
            if key in {"learning_rate", "unet_lr", "text_encoder_lr", "warmup_lr_ratio"}:
                json_obj[key] = float(json_obj[key]) if json_obj[key] is not None else None
            if obj[key] != json_obj[key]:
                print_change(key, obj[key], json_obj[key])
                obj[key] = json_obj[key]
    print("completed changing variables.")
    return obj


def print_change(value, old, new):
    print(f"{value} changed from {old} to {new}")
