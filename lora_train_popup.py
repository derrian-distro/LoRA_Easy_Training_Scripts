import gc
import json
import time
from functools import partial
from typing import Union
import os
import tkinter as tk
from tkinter import filedialog as fd, ttk
from tkinter import simpledialog as sd
from tkinter import messagebox as mb

import torch.cuda
import train_network
import library.train_util as util
import argparse


class ArgStore:
    # Represents the entirety of all possible inputs for sd-scripts. they are ordered from most important to least
    def __init__(self):
        # Important, these are the most likely things you will modify
        self.base_model: str = r""  # example path, r"E:\sd\stable-diffusion-webui\models\Stable-diffusion\nai.ckpt"
        self.img_folder: str = r""  # is the folder path to your img folder, make sure to follow the guide here for folder setup: https://rentry.org/2chAI_LoRA_Dreambooth_guide_english#for-kohyas-script
        self.output_folder: str = r""  # just the folder all epochs/safetensors are output
        self.change_output_name: Union[str, None] = None  # changes the output name of the epochs
        self.save_json_folder: Union[str, None] = None  # OPTIONAL, saves a json folder of your config to whatever location you set here.
        self.load_json_path: Union[str, None] = None  # OPTIONAL, loads a json file partially changes the config to match. things like folder paths do not get modified.
        self.json_load_skip_list: Union[list[str], None] = ["save_json_folder", "reg_img_folder",
                                                            "lora_model_for_resume", "change_output_name",
                                                            "training_comment",
                                                            "json_load_skip_list"]  # OPTIONAL, allows the user to define what they skip when loading a json, by default it loads everything, including all paths, set it up like this ["base_model", "img_folder", "output_folder"]
        self.caption_dropout_rate: Union[float, None] = None  # The rate at which captions for files get dropped.
        self.caption_dropout_every_n_epochs: Union[int, None] = None  # Defines how often an epoch will completely ignore
        # captions, EX. 3 means it will ignore captions at epochs 3, 6, and 9
        self.caption_tag_dropout_rate: Union[float, None] = None  # Defines the rate at which a tag would be dropped, rather than the entire caption file

        self.net_dim: int = 128  # network dimension, 128 is the most common, however you might be able to get lesser to work
        self.alpha: float = 128  # represents the scalar for training. the lower the alpha, the less gets learned per step. if you want the older way of training, set this to dim
        # list of schedulers: linear, cosine, cosine_with_restarts, polynomial, constant, constant_with_warmup
        self.scheduler: str = "cosine_with_restarts"  # the scheduler for learning rate. Each does something specific
        self.cosine_restarts: Union[int, None] = 1  # OPTIONAL, represents the number of times it restarts. Only matters if you are using cosine_with_restarts
        self.scheduler_power: Union[float, None] = 1  # OPTIONAL, represents the power of the polynomial. Only matters if you are using polynomial
        self.warmup_lr_ratio: Union[float, None] = None  # OPTIONAL, Calculates the number of warmup steps based on the ratio given. Make sure to set this if you are using constant_with_warmup, None to ignore
        self.learning_rate: Union[float, None] = 1e-4  # OPTIONAL, when not set, lr gets set to 1e-3 as per adamW. Personally, I suggest actually setting this as lower lr seems to be a small bit better.
        self.text_encoder_lr: Union[float, None] = None  # OPTIONAL, Sets a specific lr for the text encoder, this overwrites the base lr I believe, None to ignore
        self.unet_lr: Union[float, None] = None  # OPTIONAL, Sets a specific lr for the unet, this overwrites the base lr I believe, None to ignore
        self.num_workers: int = 1  # The number of threads that are being used to load images, lower speeds up the start of epochs, but slows down the loading of data. The assumption here is that it increases the training time as you reduce this value
        self.persistent_workers: bool = True  # makes workers persistent, further reduces/eliminates the lag in between epochs. however it may increase memory usage

        self.batch_size: int = 1  # The number of images that get processed at one time, this is directly proportional to your vram and resolution. with 12gb of vram, at 512 reso, you can get a maximum of 6 batch size
        self.num_epochs: int = 1  # The number of epochs, if you set max steps this value is ignored as it doesn't calculate steps.
        self.save_at_n_epochs: Union[int, None] = None  # OPTIONAL, how often to save epochs, None to ignore
        self.shuffle_captions: bool = False  # OPTIONAL, False to ignore
        self.keep_tokens: Union[int, None] = None  # OPTIONAL, None to ignore
        self.max_steps: Union[int, None] = None  # OPTIONAL, if you have specific steps you want to hit, this allows you to set it directly. None to ignore
        self.tag_occurrence_txt_file: bool = False  # OPTIONAL, creates a txt file that has the entire occurrence of all tags in your dataset
        # the metadata will also have this so long as you have metadata on, so no reason to have this on by default
        # will automatically output to the same folder as your output checkpoints

        # These are the second most likely things you will modify
        self.train_resolution: int = 512
        self.min_bucket_resolution: int = 320
        self.max_bucket_resolution: int = 960
        self.lora_model_for_resume: Union[str, None] = None  # OPTIONAL, takes an input lora to continue training from, not exactly the way it *should* be, but it works, None to ignore
        self.save_state: bool = False  # OPTIONAL, is the intended way to save a training state to use for continuing training, False to ignore
        self.load_previous_save_state: Union[str, None] = None  # OPTIONAL, is the intended way to load a training state to use for continuing training, None to ignore
        self.training_comment: Union[str, None] = None  # OPTIONAL, great way to put in things like activation tokens right into the metadata. seems to not work at this point and time
        self.unet_only: bool = False  # OPTIONAL, set it to only train the unet
        self.text_only: bool = False  # OPTIONAL, set it to only train the text encoder

        # These are the least likely things you will modify
        self.reg_img_folder: Union[str, None] = None  # OPTIONAL, None to ignore
        self.clip_skip: int = 2  # If you are training on a model that is anime based, keep this at 2 as most models are designed for that
        self.test_seed: int = 23  # this is the "reproducable seed", basically if you set the seed to this, you should be able to input a prompt from one of your training images and get a close representation of it
        self.prior_loss_weight: float = 1  # is the loss weight much like Dreambooth, is required for LoRA training
        self.gradient_checkpointing: bool = False  # OPTIONAL, enables gradient checkpointing
        self.gradient_acc_steps: Union[int, None] = None  # OPTIONAL, not sure exactly what this means
        self.mixed_precision: str = "fp16"  # If you have the ability to use bf16, do it, it's better
        self.save_precision: str = "fp16"  # You can also save in bf16, but because it's not universally supported, I suggest you keep saving at fp16
        self.save_as: str = "safetensors"  # list is pt, ckpt, safetensors
        self.caption_extension: str = ".txt"  # the other option is .captions, but since wd1.4 tagger outputs as txt files, this is the default
        self.max_clip_token_length = 150  # can be 75, 150, or 225 I believe, there is no reason to go higher than 150 though
        self.buckets: bool = True
        self.xformers: bool = True
        self.use_8bit_adam: bool = True
        self.cache_latents: bool = True
        self.color_aug: bool = False  # IMPORTANT: Clashes with cache_latents, only have one of the two on!
        self.flip_aug: bool = False
        self.vae: Union[str, None] = None  # Seems to only make results worse when not using that specific vae, should probably not use
        self.no_meta: bool = False  # This removes the metadata that now gets saved into safetensors, (you should keep this on)
        self.log_dir: Union[str, None] = None  # output of logs, not useful to most people.
        self.v2: bool = False  # Sets up training for SD2.1
        self.v_parameterization: bool = False  # Only is used when v2 is also set and you are using the 768x version of v2

    # Creates the dict that is used for the rest of the code, to facilitate easier json saving and loading
    @staticmethod
    def convert_args_to_dict():
        return ArgStore().__dict__


