import argparse
import os
from typing import Union

import sd_scripts.library.train_util as util
import sd_scripts.library.config_util as config_util
import sd_scripts.library.custom_train_functions as custom_train_functions


def ensure_path(path, name, ext_list=None) -> bool:
    if ext_list is None:
        ext_list = {}
    folder = len(ext_list) == 0
    if path is None or not os.path.exists(path):
        print(f"Failed to find {name}, Please make sure path is correct.")
        quit()
    elif folder and os.path.isfile(path):
        print(f"Path given for {name} is that of a file, please select a folder.")
        quit()
    elif not folder and os.path.isdir(path):
        print(f"Path given for {name} is that of a folder, please select a file.")
        quit()
    elif not folder and path.split(".")[-1] not in ext_list:
        print(f"Found a file for {name}, however it wasn't of the accepted types: {ext_list}")
        quit()
    return True


class Parser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()
        util.add_sd_models_arguments(self.parser)
        util.add_dataset_arguments(self.parser, True, True, True)
        util.add_training_arguments(self.parser, True)
        util.add_optimizer_arguments(self.parser)
        config_util.add_config_arguments(self.parser)
        custom_train_functions.add_custom_train_arguments(self.parser)
        self.add_misc_args()

    def add_misc_args(self) -> None:
        self.parser.add_argument("--save_json_name", type=str, default=None,
                                 help="Changes the output name of json files to config-123312.13123214-set_name.json")
        self.parser.add_argument("--popup", action="store_true", help="argument to run popup mode")
        self.parser.add_argument("--multi_run_path", type=str, default=None,
                                 help="Path to load a set of json files to train all at once")
        self.parser.add_argument("--save_json_path", type=str, default=None,
                                 help="Path to save a configuration json file to")
        self.parser.add_argument("--load_json_path", type=str, default=None,
                                 help="Path to a json file to configure things from")
        self.parser.add_argument("--no_metadata", action='store_true',
                                 help="do not save metadata in output model / メタデータを出力先モデルに保存しない")
        self.parser.add_argument("--save_model_as", type=str, default="safetensors",
                                 choices=[None, "ckpt", "pt", "safetensors"],
                                 help="format to save the model (default is .safetensors) / モデル保存時の形式（デフォルトはsafetensors）")

        self.parser.add_argument("--unet_lr", type=float, default=None, help="learning rate for U-Net / U-Netの学習率")
        self.parser.add_argument("--text_encoder_lr", type=float, default=None,
                                 help="learning rate for Text Encoder / Text Encoderの学習率")

        self.parser.add_argument("--network_weights", type=str, default=None,
                                 help="pretrained weights for network / 学習するネットワークの初期重み")
        self.parser.add_argument("--network_module", type=str, default=None,
                                 help='network module to train / 学習対象のネットワークのモジュール')
        self.parser.add_argument("--network_dim", type=int, default=None,
                                 help='network dimensions (depends on each network) / モジュールの次元数（ネットワークにより定義は異なります）')
        self.parser.add_argument("--network_alpha", type=float, default=1,
                                 help='alpha for LoRA weight scaling, default 1 (same as network_dim for same behavior as '
                                      'old version) / LoRaの重み調整のalpha値、デフォルト1（旧バージョンと同じ動作をするにはnetwork_dimと同じ値を指定）')
        self.parser.add_argument("--network_args", type=str, default=None, nargs='*',
                                 help='additional argmuments for network (key=value) / ネットワークへの追加の引数')
        self.parser.add_argument("--network_train_unet_only", action="store_true",
                                 help="only training U-Net part / U-Net関連部分のみ学習する")
        self.parser.add_argument("--network_train_text_encoder_only", action="store_true",
                                 help="only training Text Encoder part / Text Encoder関連部分のみ学習する")
        self.parser.add_argument("--training_comment", type=str, default=None,
                                 help="arbitrary comment string stored in metadata / メタデータに記録する任意のコメント文字列")

    def parse_args(self, args: Union[list[str], None] = None) -> argparse.Namespace:
        return self.parser.parse_args(args) if args else self.parser.parse_args()

    def create_args(self, args: dict) -> argparse.Namespace:
        remove_epochs = False
        args_list = []
        skip_list = ["save_json_folder", "load_json_path", "multi_run_folder", "json_load_skip_list",
                     "tag_occurrence_txt_file", "sort_tag_occurrence_alphabetically", "save_json_only",
                     "warmup_lr_ratio", "optimizer_args", "locon_dim", "locon_alpha", "locon", "lyco", "network_args",
                     "resolution", "height_resolution"]
        for key, value in args.items():
            if not value:
                continue
            if key in skip_list:
                continue
            if key == "max_train_steps":
                remove_epochs = True
            if isinstance(value, bool):
                args_list.append(f"--{key}")
            else:
                args_list.append(f"--{key}={value}")

        name_space = self.parser.parse_args(args_list)
        if 'height_resolution' in args and args['height_resolution']:
            name_space.resolution = f"{args['resolution']},{args['height_resolution']}"
        else:
            name_space.resolution = f"{args['resolution']}"

        if remove_epochs:
            name_space.max_train_epochs = None

        if 'optimizer_args' in args:
            name_space.optimizer_args = []
            for key, value in args['optimizer_args'].items():
                if key == "betas" and args['optimizer_type'] in {"AdaFactor", "SGDNesterov", "SGDNesterov8bit"}:
                    continue
                name_space.optimizer_args.append(f"{key}={value}")

        if args['optimizer_type'] == "DAdaptation":
            name_space.optimizer_args.append("decouple=True")

        if "use_8bit_adam" in args and args['use_8bit_adam'] is True:
            name_space.optimizer_type = ""
        if "use_lion_optimizer" in args and args['use_lion_optimizer'] is True:
            name_space.optimizer_type = ""

        if args['locon_dim']:
            if not args['network_args']:
                args['network_args'] = dict()
            args['network_args']['conv_dim'] = args['locon_dim']
        if args['locon_alpha']:
            if not args['network_args']:
                args['network_args'] = dict()
            args['network_args']['conv_alpha'] = args['locon_alpha']

        lyco = 'lyco' in args and args['lyco'] is True
        name_space.network_module = 'lycoris.kohya' if lyco else 'sd_scripts.networks.lora'

        if 'network_args' in args and args['network_args']:
            name_space.network_args = []
            for key, value in args['network_args'].items():
                name_space.network_args.append(f"{key}={value}")

        if 'lr_scheduler_args' in args and args['lr_scheduler_args']:
            name_space.lr_scheduler_args = []
            for key, value in args['lr_scheduler_args'].items():
                name_space.lr_scheduler_args.append(f"{key}={value}")
        return name_space
