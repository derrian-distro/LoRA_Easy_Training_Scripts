import string
from typing import Union
import os
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from tkinter import messagebox as mb

import train_network
import library.train_util as util
import argparse


class ArgStore:
    def __init__(self):
        # folder and path params
        self.base_model: string = None
        self.img_folder: string = None
        self.output_folder: string = None
        self.reg_img_folder: Union[string, None] = None  # OPTIONAL, None to ignore
        self.lora_model_for_resume: Union[string, None] = None  # OPTIONAL, path for input lora to resume training

        # epoch, and learning rate params
        self.batch_size: int = 1
        self.num_epochs: int = 1
        self.save_at_n_epochs: Union[int, None] = None  # OPTIONAL, how often to save epochs, set to None if unwanted
        self.net_dim: int = 128  # network dimension, 128 seems to work best, change if you want
        self.learning_rate: float = 1e-4
        self.prior_loss_weight: float = 1  # is the loss weight much like Dreambooth, is required for LoRA training
        self.gradient_checkpointing: bool = False  # OPTIONAL, enables gradient checkpointing
        self.gradient_acc_steps: Union[int, None] = None  # OPTIONAL, not sure exactly what this means

        # resolution, seed, and clip params
        self.train_resolution: int = 512
        self.min_bucket_resolution: int = 320
        self.max_bucket_resolution: int = 960
        self.test_seed: int = 23
        self.clip_skip: int = 2

        # misc params
        self.mixed_precision: string = "fp16"
        self.save_precision: string = "fp16"
        self.save_as: string = "safetensors"  # list is pt, ckpt, safetensors

        # prompt params
        self.shuffle_captions: bool = False  # OPTIONAL
        self.keep_tokens: Union[int, None] = None  # OPTIONAL, None if you don't want to use it
        self.caption_extension: string = ".txt"
        self.max_clip_token_length = 150
        self.text_encoder_lr: Union[float, None] = None  # OPTIONAL, if you want to change the learning rate, there you go

        # Scheduler params
        # list of schedulers: linear, cosine, cosine_with_restarts, polynomial, constant, constant_with_warmup
        self.scheduler: string = "cosine_with_restarts"
        self.warmup_lr_ratio: Union[float, None] = None  # OPTIONAL, make sure to set this if you are using constant_with_warmup

        # OPTIONAL misc params
        self.buckets: bool = True  # enables/disables buckets
        self.xformers: bool = True
        self.use_8bit_adam: bool = True
        self.cache_latents: bool = True
        self.color_aug: bool = False  # IMPORTANT: Clashes with cache_latents, only have one of the two on!
        self.unet_lr: Union[float, None] = None
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
                f"--max_token_length={self.max_clip_token_length}", f"--lr_scheduler={self.scheduler}"]
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
                if ext[-1] in {"png", "bmp", "gif", "jpeg", "jpg", "webp"}:
                    imgs += 1
            total_steps += (num_repeats * imgs)
        total_steps = (total_steps // self.batch_size) * self.num_epochs
        return total_steps


def main():
    parser = argparse.ArgumentParser()
    setup_args(parser)
    arg_class = ArgStore()
    arg_class = ask_elements(arg_class)
    args = arg_class.create_arg_list()
    args = parser.parse_args(args)
    train_network.train(args)


def add_misc_args(parser):
    parser.add_argument("--no_metadata", action='store_true',
                        help="do not save metadata in output model / メタデータを出力先モデルに保存しない")
    parser.add_argument("--save_model_as", type=str, default="pt", choices=[None, "ckpt", "pt", "safetensors"],
                        help="format to save the model (default is .pt) / モデル保存時の形式（デフォルトはpt）")

    parser.add_argument("--unet_lr", type=float, default=None, help="learning rate for U-Net / U-Netの学習率")
    parser.add_argument("--text_encoder_lr", type=float, default=None,
                        help="learning rate for Text Encoder / Text Encoderの学習率")

    parser.add_argument("--network_weights", type=str, default=None,
                        help="pretrained weights for network / 学習するネットワークの初期重み")
    parser.add_argument("--network_module", type=str, default=None,
                        help='network module to train / 学習対象のネットワークのモジュール')
    parser.add_argument("--network_dim", type=int, default=None,
                        help='network dimensions (depends on each network) / モジュールの次元数（ネットワークにより定義は異なります）')
    parser.add_argument("--network_args", type=str, default=None, nargs='*',
                        help='additional argmuments for network (key=value) / ネットワークへの追加の引数')
    parser.add_argument("--network_train_unet_only", action="store_true",
                        help="only training U-Net part / U-Net関連部分のみ学習する")
    parser.add_argument("--network_train_text_encoder_only", action="store_true",
                        help="only training Text Encoder part / Text Encoder関連部分のみ学習する")


def setup_args(parser):
    util.add_sd_models_arguments(parser)
    util.add_dataset_arguments(parser, True, True)
    util.add_training_arguments(parser, True)
    add_misc_args(parser)


def ask_file(message, accepted_ext_list):
    mb.showinfo(message=message)
    res = ""
    while res == "":
        res = fd.askopenfilename(title=message)
        if res == "" or not os.path.exists(res):
            res = ""
            continue
        _, name = os.path.split(res)
        split_name = name.split(".")
        if split_name[-1] not in accepted_ext_list:
            res = ""
    return res


def ask_dir(message):
    mb.showinfo(message=message)
    res = ""
    while res == "":
        res = fd.askdirectory(title=message)
        if not os.path.exists(res):
            res = ""
    return res


def ask_elements(args: ArgStore):
    # start with file dialog
    args.base_model = ask_file("Select your base model", {"ckpt", "safetensors"})
    args.img_folder = ask_dir("Select your image folder")
    args.output_folder = ask_dir("Select your output folder")

    # optional file dialog
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

    ret = sd.askinteger(title="resolution", prompt="How large of a resolution do you want to train at?\nCancel will default to 512")
    if ret is None:
        args.train_resolution = 512
    else:
        args.train_resolution = ret

    ret = sd.askfloat(title="learning_rate", prompt="What learning rate do you want to use?\n Cancel will default to 1e-4")
    if ret is None:
        args.learning_rate = 1e-4
    else:
        args.learning_rate = ret

    ret = sd.askstring(title="scheduler", prompt="Which scheduler do you want?\n Cancel will default to \"cosine_with_restarts\"")
    if ret is None:
        args.scheduler = "cosine_with_restarts"
    else:
        schedulers = {"linear", "cosine", "cosine_with_restarts", "polynomial", "constant", "constant_with_warmup"}
        while ret not in schedulers:
            mb.showwarning(message=f"scheduler isn't valid.\nvalid schedulers are: {schedulers}")
            ret = sd.askstring(title="scheduler", prompt="Which scheduler do you want?\n Cancel will default to \"cosine_with_restarts\"")
            if ret is None:
                args.scheduler = "cosine_with_restarts"

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
        ret = sd.askinteger(title="keep_tokens", prompt="How many do you want to keep at the front?\nCancel will default to 1")
        if ret is None:
            args.keep_tokens = 1
        else:
            args.keep_tokens = ret

    ret = mb.askyesno(message="Do you want to have a warmup ratio?")
    if ret:
        ret = sd.askfloat(title="warmup_ratio", prompt="What is the ratio of steps to use as warmup steps?\nCancel will default to 0.05")
        if ret is None:
            args.warmup_lr_ratio = 0.05
        else:
            args.warmup_lr_ratio = ret
    return args


if __name__ == "__main__":
    main()