def main():
    parser = argparse.ArgumentParser()
    setup_args(parser)
    pre_args = parser.parse_args()
    queues = 0
    args_queue = []
    cont = True
    while cont:
        arg_dict = ArgStore.convert_args_to_dict()
        ret = mb.askyesno(message="Do you want to load a json config file?")
        if ret:
            load_json(ask_file("select json to load from", {"json"}), arg_dict)
            arg_dict = ask_elements_trunc(arg_dict)
        else:
            arg_dict = ask_elements(arg_dict)
        if pre_args.save_json_path or arg_dict["save_json_folder"]:
            save_json(pre_args.save_json_path if pre_args.save_json_path else arg_dict['save_json_folder'], arg_dict)
        args = create_arg_space(arg_dict)
        args = parser.parse_args(args)
        queues += 1
        args_queue.append(args)
        if arg_dict['tag_occurrence_txt_file']:
            get_occurrence_of_tags(arg_dict)
        ret = mb.askyesno(message="Do you want to queue another training?")
        if not ret:
            cont = False
    for args in args_queue:
        try:
            train_network.train(args)
        except Exception as e:
            print(f"Failed to train this set of args.\nSkipping this training session.\nError is: {e}")
        gc.collect()
        torch.cuda.empty_cache()


def create_arg_space(args: dict) -> [str]:
    # This is the list of args that are to be used regardless of setup
    output = ["--network_module=networks.lora", f"--pretrained_model_name_or_path={args['base_model']}",
              f"--train_data_dir={args['img_folder']}", f"--output_dir={args['output_folder']}",
              f"--prior_loss_weight={args['prior_loss_weight']}", f"--caption_extension=" + args['caption_extension'],
              f"--resolution={args['train_resolution']}", f"--train_batch_size={args['batch_size']}",
              f"--mixed_precision={args['mixed_precision']}", f"--save_precision={args['save_precision']}",
              f"--network_dim={args['net_dim']}", f"--save_model_as={args['save_as']}",
              f"--clip_skip={args['clip_skip']}", f"--seed={args['test_seed']}",
              f"--max_token_length={args['max_clip_token_length']}", f"--lr_scheduler={args['scheduler']}",
              f"--network_alpha={args['alpha']}", f"--max_data_loader_n_workers={args['num_workers']}"]
    if not args['max_steps']:
        output.append(f"--max_train_epochs={args['num_epochs']}")
        output += create_optional_args(args, find_max_steps(args))
    else:
        output.append(f"--max_train_steps={args['max_steps']}")
        output += create_optional_args(args, args['max_steps'])
    return output


