import argparse
import os

import sd_scripts.library.train_util as util


def ensure_path(path, name, ext_list=None) -> bool:
    if ext_list is None:
        ext_list = {}
    folder = len(ext_list) == 0
    if path is None or not os.path.exists(path):
        print(f"Failed to find {name}, Please make sure path is correct.")
        return False
    elif folder and os.path.isfile(path):
        print(f"Path given for {name} is that of a file, please select a folder.")
        return False
    elif not folder and os.path.isdir(path):
        print(f"Path given for {name} is that of a folder, please select a file.")
        return False
    elif not folder and path.split(".")[-1] not in ext_list:
        print(f"Found a file for {name}, however it wasn't of the accepted types: {ext_list}")
        return False
    return True


class Parser:
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser()
        util.add_sd_models_arguments(self.parser)
        util.add_dataset_arguments(self.parser, True, True, True)
        util.add_training_arguments(self.parser, True)
        util.add_optimizer_arguments(self.parser)
        self.add_misc_args()

    def add_misc_args(self) -> None:
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
        # self.parser.add_argument("--lr_scheduler_num_cycles", type=int, default=1,
        #                          help="Number of restarts for cosine scheduler with restarts / cosine with "
        #                               "restartsスケジューラでのリスタート回数")
        # self.parser.add_argument("--lr_scheduler_power", type=float, default=1,
        #                          help="Polynomial power for polynomial scheduler / polynomialスケジューラでのpolynomial power")

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

    def parse_args(self, args: list[str]) -> argparse.Namespace:
        return self.parser.parse_args(args)

    def create_args(self, args: dict) -> argparse.Namespace:
        args_list = []
        skip_list = ["save_json_folder", "load_json_path", "multi_run_folder", "json_load_skip_list",
                     "tag_occurrence_txt_file", "sort_tag_occurrence_alphabetically", "save_json_only",
                     "warmup_lr_ratio"]
        for key, value in args.items():
            if not value:
                continue
            if key in skip_list:
                continue
            if isinstance(value, bool):
                args_list.append(f"--{key}")
            else:
                args_list.append(f"--{key}={value}")
        return self.parser.parse_args(args_list)
        # if not ensure_path(args["base_model"], "base_model", {"ckpt", "safetensors"}):
        #     raise FileNotFoundError("Failed to find base model, make sure you have the correct path")
        # if not ensure_path(args["img_folder"], "img_folder"):
        #     raise FileNotFoundError("Failed to find the image folder, make sure you have the correct path")
        # if not ensure_path(args["output_folder"], "output_folder"):
        #     raise FileNotFoundError("Failed to find the output folder, make sure you have the correct path")
        # # This is the list of args that are to be used regardless of setup
        # output = ["--network_module=networks.lora", f"--pretrained_model_name_or_path={args['base_model']}",
        #           f"--train_data_dir={args['img_folder']}", f"--output_dir={args['output_folder']}",
        #           f"--prior_loss_weight={args['prior_loss_weight']}",
        #           f"--caption_extension=" + args['caption_extension'],
        #           f"--resolution={args['train_resolution']}", f"--train_batch_size={args['batch_size']}",
        #           f"--mixed_precision={args['mixed_precision']}", f"--save_precision={args['save_precision']}",
        #           f"--network_dim={args['net_dim']}", f"--save_model_as={args['save_as']}",
        #           f"--clip_skip={args['clip_skip']}", f"--seed={args['test_seed']}",
        #           f"--max_token_length={args['max_clip_token_length']}", f"--lr_scheduler={args['scheduler']}",
        #           f"--network_alpha={args['alpha']}", f"--max_data_loader_n_workers={args['num_workers']}"]
        # if not args['max_steps']:
        #     output.append(f"--max_train_epochs={args['num_epochs']}")
        #     output += create_optional_args(args, find_max_steps(args))
        # else:
        #     output.append(f"--max_train_steps={args['max_steps']}")
        #     output += create_optional_args(args, args['max_steps'])
        # return output
        # # return self.parser.parse_args(args)
        # pass


