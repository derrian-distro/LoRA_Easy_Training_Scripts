import gc
import subprocess
import pkg_resources
import sys
import time
import os
import json

try:
    import lion_pytorch
except ModuleNotFoundError as error:
    required = {"lion-pytorch"}
    installed = {p.key for p in pkg_resources.working_set}
    missing = required - installed
    if missing:
        print("lion-pytorch is missing, installing...")
        python = sys.executable
        subprocess.check_call([python, "-m", "pip", "install", *missing], stdout=subprocess.DEVNULL)

import torch.cuda
from ArgsList import ArgStore
import sd_scripts.train_network as train_network
import sd_scripts.library.train_util as util
import argparse


def main():
    parser = argparse.ArgumentParser()
    setup_args(parser)
    pre_args = parser.parse_args()
    multi_path = ArgStore.convert_args_to_dict()['multi_run_folder']
    if multi_path or pre_args.multi_run_path:
        multi_path = multi_path if multi_path else pre_args.multi_run_path
        if multi_path and not ensure_path(multi_path, "multi_path"):
            raise FileNotFoundError("Failed to find the path to where every json file is")
        for file in os.listdir(multi_path):
            if os.path.isdir(file) or file.split(".")[-1] != "json":
                continue
            arg_dict = ArgStore.convert_args_to_dict()
            arg_dict["json_load_skip_list"] = None
            load_json(os.path.join(multi_path, file), arg_dict)
            args = create_arg_space(arg_dict)
            args = parser.parse_args(args)
            if arg_dict['tag_occurrence_txt_file']:
                get_occurrence_of_tags(arg_dict)
            train_network.train(args)
            gc.collect()
            torch.cuda.empty_cache()
            if not os.path.exists(os.path.join(multi_path, "complete")):
                os.makedirs(os.path.join(multi_path, "complete"))
            os.rename(os.path.join(multi_path, file), os.path.join(multi_path, "complete", file))
        quit(0)
    arg_dict = ArgStore.convert_args_to_dict()
    if (pre_args.load_json_path or arg_dict["load_json_path"]) and not arg_dict["save_json_only"]:
        load_json(pre_args.load_json_path if pre_args.load_json_path else arg_dict['load_json_path'], arg_dict)
    if pre_args.save_json_path or arg_dict["save_json_folder"]:
        save_json(pre_args.save_json_path if pre_args.save_json_path else arg_dict['save_json_folder'], arg_dict)
    args = create_arg_space(arg_dict)
    args = parser.parse_args(args)
    if arg_dict['tag_occurrence_txt_file']:
        get_occurrence_of_tags(arg_dict)
    if not arg_dict["save_json_only"]:
        train_network.train(args)


def find_max_steps(args: dict) -> int:
    total_steps = 0
    folders = os.listdir(args["img_folder"])
    for folder in folders:
        if not os.path.isdir(os.path.join(args["img_folder"], folder)):
            continue
        num_repeats = folder.split("_")
        if len(num_repeats) < 2:
            print(f"folder {folder} is not in the correct format. Format is x_name. skipping")
            continue
        try:
            num_repeats = int(num_repeats[0])
        except ValueError:
            print(f"folder {folder} is not in the correct format. Format is x_name. skipping")
            continue
        imgs = 0
        for file in os.listdir(os.path.join(args["img_folder"], folder)):
            if os.path.isdir(file):
                continue
            ext = file.split(".")
            if ext[-1].lower() in {"png", "bmp", "gif", "jpeg", "jpg", "webp"}:
                imgs += 1
        total_steps += (num_repeats * imgs)
    total_steps = int((total_steps / args["batch_size"]) * args["num_epochs"])
    return total_steps


def save_json(path, obj: dict) -> None:
    if not ensure_path(path, "save_json_path"):
        raise FileNotFoundError("Failed to find folder to put json into, make sure you have the correct path")
    # set these to None and False to prevent them from modifying the output when loaded back up
    obj['list_of_json_to_run'] = None
    obj['save_json_only'] = False
    fp = open(os.path.join(path, f"config-{time.time()}.json"), "w")
    json.dump(obj, fp=fp, indent=4)
    fp.close()


def load_json(path, obj: dict) -> dict:
    if not ensure_path(path, "load_json_path", {"json"}):
        raise FileNotFoundError("Failed to find base model, make sure you have the correct path")
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


def get_occurrence_of_tags(args):
    extension = args['caption_extension']
    img_folder = args['img_folder']
    output_folder = args['output_folder']
    occurrence_dict = {}
    print(img_folder)
    for folder in os.listdir(img_folder):
        print(folder)
        if not os.path.isdir(os.path.join(img_folder, folder)):
            continue
        for file in os.listdir(os.path.join(img_folder, folder)):
            if not os.path.isfile(os.path.join(img_folder, folder, file)):
                continue
            ext = os.path.splitext(file)[1]
            if ext != extension:
                continue
            get_tags_from_file(os.path.join(img_folder, folder, file), occurrence_dict)
    if not args['sort_tag_occurrence_alphabetically']:
        output_list = {k: v for k, v in sorted(occurrence_dict.items(), key=lambda item: item[1], reverse=True)}
    else:
        output_list = {k: v for k, v in sorted(occurrence_dict.items(), key=lambda item: item[0])}
    name = args['change_output_name'] if args['change_output_name'] else "last"
    with open(os.path.join(output_folder, f"{name}.txt"), "w") as f:
        f.write(f"Below is a list of keywords used during the training of {args['change_output_name']}:\n")
        for k, v in output_list.items():
            f.write(f"[{v}] {k}\n")
    print(f"Created a txt file named {name}.txt in the output folder")


def get_tags_from_file(file, occurrence_dict):
    f = open(file)
    temp = f.read().replace(", ", ",").split(",")
    f.close()
    for tag in temp:
        if tag in occurrence_dict:
            occurrence_dict[tag] += 1
        else:
            occurrence_dict[tag] = 1


if __name__ == "__main__":
    main()