def create_optional_args(args: dict, steps):
    output = []
    if args["reg_img_folder"]:
        output.append(f"--reg_data_dir={args['reg_img_folder']}")

    if args['lora_model_for_resume']:
        output.append(f"--network_weights={args['lora_model_for_resume']}")

    if args['save_at_n_epochs']:
        output.append(f"--save_every_n_epochs={args['save_at_n_epochs']}")
    else:
        output.append("--save_every_n_epochs=999999")

    if args['shuffle_captions']:
        output.append("--shuffle_caption")

    if args['keep_tokens'] and args['keep_tokens'] > 0:
        output.append(f"--keep_tokens={args['keep_tokens']}")

    if args['buckets']:
        output.append("--enable_bucket")
        output.append(f"--min_bucket_reso={args['min_bucket_resolution']}")
        output.append(f"--max_bucket_reso={args['max_bucket_resolution']}")

    if args['use_8bit_adam']:
        output.append("--use_8bit_adam")

    if args['xformers']:
        output.append("--xformers")

    if args['color_aug']:
        if args['cache_latents']:
            print("color_aug and cache_latents conflict with one another. Please select only one")
            quit(1)
        output.append("--color_aug")

    if args['flip_aug']:
        output.append("--flip_aug")

    if args['cache_latents']:
        output.append("--cache_latents")

    if args['warmup_lr_ratio'] and args['warmup_lr_ratio'] > 0:
        warmup_steps = int(steps * args['warmup_lr_ratio'])
        output.append(f"--lr_warmup_steps={warmup_steps}")

    if args['gradient_checkpointing']:
        output.append("--gradient_checkpointing")

    if args['gradient_acc_steps'] and args['gradient_acc_steps'] > 0 and args['gradient_checkpointing']:
        output.append(f"--gradient_accumulation_steps={args['gradient_acc_steps']}")

    if args['learning_rate'] and args['learning_rate'] > 0:
        output.append(f"--learning_rate={args['learning_rate']}")

    if args['text_encoder_lr'] and args['text_encoder_lr'] > 0:
        output.append(f"--text_encoder_lr={args['text_encoder_lr']}")

    if args['unet_lr'] and args['unet_lr'] > 0:
        output.append(f"--unet_lr={args['unet_lr']}")

    if args['vae']:
        output.append(f"--vae={args['vae']}")

    if args['no_meta']:
        output.append("--no_metadata")

    if args['save_state']:
        output.append("--save_state")

    if args['load_previous_save_state']:
        output.append(f"--resume={args['load_previous_save_state']}")

    if args['change_output_name']:
        output.append(f"--output_name={args['change_output_name']}")

    if args['training_comment']:
        output.append(f"--training_comment={args['training_comment']}")

    if args['cosine_restarts'] and args['scheduler'] == "cosine_with_restarts":
        output.append(f"--lr_scheduler_num_cycles={args['cosine_restarts']}")

    if args['scheduler_power'] and args['scheduler'] == "polynomial":
        output.append(f"--lr_scheduler_power={args['scheduler_power']}")

    if args['persistent_workers']:
        output.append(f"--persistent_data_loader_workers")

    if args['unet_only']:
        output.append("--network_train_unet_only")

    if args['text_only'] and not args['unet_only']:
        output.append("--network_train_text_encoder_only")

    if args["log_dir"]:
        output.append(f"--logging_dir={args['log_dir']}")

    if args['caption_dropout_rate']:
        output.append(f"--caption_dropout_rate={args['caption_dropout_rate']}")

    if args['caption_dropout_every_n_epochs']:
        output.append(f"--caption_dropout_every_n_epochs={args['caption_dropout_every_n_epochs']}")

    if args['caption_tag_dropout_rate']:
        output.append(f"--caption_tag_dropout_rate={args['caption_tag_dropout_rate']}")

    if args['v2']:
        output.append("--v2")

    if args['v2'] and args['v_parameterization']:
        output.append("--v_parameterization")
    return output


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


