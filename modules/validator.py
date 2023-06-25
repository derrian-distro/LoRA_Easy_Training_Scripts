import os
from typing import Union


def separate_and_validate(args: dict) -> tuple[Union[dict, None], Union[dict, None]]:
    new_args = {}
    new_dataset_args = {}
    for section, sec_args in args.items():
        if not sec_args:
            continue
        if section == "subsets":
            new_dataset_args[section] = sec_args
        if 'args' in sec_args:
            new_args[section] = sec_args['args']
        if 'dataset_args' in sec_args:
            new_dataset_args[section] = sec_args['dataset_args']
    valid = validate_args(new_args)
    valid_dataset = validate_dataset_args(new_dataset_args)
    return valid, valid_dataset


def validate_args(args: dict) -> Union[dict, None]:
    print("starting validation of args...")
    file_inputs = ["pretrained_model_name_or_path", "output_dir"]

    # if one or more sections report a None, then at least one thing isn't filled out correctly
    new_args = {}
    for key, value in args.items():
        if not value:
            return None
        if key == "sample_args":
            if "sample_prompts" not in value or not os.path.exists(value['sample_prompts']):
                return None
        if key == 'logging_args':
            if 'logging_dir' not in value or not os.path.exists(value['logging_dir']):
                return None
        for arg, val in value.items():
            if arg == "network_args":
                vals = []
                for k, v in val.items():
                    if k == "algo":
                        new_args['network_module'] = "lycoris.kohya"
                    if k == 'unit':
                        new_args['network_module'] = 'networks.dylora'
                    if k in ['down_lr_weight', 'up_lr_weight', 'block_dims',
                             'block_alphas', 'conv_block_dims', 'conv_block_alphas']:
                        for i in range(len(v)):
                            v[i] = str(v[i])
                        vals.append(f"{k}={','.join(v)}")
                        continue
                    vals.append(f"{k}={v}")
                val = vals
            if arg == "optimizer_args":
                vals = []
                for k, v in val.items():
                    vals.append(f"{k}={v}")
                val = vals
            if arg == 'lr_scheduler_args':
                vals = []
                for k, v in val.items():
                    vals.append(f"{k}={v}")
                val = vals
            if not val:
                continue
            new_args[arg] = val
    for file in file_inputs:
        if file not in new_args or not os.path.exists(new_args[file]):
            return None
    if "network_module" not in new_args:
        new_args['network_module'] = "networks.lora"
    return new_args


def validate_dataset_args(args: dict) -> Union[dict, None]:
    print("starting validation of dataset_args...")
    new_args = {"general": {}, "subsets": []}
    for key, value in args.items():
        if not value:
            return None
        if key == "subsets":
            continue
        for arg, val in value.items():
            if not val:
                continue
            if arg == 'max_token_length' and val == 75:
                continue
            new_args['general'][arg] = val
    for item in args['subsets']:
        sub = validate_subset(item)
        if not sub:
            return None
        new_args['subsets'].append(sub)
    return new_args


def validate_subset(args: dict) -> Union[dict, None]:
    new_args = {}
    for key, value in args.items():
        if not value:
            continue
        new_args[key] = value
    if "image_dir" not in new_args or not os.path.exists(new_args['image_dir']):
        return None
    return new_args


def validate_restarts(args: dict, dataset: dict) -> None:
    if "lr_scheduler_num_cycles" not in args:
        return
    if 'lr_scheduler_type' not in args:
        return
    if 'max_train_steps' in args:
        steps = args['max_train_steps']
    else:
        steps = calculate_steps(dataset['subsets'], args['max_train_epochs'], dataset['general']['batch_size'])
    steps = steps // args['lr_scheduler_num_cycles']
    args['lr_scheduler_args'].append(f"first_cycle_steps={steps}")


def validate_warmup_ratio(args: dict, dataset: dict) -> None:
    if "warmup_ratio" not in args:
        return
    if 'max_train_steps' in args:
        steps = args['max_train_steps']
    else:
        steps = calculate_steps(dataset['subsets'], args['max_train_epochs'], dataset['general']['batch_size'])
    steps = round(steps * args['warmup_ratio'])
    if "lr_scheduler_type" in args:
        args['lr_scheduler_args'].append(f"warmup_steps={steps // args.get('lr_scheduler_num_cycles', 1)}")
        del args['lr_scheduler_num_cycles']
    else:
        args['lr_warmup_steps'] = steps
    del args['warmup_ratio']


def validate_save_tags(args: dict, dataset: dict) -> None:
    if "tag_occurrence" not in args:
        return
    tags = {}
    for subset in dataset['subsets']:
        if not os.path.isdir(subset['image_dir']):
            continue
        for file in os.listdir(subset['image_dir']):
            if not os.path.isfile(os.path.join(subset['image_dir'], file)):
                continue
            if os.path.splitext(file)[1] != subset['caption_extension']:
                continue
            get_tags_from_file(os.path.join(subset['image_dir'], file), tags)
    output_list = {k: v for k, v in sorted(tags.items(), key=lambda item: item[1], reverse=True)}
    with open(os.path.join(args['output_dir'], f"{args['output_name']}_tags.txt"), "w") as f:
        f.write("Below is a list of keywords used during the training of this model:\n")
        for k, v in output_list.items():
            f.write(f"[{v}] {k}\n")
    del args['tag_occurrence']


def get_tags_from_file(file: str, tags: dict) -> None:
    with open(file, 'r') as f:
        temp = f.read().replace(", ", ",").split(",")
        for tag in temp:
            if tag in tags:
                tags[tag] += 1
            else:
                tags[tag] = 1


def calculate_steps(subsets: list, epochs: int, batch_size: int) -> int:
    steps = 0
    for subset in subsets:
        image_count = 0
        files = os.listdir(subset['image_dir'])
        for file in files:
            if file.split(".")[-1].lower() not in {"png", "bmp", "gif", "jpeg", "jpg", "webp"}:
                continue
            image_count += 1
        steps += (image_count * subset['num_repeats'])
    steps = (steps * epochs) // batch_size
    return steps
