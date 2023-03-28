"""
    Main Class for storing every argument
    Arguments will be split up in terms of what they are,
    and within that group, will be ordered in terms of usefulness
    some arguments are one offs, they will be placed in order in terms of usefulness
    some args are practically useless, so they will be at the very bottom of the list,
    even if they are linked to other elements
"""
import os
from typing import Union


class ArgStore:
    def __init__(self):
        # path args, make sure to use r"" when setting them. That will allow you to not have \\
        self.base_model: str = r""
        self.img_folder: str = r""
        self.output_folder: str = r""
        self.save_json_folder: Union[str, None] = None
        self.save_json_name: Union[str, None] = None
        self.load_json_path: Union[str, None] = None
        self.multi_run_folder: Union[str, None] = None
        self.reg_img_folder: Union[str, None] = None
        self.sample_prompts: Union[str, None] = None  # path to a txt file that has all of the sample prompts in it,
        # one per line. Only goes to 75 tokens, will cut off the rest. Just place the prompts into the txt file per line
        # and it will gen using those prompts
        self.change_output_name: Union[str, None] = None
        self.json_load_skip_list: Union[list[str], None] = None  # OPTIONAL, allows the user to define what they skip
        # when loading a json, IMPORTANT: by default it loads
        # everything, including all paths, format to exclude
        # things is like so: ["base_model", "img_folder", "output_folder"]
        self.training_comment: Union[str, None] = None  # OPTIONAL, great way to put in things like activation tokens
        self.save_json_only: bool = False  # set to true if you don't want to do any training, but rather just want to
        # generate a json
        self.tag_occurrence_txt_file: bool = True  # OPTIONAL, creates a txt file that has the entire occurrence of all
        # tags in your dataset will automatically output to the same folder
        # as your output checkpoints
        self.sort_tag_occurrence_alphabetically: bool = False  # OPTIONAL, only applies if tag_occurrence_txt_file
        # is also true Will change the output to be alphabetically
        # vs being occurrence based

        # Optimizer args
        self.optimizer_type: str = "AdamW8bit"  # options are AdamW, AdamW8bit, Lion, SGDNesterov,
        # SGDNesterov8bit, DAdaptation, AdaFactor

        # this is where you add things like weight_decay
        # the values set here are the default I recommend when using AdamW or AdamW8bit
        self.optimizer_args: Union[dict[str:str], None] = {"weight_decay": "0.1",
                                                           "betas": "0.9,0.99"}  # List of optional elements that can be used for an optimizer

        # scheduler args
        # list of schedulers: linear, cosine, cosine_with_restarts, polynomial, constant, constant_with_warmup
        self.scheduler: str = "cosine"
        self.cosine_restarts: Union[int, None] = 1  # OPTIONAL, represents the number of times it restarts.
        # Only matters if you are using cosine_with_restarts
        self.scheduler_power: Union[float, None] = 1  # OPTIONAL, represents the power of the polynomial.
        # Only matters if you are using polynomial
        self.lr_scheduler_type: Union[str, None] = None  # The variable to specify a custom scheduler
        self.lr_scheduler_args: Union[dict[str:str], None] = None  # The args to go with that custom scheduler

        # learning rate args
        self.learning_rate: Union[float, None] = 1e-4  # AdamW does not require this, some other optimizers do.
        self.unet_lr: Union[float, None] = None  # OPTIONAL, Sets a specific lr for the unet, this overwrites
        # the base lr in AdamW
        self.text_encoder_lr: Union[float, None] = None  # OPTIONAL, Sets a specific lr for the text encoder,
        # this overwrites the base lr in AdamW
        self.warmup_lr_ratio: Union[float, None] = None  # OPTIONAL, Calculates the number of warmup steps based on the
        # ratio given. Make sure to set this if you are using
        # constant_with_warmup, None to ignore
        self.unet_only: bool = False  # OPTIONAL, set it to only train the unet

        # general required arguments
        self.net_dim: int = 32  # network dimension, 32 is default, but some people train at higher dims
        self.alpha: float = 16  # represents the scalar for training. default is half of dim.
        # if you want the older way of training, set this to dim
        self.train_resolution: int = 512
        self.height_resolution: Union[int, None] = None  # for if you want to train in a non-square resolution
        self.batch_size: int = 1  # The number of images that get processed at one time, this is directly proportional
        # to your vram and resolution. with 12gb of vram, at 512 reso,
        # you can get a maximum of 6 batch size
        self.clip_skip: int = 2  # If you are training on a model that is anime based,
        # keep this at 2 as most models are designed for that
        self.test_seed: int = 23  # this is the "reproducable seed", basically if you set the seed to this,
        # you should be able to input a prompt from one of your training images and
        # get a close representation of it
        self.mixed_precision: str = "fp16"  # If you have the ability to use bf16, do it, it's better
        self.save_precision: str = "fp16"  # You can also save in bf16, but because it's not universally supported,
        # I suggest you keep saving at fp16

        # network arguments
        self.lyco: bool = False  # turn on if you want to use the new locon architecture

        # valid args change slightly depending on what mode you are using
        # if you are using the new lyco setup, then you have access to conv_dim, conv_alpha, dropout, and algo
        # dropout is for locon only right now, but I don't believe setting it will cause things to break
        # algo can either be lora (which is locon) or loha (the new algo that was just released)
        # if you aren't then you have access to conv_dim, and conv_alpha as Kohya has implemented it themselves
        self.network_args: Union[dict[str:str], None] = None

        # steps args
        self.num_epochs: int = 1  # The number of epochs, if you set max steps this value is
        # ignored as it doesn't calculate steps.
        self.save_every_n_epochs: Union[int, None] = None  # OPTIONAL, how often to save epochs, None to ignore
        self.save_n_epoch_ratio: Union[int, None] = None  # OPTIONAL, how many epochs to save, will try and save epochs
        # as evenly split as possible. overrides save_every_n_epochs
        self.save_last_n_epochs: Union[int, None] = None  # only save the last n epochs, is overwritten by the above two
        self.max_steps: Union[int, None] = None  # OPTIONAL, if you have specific steps you want to hit,
        # this allows you to set it directly. None to ignore

        # sample args
        # list of samplers to choose from:
        # 'ddim', 'pndm', 'lms', 'euler', 'euler_a', 'heun', 'dpm_2', 'dpm_2_a', 'dpmsolver', 'dpmsolver++',
        # 'dpmsingle', 'k_lms', 'k_euler', 'k_euler_a', 'k_dpm_2', 'k_dpm_2_a'
        self.sample_sampler: Union[str, None] = None  # what sampler to use for generating an image while training,
        # defaults to ddim
        self.sample_every_n_steps: Union[int, None] = None  # generates a sample image while training every n steps
        self.sample_every_n_epochs: Union[int, None] = None  # generate a sample image while training every n epochs,
        # overrides steps

        # bucket args
        self.buckets: bool = True
        self.min_bucket_resolution: int = 320
        self.max_bucket_resolution: int = 960
        self.bucket_reso_steps: Union[int, None] = None  # is the steps that is taken when making buckets, can be any
        # can be any positive value from 1 up
        self.bucket_no_upscale: bool = False  # Disables up-scaling for images in buckets

        # tag args
        self.shuffle_captions: bool = False  # OPTIONAL, False to ignore
        self.keep_tokens: Union[int, None] = None  # OPTIONAL, None to ignore
        self.token_warmup_step: Union[float, None] = None  # OPTIONAL, is the amount of steps before
        # all tokens get used in training
        self.token_warmup_min: Union[int, None] = None  # OPTIONAL, is the smallest amount of tokens used in tag warmup

        # other somewhat useful args
        self.xformers: bool = True
        self.cache_latents: bool = True
        self.flip_aug: bool = False
        self.v2: bool = False  # Sets up training for SD2.1
        self.v_parameterization: bool = False  # Only is used when v2 is also set and you are using the 768x version of v2
        self.gradient_checkpointing: bool = False  # OPTIONAL, enables gradient checkpointing
        self.gradient_acc_steps: Union[int, None] = None  # OPTIONAL, not sure exactly what this means
        self.noise_offset: Union[float, None] = None  # OPTIONAL, seems to help allow SD to gen better blacks and whites
        # Kohya recommends, if you have it set, to use 0.1, not sure how
        # high the value can be, I'm going to assume maximum of 1
        # seems to cause baking in outputs with two LoRA using noise offset
        self.mem_eff_attn: bool = False
        self.min_snr_gamma: Union[float, None] = None  # A new method of training that supposedly improves results,
        # recommended value is 5

        # practically useless arguments
        self.lora_model_for_resume: Union[str, None] = None  # LoRA train fast enough to not need this
        self.save_state: bool = False  # LoRA train fast enough to not need this
        self.resume: Union[str, None] = None
        self.text_only: bool = False  # Haven't seen a soul use this, unet_only does get used a bit though
        self.vae: Union[str, None] = None  # Generally messes up outputs, avoid using
        self.log_dir: Union[str, None] = None  # Only useful if you wanted to see the LR and other training details
        self.log_prefix: Union[str, None] = None  # adds a prefix to the logging output to make it easier to find
        self.tokenizer_cache_dir: Union[str, None] = None  # Doesn't seem to help in a majority of cases
        self.dataset_config: Union[str, None] = None  # I haven't implemented a system to convert the json to toml yet.
        # I'll make the toml the default once I can reliably create them and convert from my already existing json files
        self.lowram: bool = False  # Is mainly meant for people using colab, which don't use my scripts
        self.no_meta: bool = False  # Is only detrimental to preserving data
        self.color_aug: bool = False  # requires cache latents to be off
        self.random_crop: bool = False  # requires cache latents to be off
        self.use_8bit_adam: bool = False  # deprecated
        self.use_lion: bool = False  # deprecated
        self.caption_dropout_rate: Union[float, None] = None  # has seen no use
        self.caption_dropout_every_n_epochs: Union[int, None] = None  # has seen no use
        self.caption_tag_dropout_rate: Union[float, None] = None  # has seen no use
        self.prior_loss_weight: float = 1  # should keep this value at 1
        self.max_grad_norm: float = 1  # should keep this value at 1
        self.save_as: str = "safetensors"  # should keep this value as safetensors
        self.caption_extension: str = ".txt"  # should keep this as .txt unless for some reason you use .caption files
        self.max_clip_token_length: Union[int, None] = 150  # you will never really have prompts within the txt files to exceed this
        self.save_last_n_epochs_state: Union[int, None] = None  # can't see any use in it.
        self.num_workers: int = 1  # The number of threads that are being used to load images, lower speeds up
        # the start of epochs, but slows down the loading of data. The assumption here is
        # that it increases the training time as you reduce this value
        self.persistent_workers: bool = True  # makes workers persistent, further reduces/eliminates the lag in between
        # epochs. however it may increase memory usage
        self.face_crop_aug_range: Union[str, None] = None
        self.network_module: str = 'sd_scripts.networks.lora'
        self.locon_dim: Union[int, None] = None  # deprecated
        self.locon_alpha: Union[int, None] = None  # deprecated
        self.locon: bool = False  # deprecated

    # Creates the dict that is used for the rest of the code, to facilitate easier json saving and loading
    @staticmethod
    def convert_args_to_dict():
        return ArgStore().__dict__

    @staticmethod
    def change_dict_to_internal_names(dic: dict):
        internal_names = {'base_model': 'pretrained_model_name_or_path', 'img_folder': 'train_data_dir',
                          'shuffle_captions': 'shuffle_caption', 'train_resolution': 'resolution',
                          'buckets': 'enable_bucket', 'min_bucket_resolution': 'min_bucket_reso',
                          'max_bucket_resolution': 'max_bucket_reso', 'reg_img_folder': 'reg_data_dir',
                          'output_folder': 'output_dir', 'change_output_name': 'output_name',
                          'batch_size': 'train_batch_size', 'max_clip_token_length': 'max_token_length',
                          'max_steps': 'max_train_steps', 'num_epochs': 'max_train_epochs',
                          'num_workers': 'max_data_loader_n_workers',
                          'persistent_workers': 'persistent_data_loader_workers',
                          'test_seed': 'seed', 'gradient_acc_steps': 'gradient_accumulation_steps',
                          'log_dir': 'logging_dir', 'use_lion': 'use_lion_optimizer', 'scheduler': 'lr_scheduler',
                          'cosine_restarts': 'lr_scheduler_num_cycles', 'scheduler_power': 'lr_scheduler_power',
                          'no_meta': 'no_metadata', 'save_as': 'save_model_as',
                          'lora_model_for_resume': 'network_weights', 'net_dim': 'network_dim',
                          'alpha': 'network_alpha', 'unet_only': 'network_train_unet_only',
                          'text_only': 'network_train_text_encoder_only'}

        if 'warmup_lr_ratio' in dic and dic['warmup_lr_ratio'] is not None:
            steps = find_max_steps(dic) if not dic['max_steps'] else dic['max_steps']
            dic['lr_warmup_steps'] = int(steps * dic['warmup_lr_ratio'])

        for key, val in internal_names.items():
            if key in dic:
                dic[val] = dic[key]
                dic.pop(key)

        return dic


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
