import json
import string
import time
from json import JSONEncoder
from typing import Union
import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from tkinter import messagebox as mb

import train_network
import library.train_util as util
import argparse


class ArgStore:
    def __init__(self):
        # Important, these are the most likely things you will modify
        self.base_model: string = None  # example path, make sure to use \\ instead of \ if on windows -> "E:\\sd\\stable-diffusion-webui\\models\\Stable-diffusion\\nai.ckpt"
        self.img_folder: string = None
        self.output_folder: string = None
        self.change_output_name: Union[string, None] = None  # OPTIONAL, changes how the output files are named
        self.save_json_folder: Union[string, None] = None  # OPTIONAL, saves a json folder of your config to whatever location you set here.
        self.load_json_path: Union[string, None] = None  # OPTIONAL, loads a json file partially changes the config to match. things like folder paths do not get modified.

        self.net_dim: int = 128  # network dimension, 128 seems to work best, change if you want
        self.alpha: float = 128  # setting it equal to net_dim makes it work equally to how it used to work.
        # list of schedulers: linear, cosine, cosine_with_restarts, polynomial, constant, constant_with_warmup
        self.scheduler: string = "cosine_with_restarts"
        self.cosine_restarts: Union[int, None] = 1  # OPTIONAL, only matters if you are using cosine_with_restarts
        self.scheduler_power: Union[float, None] = 1  # OPTIONAL, only matters if you are using polynomial
        self.warmup_lr_ratio: Union[float, None] = None  # OPTIONAL, make sure to set this if you are using constant_with_warmup, None to ignore
        self.learning_rate: float = 1e-4
        self.text_encoder_lr: Union[float, None] = None  # OPTIONAL, None to ignore
        self.unet_lr: Union[float, None] = None  # OPTIONAL, None to ignore
        self.num_workers: int = 8  # The number of threads that are being used to load images, lower speeds up the start of epochs, but slows down the loading of data. The assumption here is that it increases the training time as you reduce this value

        self.batch_size: int = 1
        self.num_epochs: int = 1
        self.save_at_n_epochs: Union[int, None] = None  # OPTIONAL, how often to save epochs, None to ignore
        self.shuffle_captions: bool = False  # OPTIONAL, False to ignore
        self.keep_tokens: Union[int, None] = None  # OPTIONAL, None to ignore

        # These are the second most likely things you will modify
        self.train_resolution: int = 512
        self.min_bucket_resolution: int = 320
        self.max_bucket_resolution: int = 960
        self.lora_model_for_resume: Union[string, None] = None  # OPTIONAL, takes an input lora to continue training from, not exactly the way it *should* be, but it works, None to ignore
        self.save_state: bool = False  # OPTIONAL, is the intended way to save a training state to use for continuing training, False to ignore
        self.load_previous_save_state: Union[string, None] = None  # OPTIONAL, is the intended way to load a training state to use for continuing training, None to ignore
        self.training_comment: Union[str, None] = None  # OPTIONAL, great way to put in things like activation tokens right into the metadata.

        # These are the least likely things you will modify
        self.reg_img_folder: Union[string, None] = None  # OPTIONAL, None to ignore
        self.clip_skip: int = 2
        self.test_seed: int = 23
        self.prior_loss_weight: float = 1  # is the loss weight much like Dreambooth, is required for LoRA training
        self.gradient_checkpointing: bool = False  # OPTIONAL, enables gradient checkpointing
        self.gradient_acc_steps: Union[int, None] = None  # OPTIONAL, not sure exactly what this means
        self.mixed_precision: string = "fp16"
        self.save_precision: string = "fp16"
        self.save_as: string = "safetensors"  # list is pt, ckpt, safetensors
        self.caption_extension: string = ".txt"
        self.max_clip_token_length = 150
        self.buckets: bool = True  # enables/disables buckets
        self.xformers: bool = True
        self.use_8bit_adam: bool = True
        self.cache_latents: bool = True
        self.color_aug: bool = False  # IMPORTANT: Clashes with cache_latents, only have one of the two on!
        self.flip_aug: bool = False
        self.vae: Union[string, None] = None
        self.no_meta: bool = False  # This removes the metadata that now gets saved into safetensors, (you should keep this on)

    def create_arg_list(self):
        # This is the list of args that are to be used regardless of setup
        args = ["--network_module=networks.lora", f"--pretrained_model_name_or_path={self.base_model}",
                f"--train_data_dir={self.img_folder}", f"--output_dir={self.output_folder}",
                f"--prior_loss_weight={self.prior_loss_weight}", f"--caption_extension=" + self.caption_extension,
                f"--resolution={self.train_resolution}", f"--train_batch_size={self.batch_size}",
                f"--learning_rate={self.learning_rate}", f"--mixed_precision={self.mixed_precision}",
                f"--save_precision={self.save_precision}", f"--network_dim={self.net_dim}",
                f"--save_model_as={self.save_as}", f"--clip_skip={self.clip_skip}", f"--seed={self.test_seed}",
                f"--max_token_length={self.max_clip_token_length}", f"--lr_scheduler={self.scheduler}",
                f"--network_alpha={self.alpha}"]
        steps = self.find_max_steps()
        args.append(f"--max_train_steps={steps}")
        args = self.create_optional_args(args, steps)
        return args

    def create_optional_args(self, args, steps):
        if self.reg_img_folder:
            args.append(f"--reg_data_dir={self.reg_img_folder}")

        if self.lora_model_for_resume:
            args.append(f"--network_weights={self.lora_model_for_resume}")

        if self.save_at_n_epochs:
            args.append(f"--save_every_n_epochs={self.save_at_n_epochs}")
        else:
            args.append("--save_every_n_epochs=999999")

        if self.shuffle_captions:
            args.append("--shuffle_caption")

        if self.keep_tokens and self.keep_tokens > 0:
            args.append(f"--keep_tokens={self.keep_tokens}")

        if self.buckets:
            args.append("--enable_bucket")
            args.append(f"--min_bucket_reso={self.min_bucket_resolution}")
            args.append(f"--max_bucket_reso={self.max_bucket_resolution}")

        if self.use_8bit_adam:
            args.append("--use_8bit_adam")

        if self.xformers:
            args.append("--xformers")

        if self.color_aug:
            if self.cache_latents:
                print("color_aug and cache_latents conflict with one another. Please select only one")
                quit(1)
            args.append("--color_aug")

        if self.flip_aug:
            args.append("--flip_aug")

        if self.cache_latents:
            args.append("--cache_latents")

        if self.warmup_lr_ratio and self.warmup_lr_ratio > 0:
            warmup_steps = int(steps * self.warmup_lr_ratio)
            args.append(f"--lr_warmup_steps={warmup_steps}")

        if self.gradient_checkpointing:
            args.append("--gradient_checkpointing")

        if self.gradient_acc_steps and self.gradient_acc_steps > 0 and self.gradient_checkpointing:
            args.append(f"--gradient_accumulation_steps={self.gradient_acc_steps}")

        if self.text_encoder_lr and self.text_encoder_lr > 0:
            args.append(f"--text_encoder_lr={self.text_encoder_lr}")

        if self.unet_lr and self.unet_lr > 0:
            args.append(f"--unet_lr={self.unet_lr}")

        if self.vae:
            args.append(f"--vae={self.vae}")

        if self.no_meta:
            args.append("--no_metadata")

        if self.change_output_name:
            args.append(f"--output_name={self.change_output_name}")

        if self.training_comment:
            args.append(f"--training_comment={self.training_comment}")

        if self.num_workers:
            args.append(f"--max_data_loader_n_workers={self.num_workers}")

        if self.cosine_restarts and self.scheduler == "cosine_with_restarts":
            args.append(f"--lr_scheduler_num_cycles={self.cosine_restarts}")

        if self.scheduler_power and self.scheduler == "polynomial":
            args.append(f"--lr_scheduler_power={self.scheduler_power}")
        return args

    def find_max_steps(self):
        total_steps = 0
        folders = os.listdir(self.img_folder)
        for folder in folders:
            if not os.path.isdir(os.path.join(self.img_folder, folder)):
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
            for file in os.listdir(os.path.join(self.img_folder, folder)):
                if os.path.isdir(file):
                    continue
                ext = file.split(".")
                if ext[-1].lower() in {"png", "bmp", "gif", "jpeg", "jpg", "webp"}:
                    imgs += 1
            total_steps += (num_repeats * imgs)
        total_steps = (total_steps // self.batch_size) * self.num_epochs
        return total_steps


class ArgsEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def main():
    parser = argparse.ArgumentParser()
    setup_args(parser)
    arg_class = ArgStore()
    ret = mb.askyesno(message="Do you want to load a json config file?")
    if ret:
        load_json(ask_file("json to load from", {"json"}), arg_class)
        arg_class = ask_elements_trunc(arg_class)
    else:
        arg_class = ask_elements(arg_class)
    if arg_class.save_json_folder:
        save_json(arg_class.save_json_folder, arg_class)
    args = arg_class.create_arg_list()
    args = parser.parse_args(args)
    train_network.train(args)


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
    util.add_dataset_arguments(parser, True, True)
    util.add_training_arguments(parser, True)
    add_misc_args(parser)


def ask_file(message, accepted_ext_list, file_path=None):
    mb.showinfo(message=message)
    res = ""
    _initialdir  = ""
    _initialfile = ""
    if file_path!=None:
        _initialdir  = os.path.dirname(file_path) if os.path.exists(file_path) else ""
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
    if dir_path!=None:
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


def ask_elements_trunc(args: ArgStore):
    args.base_model = ask_file("Select your base model", {"ckpt", "safetensors"}, args.base_model)
    args.img_folder = ask_dir("Select your image folder", args.img_folder)
    args.output_folder = ask_dir("Select your output folder", args.output_folder)

    ret = mb.askyesno(message="Do you want to save a json of your configuration?")
    if ret:
        args.save_json_folder = ask_dir("Select the folder to save json files to", args.save_json_folder)
    else:
        args.save_json_folder = None

    ret = sd.askinteger(title="num_workers", prompt="How many workers do you want? higher means longer epoch starts, but faster data loading, and has higher System Memory Usage.\nIf you want fast epoch start times, set this number to 1.\nCancel defaults to 8")
    if ret:
        args.num_workers = ret
    else:
        args.num_workers = 8

    ret = mb.askyesno(message="Do you want to use regularisation images?")
    if ret:
        args.reg_img_folder = ask_dir("Select your regularisation folder", args.reg_img_folder)

    ret = mb.askyesno(message="Do you want to continue from an earlier version?")
    if ret:
        args.lora_model_for_resume = ask_file("Select your lora model", {"ckpt", "pt", "safetensors"}, args.lora_model_for_resume)

    ret = mb.askyesno(message="Do you want to change the name of output epochs?")
    if ret:
        ret = sd.askstring(title="output_name", prompt="What do you want your output name to be?\n"
                                                       "Cancel keeps outputs the original")
        if ret:
            args.change_output_name = ret
        else:
            args.change_output_name = None

    ret = sd.askfloat(title="alpha", prompt="What Alpha do you want?\nCancel will default to equal to network_dim")
    if ret is None:
        args.alpha = args.net_dim
    else:
        args.alpha = ret

    #ret = sd.askstring(title="comment",
    #                  prompt="Do you want to set a comment that gets put into the metadata?\nA good use of this would be to include how to use, such as activation keywords.\nCancel will leave empty")
    #if ret is None:
    #    args.training_comment = ret
    #else:
    #    args.training_comment = None
    return args


def ask_elements(args: ArgStore):
    # start with file dialog
    args.base_model = ask_file("Select your base model", {"ckpt", "safetensors"})
    args.img_folder = ask_dir("Select your image folder")
    args.output_folder = ask_dir("Select your output folder")

    # optional file dialog
    ret = mb.askyesno(message="Do you want to save a json of your configuration?")
    if ret:
        args.save_json_folder = ask_dir("Select the folder to save json files to")

    ret = sd.askinteger(title="num_workers",
                        prompt="How many workers do you want? higher means longer epoch starts, but faster data loading, and has higher System Memory Usage.\nIf you want fast epoch start times, set this number to 1.\nCancel defaults to 8")
    if ret:
        args.num_workers = ret
    else:
        args.num_workers = 8

    ret = mb.askyesno(message="Do you want to use regularisation images?")
    if ret:
        args.reg_img_folder = ask_dir("Select your regularisation folder")

    ret = mb.askyesno(message="Do you want to continue from an earlier version?")
    if ret:
        args.lora_model_for_resume = ask_file("Select your lora model", {"ckpt", "pt", "safetensors"})

    # text based required elements
    ret = sd.askinteger(title="batch_size", prompt="How large is your batch size going to be?\nCancel will default to 1")
    if ret is None:
        args.batch_size = 1
    else:
        args.batch_size = ret

    ret = sd.askinteger(title="num_epochs", prompt="How many epochs do you want?\nCancel will default to 1")
    if ret is None:
        args.num_epochs = 1
    else:
        args.num_epochs = ret

    ret = sd.askinteger(title="network_dim", prompt="What is the dim size you want to use?\nCancel will default to 128")
    if ret is None:
        args.net_dim = 128
    else:
        args.net_dim = ret

    ret = sd.askfloat(title="alpha", prompt="What Alpha do you want?\nCancel will default to equal to network_dim")
    if ret is None:
        args.alpha = args.net_dim
    else:
        args.alpha = ret

    ret = sd.askinteger(title="resolution", prompt="How large of a resolution do you want to train at?\n"
                                                   "Cancel will default to 512")
    if ret is None:
        args.train_resolution = 512
    else:
        args.train_resolution = ret

    ret = sd.askfloat(title="learning_rate", prompt="What learning rate do you want to use?\n"
                                                    "Cancel will default to 1e-4")
    if ret is None:
        args.learning_rate = 1e-4
    else:
        args.learning_rate = ret

    ret = sd.askfloat(title="text_encoder_lr", prompt="Do you want to set the text_encoder_lr?\n"
                      "Cancel will default to None")
    if ret is None:
        args.text_encoder_lr = None
    else:
        args.text_encoder_lr = ret

    ret = sd.askfloat(title="unet_lr", prompt="Do you want to set the unet_lr?\nCancel will default to None")
    if ret is None:
        args.unet_lr = None
    else:
        args.unet_lr = ret

    ret = sd.askstring(title="scheduler", prompt="Which scheduler do you want?\n Cancel will default "
                                                 "to \"cosine_with_restarts\"")
    if ret is None:
        args.scheduler = "cosine_with_restarts"
    else:
        schedulers = {"linear", "cosine", "cosine_with_restarts", "polynomial", "constant", "constant_with_warmup"}
        while ret not in schedulers:
            mb.showwarning(message=f"scheduler isn't valid.\nvalid schedulers are: {schedulers}")
            ret = sd.askstring(title="scheduler", prompt="Which scheduler do you want?\n Cancel will default "
                                                         "to \"cosine_with_restarts\"")
            if ret is None:
                args.scheduler = "cosine_with_restarts"

    if args.scheduler == "cosine_with_restarts":
        ret = sd.askinteger(title="Cycle Count", prompt="How many times do you want cosine to restart?\nThis is the entire amount of times it will restart for the entire training\nCancel will default to 1")
        if ret is None:
            args.cosine_restarts = 1
        else:
            args.cosine_restarts = ret

    if args.scheduler == "polynomial":
        ret = sd.askfloat(title="Poly Strength", prompt="What power do you want to set your polynomial to?\nhigher power means that the model reduces the learning more more aggressively from initial training.\n1 = linear\nCancel sets to 1")
        if ret is None:
            args.scheduler_power = 1
        else:
            args.scheduler_power = ret

    ret = mb.askyesno(message="do you want to save intermediate epochs?")
    if ret:
        ret = sd.askinteger(title="save_epoch", prompt="How often do you want to save epochs?\nCancel will default to 1")
        if ret is None:
            args.save_at_n_epochs = 1
        else:
            args.save_at_n_epochs = ret

    ret = mb.askyesno(message="Do you want to shuffle captions?")
    if ret:
        args.shuffle_captions = True
    else:
        args.shuffle_captions = False

    ret = mb.askyesno(message="Do you want to keep some tokens at the front of your captions?")
    if ret:
        ret = sd.askinteger(title="keep_tokens", prompt="How many do you want to keep at the front?"
                                                        "\nCancel will default to 1")
        if ret is None:
            args.keep_tokens = 1
        else:
            args.keep_tokens = ret

    ret = mb.askyesno(message="Do you want to have a warmup ratio?")
    if ret:
        ret = sd.askfloat(title="warmup_ratio", prompt="What is the ratio of steps to use as warmup "
                                                       "steps?\nCancel will default to 0.05")
        if ret is None:
            args.warmup_lr_ratio = 0.05
        else:
            args.warmup_lr_ratio = ret

    ret = mb.askyesno(message="Do you want to change the name of output epochs?")
    if ret:
        ret = sd.askstring(title="output_name", prompt="What do you want your output name to be?\n"
                                                       "Cancel keeps outputs the original")
        if ret:
            args.change_output_name = ret
        else:
            args.change_output_name = None

    #ret = sd.askstring(title="comment",
    #                  prompt="Do you want to set a comment that gets put into the metadata?\nA good use of this would be to include how to use, such as activation keywords.\nCancel will leave empty")
    #if ret is None:
    #    args.training_comment = ret
    #else:
    #    args.training_comment = None
    return args


def save_json(path, obj):
    fp = open(os.path.join(path, f"config-{time.time()}.json"), "w")
    json.dump(obj, fp=fp, indent=4, cls=ArgsEncoder)
    fp.close()


def load_json(path, obj: ArgStore):
    json_obj = None
    with open(path) as f:
        json_obj = json.loads(f.read())
    print("json loaded, setting variables...")

    if "base_model" in json_obj:
        old = obj.base_model
        obj.base_model = json_obj["base_model"]
        print_change("base_model", old, obj.base_model)

    if "img_folder" in json_obj:
        old = obj.img_folder
        obj.img_folder = json_obj["img_folder"]
        print_change("img_folder", old, obj.img_folder)

    if "output_folder" in json_obj:
        old = obj.output_folder
        obj.output_folder = json_obj["output_folder"]
        print_change("output_folder", old, obj.output_folder)

    if "change_output_name" in json_obj:
        old = obj.change_output_name
        obj.change_output_name = json_obj["change_output_name"]
        print_change("change_output_name", old, obj.change_output_name)

    if "save_json_folder" in json_obj:
        old = obj.save_json_folder
        obj.save_json_folder = json_obj["save_json_folder"]
        print_change("save_json_folder", old, obj.save_json_folder)

    if "load_json_path" in json_obj:
        old = obj.load_json_path
        obj.load_json_path = json_obj["load_json_path"]
        print_change("load_json_path", old, obj.load_json_path)

    if "net_dim" in json_obj:
        old = obj.net_dim
        obj.net_dim = json_obj["net_dim"]
        print_change("net_dim", old, obj.net_dim)
    elif "network_dim" in json_obj:
        old = obj.net_dim
        obj.net_dim = json_obj["network_dim"]
        print_change("net_dim", old, obj.net_dim)

    if "scheduler" in json_obj:
        old = obj.scheduler
        obj.scheduler = json_obj["scheduler"]
        print_change("scheduler", old, obj.scheduler)
    elif "lr_scheduler" in json_obj:
        old = obj.scheduler
        obj.scheduler = json_obj["lr_scheduler"]
        print_change("scheduler", old, obj.scheduler)

    if "warmup_lr_ratio" in json_obj:
        old = obj.warmup_lr_ratio
        obj.warmup_lr_ratio = json_obj["warmup_lr_ratio"]  # UI version doesn't have an equivalent, only handles steps
        print_change("warmup_lr_ratio", old, obj.warmup_lr_ratio)

    if "learning_rate" in json_obj:
        old = obj.learning_rate
        obj.learning_rate = json_obj["learning_rate"]
        print_change("learning_rate", old, obj.learning_rate)

    if "text_encoder_lr" in json_obj:
        old = obj.text_encoder_lr
        obj.text_encoder_lr = json_obj["text_encoder_lr"]  # UI version is the same
        print_change("text_encoder_lr", old, obj.text_encoder_lr)

    if "unet_lr" in json_obj:
        old = obj.unet_lr
        obj.unet_lr = json_obj["unet_lr"]  # UI version is the same
        print_change("unet_lr", old, obj.unet_lr)

    if "clip_skip" in json_obj:
        old = obj.clip_skip
        obj.clip_skip = json_obj["clip_skip"]  # UI version is the same
        print_change("clip_skip", old, obj.clip_skip)

    old_tr = obj.train_resolution
    if "train_resolution" in json_obj:
        obj.train_resolution = json_obj["train_resolution"]

    if "min_bucket_resolution" in json_obj:
        obj.min_bucket_resolution = json_obj["min_bucket_resolution"]

    if "max_bucket_resolution" in json_obj:
        obj.max_bucket_resolution = json_obj["max_bucket_resolution"]

    if "num_epochs" in json_obj:
        obj.num_epochs = json_obj["num_epochs"]

    if "shuffle_captions" in json_obj:
        obj.shuffle_captions = json_obj["shuffle_captions"]

    if "keep_tokens" in json_obj:
        obj.keep_tokens = json_obj["keep_tokens"]

    if old_tr != obj.train_resolution:
        ans = sd.askinteger(title="batch_size", prompt=f"Your train resolution changed from {old_tr} to "
                                                       f"{obj.train_resolution}.\nSelect a new value for batch_size, "
                                                       f"if you don't know hit cancel\nCancel defaults to 1")
        if ans:
            obj.batch_size = ans
        else:
            obj.batch_size = 1
    elif "batch_size" in json_obj:
        obj.batch_size = json_obj["batch_size"]
    print("completed changing variables.")


def print_change(value, old, new):
    print(f"{value} changed from {old} to {new}")


root = tk.Tk()
root.attributes('-topmost', True)
root.withdraw()

if __name__ == "__main__":
    main()