def add_misc_args(parser):
    parser.add_argument("--save_json_path", type=str, default=None,
                        help="Path to save a configuration json file to")
    parser.add_argument("--load_json_path", type=str, default=None,
                        help="Path to a json file to configure things from")
    parser.add_argument("--no_metadata", action='store_true',
                        help="do not save metadata in output model / メタデータを出力先モデルに保存しない")
    parser.add_argument("--save_model_as", type=str, default="safetensors", choices=[None, "ckpt", "pt", "safetensors"],
                        help="format to save the model (default is .safetensors) / モデル保存時の形式（デフォルトはsafetensors）")

    parser.add_argument("--unet_lr", type=float, default=None, help="learning rate for U-Net / U-Netの学習率")
    parser.add_argument("--text_encoder_lr", type=float, default=None,
                        help="learning rate for Text Encoder / Text Encoderの学習率")
    parser.add_argument("--lr_scheduler_num_cycles", type=int, default=1,
                        help="Number of restarts for cosine scheduler with restarts / cosine with restartsスケジューラでのリスタート回数")
    parser.add_argument("--lr_scheduler_power", type=float, default=1,
                        help="Polynomial power for polynomial scheduler / polynomialスケジューラでのpolynomial power")

    parser.add_argument("--network_weights", type=str, default=None,
                        help="pretrained weights for network / 学習するネットワークの初期重み")
    parser.add_argument("--network_module", type=str, default=None,
                        help='network module to train / 学習対象のネットワークのモジュール')
    parser.add_argument("--network_dim", type=int, default=None,
                        help='network dimensions (depends on each network) / モジュールの次元数（ネットワークにより定義は異なります）')
    parser.add_argument("--network_alpha", type=float, default=1,
                        help='alpha for LoRA weight scaling, default 1 (same as network_dim for same behavior as old version) / LoRaの重み調整のalpha値、デフォルト1（旧バージョンと同じ動作をするにはnetwork_dimと同じ値を指定）')
    parser.add_argument("--network_args", type=str, default=None, nargs='*',
                        help='additional argmuments for network (key=value) / ネットワークへの追加の引数')
    parser.add_argument("--network_train_unet_only", action="store_true",
                        help="only training U-Net part / U-Net関連部分のみ学習する")
    parser.add_argument("--network_train_text_encoder_only", action="store_true",
                        help="only training Text Encoder part / Text Encoder関連部分のみ学習する")
    parser.add_argument("--training_comment", type=str, default=None,
                        help="arbitrary comment string stored in metadata / メタデータに記録する任意のコメント文字列")