# def create_optional_args(args: dict, steps):
#     output = []
#     if args["reg_img_folder"]:
#         if not ensure_path(args["reg_img_folder"], "reg_img_folder"):
#             raise FileNotFoundError("Failed to find the reg image folder, make sure you have the correct path")
#         output.append(f"--reg_data_dir={args['reg_img_folder']}")
#
#     if args['lora_model_for_resume']:
#         if not ensure_path(args['lora_model_for_resume'], "lora_model_for_resume", {"pt", "ckpt", "safetensors"}):
#             raise FileNotFoundError("Failed to find the lora model, make sure you have the correct path")
#         output.append(f"--network_weights={args['lora_model_for_resume']}")
#
#     if args['save_every_n_epochs']:
#         output.append(f"--save_every_n_epochs={args['save_every_n_epochs']}")
#     else:
#         output.append("--save_every_n_epochs=999999")
#
#     if args['shuffle_captions']:
#         output.append("--shuffle_caption")
#
#     if args['keep_tokens'] and args['keep_tokens'] > 0:
#         output.append(f"--keep_tokens={args['keep_tokens']}")
#
#     if args['buckets']:
#         output.append("--enable_bucket")
#         output.append(f"--min_bucket_reso={args['min_bucket_resolution']}")
#         output.append(f"--max_bucket_reso={args['max_bucket_resolution']}")
#
#     if args['use_8bit_adam']:
#         output.append("--use_8bit_adam")
#
#     if not args['use_8bit_adam'] and args['use_lion']:
#         output.append("--use_lion_optimizer")
#
#     if args['xformers']:
#         output.append("--xformers")
#
#     if args['color_aug']:
#         if args['cache_latents']:
#             print("color_aug and cache_latents conflict with one another. Please select only one")
#             quit(1)
#         output.append("--color_aug")
#
#     if args['flip_aug']:
#         output.append("--flip_aug")
#
#     if args['cache_latents']:
#         output.append("--cache_latents")
#
#     if args['warmup_lr_ratio'] and args['warmup_lr_ratio'] > 0:
#         warmup_steps = int(steps * args['warmup_lr_ratio'])
#         output.append(f"--lr_warmup_steps={warmup_steps}")
#
#     if args['gradient_checkpointing']:
#         output.append("--gradient_checkpointing")
#
#     if args['gradient_acc_steps'] and args['gradient_acc_steps'] > 0 and args['gradient_checkpointing']:
#         output.append(f"--gradient_accumulation_steps={args['gradient_acc_steps']}")
#
#     if args['learning_rate'] and args['learning_rate'] > 0:
#         output.append(f"--learning_rate={args['learning_rate']}")
#
#     if args['text_encoder_lr'] and args['text_encoder_lr'] > 0:
#         output.append(f"--text_encoder_lr={args['text_encoder_lr']}")
#
#     if args['unet_lr'] and args['unet_lr'] > 0:
#         output.append(f"--unet_lr={args['unet_lr']}")
#
#     if args['vae']:
#         output.append(f"--vae={args['vae']}")
#
#     if args['no_meta']:
#         output.append("--no_metadata")
#
#     if args['save_state']:
#         output.append("--save_state")
#
#     if args['load_previous_save_state']:
#         if not ensure_path(args['load_previous_save_state'], "previous_state"):
#             raise FileNotFoundError("Failed to find the save state folder, make sure you have the correct path")
#         output.append(f"--resume={args['load_previous_save_state']}")
#
#     if args['change_output_name']:
#         output.append(f"--output_name={args['change_output_name']}")
#
#     if args['training_comment']:
#         output.append(f"--training_comment={args['training_comment']}")
#
#     if args['cosine_restarts'] and args['scheduler'] == "cosine_with_restarts":
#         output.append(f"--lr_scheduler_num_cycles={args['cosine_restarts']}")
#
#     if args['scheduler_power'] and args['scheduler'] == "polynomial":
#         output.append(f"--lr_scheduler_power={args['scheduler_power']}")
#
#     if args['persistent_workers']:
#         output.append("--persistent_data_loader_workers")
#
#     if args['unet_only']:
#         output.append("--network_train_unet_only")
#
#     if args['text_only'] and not args['unet_only']:
#         output.append("--network_train_text_encoder_only")
#
#     if args["log_dir"]:
#         output.append(f"--logging_dir={args['log_dir']}")
#
#     if args['bucket_reso_steps']:
#         output.append(f"--bucket_reso_steps={args['bucket_reso_steps']}")
#
#     if args['bucket_no_upscale']:
#         output.append("--bucket_no_upscale")
#
#     if args['random_crop'] and not args['cache_latents']:
#         output.append("--random_crop")
#
#     if args['caption_dropout_rate']:
#         output.append(f"--caption_dropout_rate={args['caption_dropout_rate']}")
#
#     if args['caption_dropout_every_n_epochs']:
#         output.append(f"--caption_dropout_every_n_epochs={args['caption_dropout_every_n_epochs']}")
#
#     if args['caption_tag_dropout_rate']:
#         output.append(f"--caption_tag_dropout_rate={args['caption_tag_dropout_rate']}")
#
#     if args['v2']:
#         output.append("--v2")
#
#     if args['v2'] and args['v_parameterization']:
#         output.append("--v_parameterization")
#
#     if args['noise_offset']:
#         output.append(f"--noise_offset={args['noise_offset']}")
#
#     if args['lowram']:
#         output.append(f"--lowram")
#     return output
