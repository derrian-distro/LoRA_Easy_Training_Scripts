import time
from typing import Union
import os
import json
from json import JSONEncoder

import train_network
import library.train_util as util
import argparse


class ArgStore:
    def __init__(self):
        # Important, these are the most likely things you will modify
        self.base_model: str = r""  # example path, r"E:\sd\stable-diffusion-webui\models\Stable-diffusion\nai.ckpt"
        self.img_folder: str = r""
        self.output_folder: str = r""
        self.change_output_name: Union[str, None] = None  # OPTIONAL, changes how the output files are named
        self.save_json_folder: Union[str, None] = None  # OPTIONAL, saves a json folder of your config to whatever location you set here.
        self.load_json_path: Union[str, None] = None  # OPTIONAL, loads a json file partially changes the config to match. things like folder paths do not get modified.

        self.net_dim: int = 128  # network dimension, 128 seems to work best, change if you want
        self.alpha: float = 128  # setting it equal to net_dim makes it work equally to how it used to work.
        # list of schedulers: linear, cosine, cosine_with_restarts, polynomial, constant, constant_with_warmup
        self.scheduler: str = "cosine_with_restarts"
        self.cosine_restarts: Union[int, None] = 1  # OPTIONAL, only matters if you are using cosine_with_restarts
        self.scheduler_power: Union[float, None] = 1  # OPTIONAL, only matters if you are using polynomial
        self.warmup_lr_ratio: Union[float, None] = None  # OPTIONAL, make sure to set this if you are using constant_with_warmup, None to ignore
        self.learning_rate: Union[float, None] = 1e-4  # OPTIONAL, None to ignore, seems like people have started not setting this value, so I updated the script to allow for that.
        self.text_encoder_lr: Union[float, None] = None  # OPTIONAL, None to ignore
        self.unet_lr: Union[float, None] = None  # OPTIONAL, None to ignore
        self.num_workers: int = 8  # The number of threads that are being used to load images, lower speeds up the start of epochs, but slows down the loading of data. The assumption here is that it increases the training time as you reduce this value

        self.batch_size: int = 1
        self.num_epochs: int = 1
        self.save_at_n_epochs: Union[int, None] = 1  # OPTIONAL, how often to save epochs, None to ignore
        self.shuffle_captions: bool = False  # OPTIONAL, False to ignore
        self.keep_tokens: Union[int, None] = None  # OPTIONAL, None to ignore
        self.max_steps: Union[int, None] = None  # OPTIONAL, None to ignore, if you want, you can define an exact step count, the script will do the rest.

        # These are the second most likely things you will modify
        self.train_resolution: int = 512
        self.min_bucket_resolution: int = 320
        self.max_bucket_resolution: int = 960
        self.lora_model_for_resume: Union[str, None] = None  # OPTIONAL, takes an input lora to continue training from, not exactly the way it *should* be, but it works, None to ignore
        self.save_state: bool = False  # OPTIONAL, is the intended way to save a training state to use for continuing training, False to ignore
        self.load_previous_save_state: Union[str, None] = None  # OPTIONAL, is the intended way to load a training state to use for continuing training, None to ignore
        self.training_comment: Union[str, None] = None  # OPTIONAL, great way to put in things like activation tokens right into the metadata. seems to not work at this point and time

        # These are the least likely things you will modify
        self.reg_img_folder: Union[str, None] = None  # OPTIONAL, None to ignore
        self.clip_skip: int = 2
        self.test_seed: int = 23
        self.prior_loss_weight: float = 1  # is the loss weight much like Dreambooth, is required for LoRA training
        self.gradient_checkpointing: bool = False  # OPTIONAL, enables gradient checkpointing
        self.gradient_acc_steps: Union[int, None] = None  # OPTIONAL, not sure exactly what this means
        self.mixed_precision: str = "fp16"
        self.save_precision: str = "fp16"
        self.save_as: str = "safetensors"  # list is pt, ckpt, safetensors
        self.caption_extension: str = ".txt"
        self.max_clip_token_length = 150
        self.buckets: bool = True  # enables/disables buckets
        self.xformers: bool = True
        self.use_8bit_adam: bool = True
        self.cache_latents: bool = True
        self.color_aug: bool = False  # IMPORTANT: Clashes with cache_latents, only have one of the two on!
        self.flip_aug: bool = False
        self.vae: Union[str, None] = None
        self.no_meta: bool = False  # This removes the metadata that now gets saved into safetensors, (you should keep this on)

    def create_arg_list(self):
        ensure_path(self.base_model, "base_model", {"ckpt", "safetensors"})
        ensure_path(self.img_folder, "img_folder")
        ensure_path(self.output_folder, "output_folder")
        # This is the list of args that are to be used regardless of setup
        args = ["--network_module=networks.lora", f"--pretrained_model_name_or_path={self.base_model}",
                f"--train_data_dir={self.img_folder}", f"--output_dir={self.output_folder}",
                f"--prior_loss_weight={self.prior_loss_weight}", f"--caption_extension=" + self.caption_extension,
                f"--resolution={self.train_resolution}", f"--train_batch_size={self.batch_size}",
                f"--mixed_precision={self.mixed_precision}", f"--save_precision={self.save_precision}",
                f"--network_dim={self.net_dim}", f"--save_model_as={self.save_as}",
                f"--clip_skip={self.clip_skip}", f"--seed={self.test_seed}",
                f"--max_token_length={self.max_clip_token_length}", f"--lr_scheduler={self.scheduler}",
                f"--network_alpha={self.alpha}"]
        if not self.max_steps:
            steps = self.find_max_steps()
        else:
            steps = self.max_steps
        args.append(f"--max_train_steps={steps}")
        args = self.create_optional_args(args, steps)
        return args

    def create_optional_args(self, args, steps):
        if self.reg_img_folder:
            ensure_path(self.reg_img_folder, "reg_img_folder")
            args.append(f"--reg_data_dir={self.reg_img_folder}")

        if self.lora_model_for_resume:
            ensure_path(self.lora_model_for_resume, "lora_model_for_resume", {"pt", "ckpt", "safetensors"})
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

        if self.learning_rate and self.learning_rate > 0:
            args.append(f"--learning_rate={self.learning_rate}")

        if self.text_encoder_lr and self.text_encoder_lr > 0:
            args.append(f"--text_encoder_lr={self.text_encoder_lr}")

        if self.unet_lr and self.unet_lr > 0:
            args.append(f"--unet_lr={self.unet_lr}")

        if self.vae:
            args.append(f"--vae={self.vae}")

        if self.no_meta:
            args.append("--no_metadata")

        if self.save_state:
            args.append("--save_state")

        if self.load_previous_save_state:
            args.append(f"--resume={self.load_previous_save_state}")

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
        total_steps = int((total_steps / self.batch_size) * self.num_epochs)
        if self.quick_calc_regs():
            total_steps *= 2
        return total_steps

    def quick_calc_regs(self):
        if not self.reg_img_folder or not os.path.exists(self.reg_img_folder):
            return False
        folders = os.listdir(self.reg_img_folder)
        for folder in folders:
            if not os.path.isdir(os.path.join(self.reg_img_folder, folder)):
                continue
            num_repeats = folder.split("_")
            if len(num_repeats) < 2:
                continue
            try:
                num_repeats = int(num_repeats[0])
            except ValueError:
                continue
            for file in os.listdir(os.path.join(self.reg_img_folder, folder)):
                if os.path.isdir(file):
                    continue
                ext = file.split(".")
                if ext[-1].lower() in {"png", "bmp", "gif", "jpeg", "jpg", "webp"}:
                    return True
        return False


class ArgsEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def main():
    parser = argparse.ArgumentParser()
    setup_args(parser)
    arg_class = ArgStore()
    pre_args = parser.parse_args()
    if pre_args.load_json_path or arg_class.load_json_path:
        load_json(pre_args.load_json_path if pre_args.load_json_path else arg_class.load_json_path, arg_class)
    if pre_args.save_json_path or arg_class.save_json_folder:
        save_json(pre_args.save_json_path if pre_args.save_json_path else arg_class.save_json_folder, arg_class)
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


def ensure_path(path, name, ext_list=None):
    if ext_list is None:
        ext_list = {}
    folder = len(ext_list) == 0
    if path is None or not os.path.exists(path):
        print(f"Failed to find {name}, Please make sure path is correct.")
        quit(1)
    elif folder and os.path.isfile(path):
        print(f"Path given for {name} is that of a file, please select a folder.")
        quit(1)
    elif not folder and os.path.isdir(path):
        print(f"Path given for {name} is that of a folder, please select a file.")
        quit(1)
    elif not folder and path.split(".")[-1] not in ext_list:
        print(f"Found a file for {name}, however it wasn't of the accepted types: {ext_list}")
        quit(1)


def save_json(path, obj):
    ensure_path(path, "save_json_path")
    fp = open(os.path.join(path, f"config-{time.time()}.json"), "w")
    json.dump(obj, fp=fp, indent=4, cls=ArgsEncoder)
    fp.close()