def setup_args(parser):
    util.add_sd_models_arguments(parser)
    util.add_dataset_arguments(parser, True, True, True)
    util.add_training_arguments(parser, True)
    add_misc_args(parser)


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
    output_list = {k: v for k, v in sorted(occurrence_dict.items(), key=lambda item: item[1], reverse=True)}
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


def ask_file(message, accepted_ext_list, file_path=None):
    mb.showinfo(message=message)
    res = ""
    _initialdir = ""
    _initialfile = ""
    if file_path != None:
        _initialdir = os.path.dirname(file_path) if os.path.exists(file_path) else ""
        _initialfile = os.path.basename(file_path) if os.path.exists(file_path) else ""

    while res == "":
        res = fd.askopenfilename(title=message, initialdir=_initialdir, initialfile=_initialfile)
        if res == "":
            ret = mb.askretrycancel(message="Do you want to to cancel training?")
            if not ret:
                exit()
            continue
        elif not os.path.exists(res):
            res = ""
            continue
        _, name = os.path.split(res)
        split_name = name.split(".")
        if split_name[-1] not in accepted_ext_list:
            res = ""
    return res


def ask_dir(message, dir_path=None):
    mb.showinfo(message=message)
    res = ""
    _initialdir = ""
    if dir_path != None:
        _initialdir = dir_path if os.path.exists(dir_path) else ""
    while res == "":
        res = fd.askdirectory(title=message, initialdir=_initialdir)
        if res == "":
            ret = mb.askretrycancel(message="Do you want to to cancel training?")
            if not ret:
                exit()
            continue
        if not os.path.exists(res):
            res = ""
    return res


