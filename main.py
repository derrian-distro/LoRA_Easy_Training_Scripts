import gc
import os
import subprocess
import sys

import pkg_resources
import torch

import popup_questions
from ArgsList import ArgStore
from Parser import Parser, ensure_path
import json_functions
import sd_scripts.train_network as train_network

try:
    import lion_pytorch
    import dadaptation
    import lycoris
except ModuleNotFoundError as error:
    required = {"lion-pytorch", "dadaptation", "lycoris_lora"}
    installed = {p.key for p in pkg_resources.working_set}
    missing = required - installed
    if missing:
        print("missing some requirements, installing...")
        python = sys.executable
        subprocess.check_call([python, "-m", "pip", "install", *missing], stdout=subprocess.DEVNULL)


def main() -> None:
    parser = Parser()
    pre_args = parser.parse_args()
    args = ArgStore.convert_args_to_dict()
    if pre_args.popup:
        selected = popup_questions.ask_starter_questions(args)
        if selected == 2:
            popup_questions.ask_all_questions(args)
    q = args['save_json_only']
    multi_path = pre_args.multi_run_path if pre_args.multi_run_path else args['multi_run_folder']
    if multi_path and ensure_path(multi_path, "multi_run_folder"):
        for file in os.listdir(multi_path):
            if os.path.isdir(file) or file.split(".")[-1] != "json":
                continue
            args = ArgStore.convert_args_to_dict()
            args['json_load_skip_list'] = None
            json_functions.load_json(os.path.join(multi_path, file), args)
            try:
                ensure_file_paths(args)
            except FileNotFoundError:
                print("failed to find one or more folders or paths, skipping.")
                continue
            if args['tag_occurrence_txt_file']:
                get_occurrence_of_tags(args)
            args = parser.create_args(ArgStore.change_dict_to_internal_names(args))
            train_network.train(args)
            gc.collect()
            torch.cuda.empty_cache()
            if not os.path.exists(os.path.join(multi_path, "complete")):
                os.makedirs(os.path.join(multi_path, "complete"))
            os.rename(os.path.join(multi_path, file), os.path.join(multi_path, "complete", file))
        print("completed all training")
        quit()

    json_path = pre_args.load_json_path if pre_args.load_json_path else args['load_json_path']
    if json_path and ensure_path(json_path, 'load_json_path', {"json"}):
        json_functions.load_json(json_path, args)

    ensure_file_paths(args)

    if args['tag_occurrence_txt_file']:
        get_occurrence_of_tags(args)

    json_path = pre_args.save_json_path if pre_args.save_json_path else args['save_json_folder']
    if json_path and ensure_path(json_path, 'save_json_folder'):
        json_functions.save_json(json_path, args)

    if q:
        quit(0)

    args = parser.create_args(ArgStore.change_dict_to_internal_names(args))
    # print(args)
    train_network.train(args)


def ensure_file_paths(args: dict) -> None:
    failed_to_find = False
    folders_to_check = ['img_folder', 'output_folder', 'save_json_folder', 'multi_run_folder',
                        'reg_img_folder', 'log_dir', 'tokenizer_cache_dir']
    for folder in folders_to_check:
        if folder in args and args[folder] is not None:
            if not ensure_path(args[folder], folder):
                failed_to_find = True

    if not ensure_path(args['base_model'], 'base_model', {"safetensors", "ckpt"}):
        failed_to_find = True
    if args['load_json_path'] is not None and not ensure_path(args['load_json_path'], 'load_json_path', {'json'}):
        failed_to_find = True
    if args['vae'] is not None and not ensure_path(args['vae'], 'vae', {'pt'}):
        failed_to_find = True
    if args['sample_prompts'] is not None and not ensure_path(args['sample_prompts'], 'sample_prompts', {"txt"}):
        failed_to_find = True
    if args['dataset_config'] is not None and not ensure_path(args['dataset_config'], 'dataset_config', {'toml'}):
        failed_to_find = True
    if failed_to_find:
        raise FileNotFoundError()


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