def load_json(path, obj):
    ensure_path(path, "load_json_path", {"json"})
    json_obj = None
    with open(path) as f:
        json_obj = json.loads(f.read())
    print("json loaded, setting variables...")
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

    if "train_resolution" in json_obj and obj.train_resolution != json_obj["train_resolution"]:
        ans = check_input("train_resolution", obj.train_resolution, json_obj["train_resolution"])
        obj.train_resolution = process_input(ans, obj.train_resolution, json_obj["train_resolution"])
    elif "max_resolution" in json_obj and obj.train_resolution != int(json_obj["max_resolution"].split(",")[0]):
        ans = check_input("train_resolution", obj.train_resolution, int(json_obj["max_resolution"].split(",")[0]))
        obj.train_resolution = process_input(ans, obj.train_resolution, int(json_obj["max_resolution"].split(",")[0]))

    if "min_bucket_resolution" in json_obj and obj.min_bucket_resolution != json_obj["min_bucket_resolution"]:
        ans = check_input("min_bucket_resolution", obj.min_bucket_resolution, json_obj["min_bucket_resolution"])
        obj.min_bucket_resolution = process_input(ans, obj.min_bucket_resolution, json_obj["min_bucket_resolution"])

    if "max_bucket_resolution" in json_obj and obj.max_bucket_resolution != json_obj["max_bucket_resolution"]:
        ans = check_input("max_bucket_resolution", obj.max_bucket_resolution, json_obj["max_bucket_resolution"])
        obj.max_bucket_resolution = process_input(ans, obj.max_bucket_resolution, json_obj["max_bucket_resolution"])

    if "batch_size" in json_obj and obj.batch_size != json_obj["batch_size"]:
        ans = check_input("batch_size", obj.batch_size, json_obj["batch_size"])
        obj.batch_size = process_input(ans, obj.batch_size, json_obj["batch_size"])
    elif "train_batch_size" in json_obj and obj.batch_size != json_obj["train_batch_size"]:
        ans = check_input("batch_size", obj.batch_size, json_obj["train_batch_size"])
        obj.batch_size = process_input(ans, obj.batch_size, json_obj["train_batch_size"])

    if "num_epochs" in json_obj and obj.num_epochs != json_obj["num_epochs"]:
        ans = check_input("num_epochs", obj.num_epochs, json_obj["num_epochs"])
        obj.num_epochs = process_input(ans, obj.num_epochs, json_obj["num_epochs"])
    elif "epoch" in json_obj and obj.num_epochs != json_obj["epoch"]:
        ans = check_input("num_epochs", obj.num_epochs, json_obj["epoch"])
        obj.num_epochs = process_input(ans, obj.num_epochs, json_obj["epoch"])

    if "shuffle_captions" in json_obj and obj.shuffle_captions != json_obj["shuffle_captions"]:
        ans = check_input("shuffle_captions", obj.shuffle_captions, json_obj["shuffle_captions"], True)
        obj.shuffle_captions = process_input(ans, obj.shuffle_captions, json_obj["shuffle_captions"])
    elif "shuffle_caption" in json_obj and obj.shuffle_captions != json_obj["shuffle_caption"]:
        ans = check_input("shuffle_captions", obj.shuffle_captions, json_obj["shuffle_caption"], True)
        obj.shuffle_captions = process_input(ans, obj.shuffle_captions, json_obj["shuffle_caption"])

    if "keep_tokens" in json_obj and obj.keep_tokens != json_obj["keep_tokens"]:
        ans = check_input("keep_tokens", obj.keep_tokens, json_obj["keep_tokens"])
        obj.keep_tokens = process_input(ans, obj.keep_tokens, json_obj["keep_tokens"])
    print("completed changing variables.")


def check_input(name, oldval, newval, no_int: bool = False):
    ans = None
    while not ans:
        ans = input(f"{name} is different old:{oldval} -> new:{newval}\n"
                    f"Would you like to use the new value?\n" + ("Answer y/n or an int to overwrite both: " if not no_int else "Answer y/n: "))
        if not no_int:
            try:
                ans = int(ans)
                return ans
            except ValueError:
                pass
        if ans and ans not in {'y', 'Y', 'n', 'N'}:
            ans = None
    return ans


def process_input(value, oldval, newval):
    if type(value) is int:
        return value
    elif value in {'y', 'Y'}:
        return newval
    else:
        return oldval


def print_change(value, old, new):
    print(f"{value} changed from {old} to {new}")


if __name__ == "__main__":
    main()