def ask_elements_trunc(args: dict):
    args['base_model'] = ask_file("Select your base model", {"ckpt", "safetensors"}, args['base_model'])
    args['img_folder'] = ask_dir("Select your image folder", args['img_folder'])
    args['output_folder'] = ask_dir("Select your output folder", args['output_folder'])

    ret = mb.askyesno(message="Do you want to save a json of your configuration?")
    if ret:
        args['save_json_folder'] = ask_dir("Select the folder to save json files to", args['save_json_folder'])
    else:
        args['save_json_folder'] = None

    ret = mb.askyesno(message="Are you training on a SD2 based model?")
    if ret:
        args['v2'] = True

    ret = mb.askyesno(message="Are you training on an realistic model?")
    if ret:
        args['clip_skip'] = 1

    if args['v2']:
        ret = mb.askyesno(message="Are you training on a model based on the 768x version of SD2?")
        if ret:
            args['v_parameterization'] = True

    ret = mb.askyesno(message="Do you want to use regularization images?")
    if ret:
        args['reg_img_folder'] = ask_dir("Select your regularization folder", args['reg_img_folder'])
    else:
        args['reg_img_folder'] = None

    ret = mb.askyesno(message="Do you want to continue from an earlier version?")
    if ret:
        args['lora_model_for_resume'] = ask_file("Select your lora model", {"ckpt", "pt", "safetensors"},
                                                 args['lora_model_for_resume'])
    else:
        args['lora_model_for_resume'] = None

    ret = mb.askyesno(message="Do you want to change the name of output checkpoints?")
    if ret:
        ret = sd.askstring(title="output_name", prompt="What do you want your output name to be?\n"
                                                       "Cancel keeps outputs the original")
        if ret:
            args['change_output_name'] = ret
        else:
            args['change_output_name'] = None

    ret = sd.askstring(title="comment",
                       prompt="Do you want to set a comment that gets put into the metadata?\nA good use of this would "
                              "be to include how to use, such as activation keywords.\nCancel will leave empty")
    if ret is None:
        args['training_comment'] = ret
    else:
        args['training_comment'] = None

    ret = mb.askyesno(message="Do you want to train only one of unet and text encoder?")
    if ret:
        button = ButtonBox("Which do you want to train with?", ["unet_only", "text_only"])
        button.window.mainloop()
        if button.current_value != "":
            args[button.current_value] = True

    ret = mb.askyesno(message="Do you want to save a txt file that contains a list\n"
                              "of all tags that you have used in your training data?\n"
                              "this will output so that the highest occurrences are at the top\n"
                              "of the file, with the file name that is the same as your output name")
    if ret:
        args['tag_occurrence_txt_file'] = True

    ret = mb.askyesno(message="Do you want to use caption dropout?")
    if ret:
        ret = mb.askyesno(message="Do you want full caption files to dropout randomly?")
        if ret:
            ret = sd.askinteger(title="Caption_File_Dropout",
                                prompt="How often do you want caption files to drop out?\n"
                                       "enter a number from 0 to 100 that is the percentage chance of dropout\n"
                                       "Cancel sets to 0")
            if ret and 0 <= ret <= 100:
                args['caption_dropout_rate'] = ret / 100.0

        ret = mb.askyesno(message="Do you want to have full epochs have no captions?")
        if ret:
            ret = sd.askinteger(title="Caption_epoch_dropout", prompt="The number set here is how often you will have an"
                                                                      "epoch with no captions\nSo if you set 3, then every"
                                                                      "three epochs will not have captions (3, 6, 9)\n"
                                                                      "Cancel will set to None")
            if ret:
                args['caption_dropout_every_n_epochs'] = ret

        ret = mb.askyesno(message="Do you want to have tags to randomly drop?")
        if ret:
            ret = sd.askinteger(title="Caption_tag_dropout", prompt="How often do you want tags to randomly drop out?\n"
                                                                    "Enter a number between 0 and 100 that is the percentage"
                                                                    "chance of dropout.\nCancel sets to 0")
            if ret and 0 <= ret <= 100:
                args['caption_tag_dropout_rate'] = ret / 100.0
    return args


def ask_elements(args: dict):
    # start with file dialog
    args['base_model'] = ask_file("Select your base model", {"ckpt", "safetensors"}, args['base_model'])
    args['img_folder'] = ask_dir("Select your image folder", args['img_folder'])
    args['output_folder'] = ask_dir("Select your output folder", args['output_folder'])

    # optional file dialog
    ret = mb.askyesno(message="Do you want to save a json of your configuration?")
    if ret:
        args['save_json_folder'] = ask_dir("Select the folder to save json files to", args['save_json_folder'])
    else:
        args['save_json_folder'] = None

    ret = mb.askyesno(message="Are you training on a SD2 based model?")
    if ret:
        args['v2'] = True

    ret = mb.askyesno(message="Are you training on an realistic model?")
    if ret:
        args['clip_skip'] = 1

    if args['v2']:
        ret = mb.askyesno(message="Are you training on a model based on the 768x version of SD2?")
        if ret:
            args['v_parameterization'] = True

    ret = mb.askyesno(message="Do you want to use regularization images?")
    if ret:
        args['reg_img_folder'] = ask_dir("Select your regularization folder", args['reg_img_folder'])
    else:
        args['reg_img_folder'] = None

    ret = mb.askyesno(message="Do you want to continue from an earlier version?")
    if ret:
        args['lora_model_for_resume'] = ask_file("Select your lora model", {"ckpt", "pt", "safetensors"},
                                                 args['lora_model_for_resume'])
    else:
        args['lora_model_for_resume'] = None

    # text based required elements
    ret = sd.askinteger(title="batch_size",
                        prompt="The number of images that get processed at one time, this is directly proportional to "
                               "your vram and resolution. with 12gb of vram, at 512 reso, you can get a maximum of 6 "
                               "batch size\nHow large is your batch size going to be?\nCancel will default to 1")
    if ret is None:
        args['batch_size'] = 1
    else:
        args['batch_size'] = ret

    ret = sd.askinteger(title="num_epochs", prompt="How many epochs do you want?\nCancel will default to 1")
    if ret is None:
        args['num_epochs'] = 1
    else:
        args['num_epochs'] = ret

    ret = sd.askinteger(title="network_dim", prompt="What is the dim size you want to use?\nCancel will default to 128")
    if ret is None:
        args['net_dim'] = 128
    else:
        args['net_dim'] = ret

    ret = sd.askfloat(title="alpha", prompt="Alpha is the scalar of the training, generally a good starting point is "
                                            "0.5x dim size\nWhat Alpha do you want?\nCancel will default to equal to "
                                            "0.5 x network_dim")
    if ret is None:
        args['alpha'] = args['net_dim'] / 2
    else:
        args['alpha'] = ret

    ret = sd.askinteger(title="resolution", prompt="How large of a resolution do you want to train at?\n"
                                                   "Cancel will default to 512")
    if ret is None:
        args['train_resolution'] = 512
    else:
        args['train_resolution'] = ret

    ret = sd.askfloat(title="learning_rate", prompt="What learning rate do you want to use?\n"
                                                    "Cancel will default to 1e-4")
    if ret is None:
        args['learning_rate'] = 1e-4
    else:
        args['learning_rate'] = ret

    ret = sd.askfloat(title="text_encoder_lr", prompt="Do you want to set the text_encoder_lr?\n"
                                                      "Cancel will default to None")
    if ret is None:
        args['text_encoder_lr'] = None
    else:
        args['text_encoder_lr'] = ret

    ret = sd.askfloat(title="unet_lr", prompt="Do you want to set the unet_lr?\nCancel will default to None")
    if ret is None:
        args['unet_lr'] = None
    else:
        args['unet_lr'] = ret

    button = ButtonBox("Which scheduler do you want?", ["cosine_with_restarts", "cosine", "polynomial",
                                                        "constant", "constant_with_warmup", "linear"])
    button.window.mainloop()
    args['scheduler'] = button.current_value if button.current_value != "" else "cosine_with_restarts"

    if args['scheduler'] == "cosine_with_restarts":
        ret = sd.askinteger(title="Cycle Count",
                            prompt="How many times do you want cosine to restart?\nThis is the entire amount of times "
                                   "it will restart for the entire training\nCancel will default to 1")
        if ret is None:
            args['cosine_restarts'] = 1
        else:
            args['cosine_restarts'] = ret

    if args['scheduler'] == "polynomial":
        ret = sd.askfloat(title="Poly Strength",
                          prompt="What power do you want to set your polynomial to?\nhigher power means that the "
                                 "model reduces the learning more more aggressively from initial training.\n1 = "
                                 "linear\nCancel sets to 1")
        if ret is None:
            args['scheduler_power'] = 1
        else:
            args['scheduler_power'] = ret

    ret = mb.askyesno(message="Do you want to save epochs as it trains?")
    if ret:
        ret = sd.askinteger(title="save_epoch",
                            prompt="How often do you want to save epochs?\nCancel will default to 1")
        if ret is None:
            args['save_at_n_epochs'] = 1
        else:
            args['save_at_n_epochs'] = ret

    ret = mb.askyesno(message="Do you want to shuffle captions?")
    if ret:
        args['shuffle_captions'] = True
    else:
        args['shuffle_captions'] = False

    ret = mb.askyesno(message="Do you want to keep some tokens at the front of your captions?")
    if ret:
        ret = sd.askinteger(title="keep_tokens", prompt="How many do you want to keep at the front?"
                                                        "\nCancel will default to 1")
        if ret is None:
            args['keep_tokens'] = 1
        else:
            args['keep_tokens'] = ret

    ret = mb.askyesno(message="Do you want to have a warmup ratio?")
    if ret:
        ret = sd.askfloat(title="warmup_ratio", prompt="What is the ratio of steps to use as warmup "
                                                       "steps?\nCancel will default to None")
        if ret is None:
            args['warmup_lr_ratio'] = None
        else:
            args['warmup_lr_ratio'] = ret

    ret = mb.askyesno(message="Do you want to change the name of output checkpoints?")
    if ret:
        ret = sd.askstring(title="output_name", prompt="What do you want your output name to be?\n"
                                                       "Cancel keeps outputs the original")
        if ret:
            args['change_output_name'] = ret
        else:
            args['change_output_name'] = None

    ret = sd.askstring(title="comment",
                       prompt="Do you want to set a comment that gets put into the metadata?\nA good use of this would "
                              "be to include how to use, such as activation keywords.\nCancel will leave empty")
    if ret is None:
        args['training_comment'] = ret
    else:
        args['training_comment'] = None

    ret = mb.askyesno(message="Do you want to train only one of unet and text encoder?")
    if ret:
        if ret:
            button = ButtonBox("Which do you want to train with?", ["unet_only", "text_only"])
            button.window.mainloop()
            if button.current_value != "":
                args[button.current_value] = True

    ret = mb.askyesno(message="Do you want to save a txt file that contains a list\n"
                              "of all tags that you have used in your training data?\n"
                              "this will output so that the highest occurrences are at the top\n"
                              "of the file, with the file name that is the same as your output name")
    if ret:
        args['tag_occurrence_txt_file'] = True

    ret = mb.askyesno(message="Do you want to use caption dropout?")
    if ret:
        ret = mb.askyesno(message="Do you want full caption files to dropout randomly?")
        if ret:
            ret = sd.askinteger(title="Caption_File_Dropout",
                                prompt="How often do you want caption files to drop out?\n"
                                       "enter a number from 0 to 100 that is the percentage chance of dropout\n"
                                       "Cancel sets to 0")
            if ret and 0 <= ret <= 100:
                args['caption_dropout_rate'] = ret / 100.0

        ret = mb.askyesno(message="Do you want to have full epochs have no captions?")
        if ret:
            ret = sd.askinteger(title="Caption_epoch_dropout", prompt="The number set here is how often you will have an"
                                                                      "epoch with no captions\nSo if you set 3, then every"
                                                                      "three epochs will not have captions (3, 6, 9)\n"
                                                                      "Cancel will set to None")
            if ret:
                args['caption_dropout_every_n_epochs'] = ret

        ret = mb.askyesno(message="Do you want to have tags to randomly drop?")
        if ret:
            ret = sd.askinteger(title="Caption_tag_dropout", prompt="How often do you want tags to randomly drop out?\n"
                                                                    "Enter a number between 0 and 100 that is the percentage"
                                                                    "chance of dropout.\nCancel sets to 0")
            if ret and 0 <= ret <= 100:
                args['caption_tag_dropout_rate'] = ret / 100.0
    return args


def save_json(path, obj: dict) -> None:
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
            if key in {"keep_tokens", "warmup_lr_ratio"}:
                json_obj[key] = int(json_obj[key]) if json_obj[key] is not None else None
            if key in {"learning_rate", "unet_lr", "text_encoder_lr"}:
                json_obj[key] = float(json_obj[key]) if json_obj[key] is not None else None
            if obj[key] != json_obj[key]:
                print_change(key, obj[key], json_obj[key])
                obj[key] = json_obj[key]
    print("completed changing variables.")
    return obj


def print_change(value, old, new):
    print(f"{value} changed from {old} to {new}")


class ButtonBox:
    def __init__(self, label: str, button_name_list: list[str]) -> None:
        self.window = tk.Tk()
        self.button_list = []
        self.current_value = ""

        self.window.attributes("-topmost", True)
        self.window.resizable(False, False)
        self.window.eval('tk::PlaceWindow . center')

        def del_window():
            self.window.quit()
            self.window.destroy()

        self.window.protocol("WM_DELETE_WINDOW", del_window)
        tk.Label(text=label, master=self.window).pack()
        for button in button_name_list:
            self.button_list.append(ttk.Button(text=button, master=self.window,
                                               command=partial(self.set_current_value, button)))
            self.button_list[-1].pack()

    def set_current_value(self, value):
        self.current_value = value
        self.window.quit()
        self.window.destroy()


root = tk.Tk()
root.attributes('-topmost', True)
root.withdraw()

if __name__ == "__main__":
    main()
