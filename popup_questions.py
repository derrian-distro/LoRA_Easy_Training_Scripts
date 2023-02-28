from tkinter import messagebox
from tkinter import simpledialog

import popup_modules


def ask_starter_questions(args: dict) -> int:
    ret = messagebox.askyesno(message="Do you want to run multiple trainings?\n"
                                      "Keep in mind that this will prevent any more popups\n"
                                      "as it will load according to the json files input")
    if ret:
        args['multi_run_folder'] = popup_modules.ask_dir("Select the folder you have all of your json files in.")
        return 0
    else:
        args['multi_run_folder'] = None

    ret = messagebox.askyesno(message="Do you want to load a json file?\n"
                                      "Keep in mind that this will prevent any more popups")
    if ret:
        args['load_json_path'] = popup_modules.ask_file("Select the json file you want to load", ["json"])
        return 1
    else:
        args['load_json_path'] = None

    ret = messagebox.askyesno(message="Do you want to save a json of your configuration?")
    if ret:
        args['save_json_folder'] = popup_modules.ask_dir("Select the folder to save json files to",
                                                         args['save_json_folder'])
    else:
        args['save_json_folder'] = None

    if args['save_json_folder']:
        ret = simpledialog.askstring(title="Json Name", prompt="What name do you want to set for the json file?\n"
                                                               "Cancel will retain old saving style")
        if ret:
            args['save_json_name'] = ret
        else:
            args['save_json_name'] = None

    if args['save_json_folder']:
        ret = messagebox.askyesno(message="Do you want to only save a json file and not train?\n"
                                          "(this is good for setting up training for the queue system)")
        if ret:
            args['save_json_only'] = True
    return 2


def ask_all_questions(args: dict) -> None:
    args['base_model'] = popup_modules.ask_file("Select your base model", {"ckpt", "safetensors"}, args['base_model'])
    args['img_folder'] = popup_modules.ask_dir("Select your image folder", args['img_folder'])
    args['output_folder'] = popup_modules.ask_dir("Select your output folder", args['output_folder'])

    ret = messagebox.askyesno(message="Do you want to change the name of output checkpoints?")
    if ret:
        ret = simpledialog.askstring(title="output_name", prompt="What do you want your output name to be?\n"
                                                                 "Cancel keeps outputs the original")
        if ret:
            args['change_output_name'] = ret
        else:
            args['change_output_name'] = None

    ret = messagebox.askyesno(message="Do you want to save a txt file that contains a list\n"
                              "of all tags that you have used in your training data?\n")
    if ret:
        args['tag_occurrence_txt_file'] = True
        button = popup_modules.ButtonBox("How do you want tags to be ordered?", ["alphabetically", "occurrence-ly"])
        if button.current_value == "alphabetically":
            args['sort_tag_occurrence_alphabetically'] = True

    ret = messagebox.askyesno(message="Are you training on a SD2.x based model?")
    if ret:
        args['v2'] = True

    if args['v2']:
        ret = messagebox.askyesno(message="Are you training on a model based on the 768x version of SD2?")
        if ret:
            args['v_parameterization'] = True

    ret = messagebox.askyesno(message="Are you training on an realistic model?")
    if ret:
        args['clip_skip'] = 1

    ret = messagebox.askyesno(message="Do you want to use regularization images?")
    if ret:
        args['reg_img_folder'] = popup_modules.ask_dir("Select your regularization folder", args['reg_img_folder'])
    else:
        args['reg_img_folder'] = None

    button = popup_modules.ButtonBox("Which Optimizer do you want? The default optimizer is AdamW",
                                     ["AdamW", "AdamW8bit", "Lion", "SGDNesterov", "SGDNesterov8bit", "DAdaptation",
                                      "AdaFactor"])
    if button.current_value != "":
        args['optimizer_type'] = button.current_value
        if args['optimizer_type'] == "DAdaptation":
            args['optimizer_args']["decouple"] = "True"
    else:
        args['optimizer_type'] = "AdamW"

    ret = simpledialog.askinteger(title="network_dim", prompt="What is the dim size you want to use?\n"
                                                              "Cancel will default to 32")
    if ret is None:
        args['net_dim'] = 32
    else:
        args['net_dim'] = ret

    ret = simpledialog.askfloat(title="alpha", prompt="Alpha is the scalar of the training, generally a good starting\n"
                                                      "point is 0.5x dim size. What Alpha do you want?\n"
                                                      "Cancel will default to equal to 0.5 x network_dim")
    if ret is None:
        args['alpha'] = args['net_dim'] / 2
    else:
        args['alpha'] = ret

    if args['optimizer_type'] == "DAdaptation":
        ret = simpledialog.askfloat(title="learning_rate", prompt="What learning rate do you want to use?\n"
                                                                  "Cancel will default to 1.0\nIt is recommended that"
                                                                  " you use a value close to 1")
        if ret is None:
            args['learning_rate'] = 1.0
        else:
            args['learning_rate'] = ret
    else:
        ret = simpledialog.askfloat(title="learning_rate", prompt="What learning rate do you want to use?\n"
                                                                  "Cancel will default to 1e-4")
        if ret is None:
            args['learning_rate'] = 1e-4
        else:
            args['learning_rate'] = ret

    if args['optimizer_type'] == "DAdaptation":
        ret = simpledialog.askfloat(title="unet_lr", prompt="What unet_lr do you want to use?\n"
                                                            "Cancel will default to 1.0\nIt is recommended that"
                                                            " you use a value close to 1")
        if ret is None:
            args['unet_lr'] = 1.0
        else:
            args['unet_lr'] = ret
    else:
        ret = simpledialog.askfloat(title="unet_lr", prompt="What unet_lr do you want to use?\n"
                                                            "Cancel will default to None")
        if ret is None:
            args['unet_lr'] = None
        else:
            args['unet_lr'] = ret

    if args['optimizer_type'] == "DAdaptation":
        ret = simpledialog.askfloat(title="text_encoder_lr", prompt="What text_encoder_lr do you want to use?\n"
                                                                    "Cancel will default to 1.0\nIt is recommended that"
                                                                    "you use a value close to 1")
        if ret is None:
            args['text_encoder_lr'] = 1.0
        else:
            args['text_encoder_lr'] = ret
    else:
        ret = simpledialog.askfloat(title="text_encoder_lr", prompt="What text_encoder_lr do you want to use?\n"
                                                                    "Cancel will default to None")
        if ret is None:
            args['text_encoder_lr'] = None
        else:
            args['text_encoder_lr'] = ret

    button = popup_modules.ButtonBox("Which scheduler do you want?", ["cosine_with_restarts", "cosine", "polynomial",
                                                                      "constant", "constant_with_warmup", "linear"])
    args['scheduler'] = button.current_value if button.current_value != "" else "cosine_with_restarts"

    if args['scheduler'] == "cosine_with_restarts":
        ret = simpledialog.askinteger(title="Cycle Count",
                                      prompt="How many times do you want cosine to restart?\nThis is the entire "
                                             "amount of times it will restart for the entire training\n"
                                             "Cancel will default to 1")
        if ret is None:
            args['cosine_restarts'] = 1
        else:
            args['cosine_restarts'] = ret

    if args['scheduler'] == "polynomial":
        ret = simpledialog.askfloat(title="Poly Strength",
                                    prompt="What power do you want to set your polynomial to?\nhigher power means "
                                           "that the model reduces the learning more more aggressively from initial "
                                           "training.\n1 = linear\nCancel sets to 1")
        if ret is None:
            args['scheduler_power'] = 1
        else:
            args['scheduler_power'] = ret

    ret = simpledialog.askinteger(title="resolution", prompt="How large of a resolution do you want to train at?\n"
                                                             "Cancel will default to 512")
    if ret is None:
        args['train_resolution'] = 512
    else:
        args['train_resolution'] = ret

    ret = simpledialog.askinteger(title="batch_size",
                                  prompt="The number of images that get processed at one time, this is directly "
                                         "proportional to your vram and resolution. with 12gb of vram, at 512 reso, "
                                         "you can get a maximum of 6 batch size\nHow large is your batch size going to "
                                         "be?\nCancel will default to 1")
    if ret is None:
        args['batch_size'] = 1
    else:
        args['batch_size'] = ret

    button = popup_modules.ButtonBox("Which way do you want to manage steps?\nCancel will default to epochs",
                                     ["epochs", "steps"])
    if button.current_value in {"", "epochs"}:
        ret = simpledialog.askinteger(title="num_epochs", prompt="How many epochs do you want?\n"
                                                                 "Cancel will default to 1")
        if ret is None:
            args['num_epochs'] = 1
        else:
            args['num_epochs'] = ret
    else:
        ret = simpledialog.askinteger(title="Num Steps", prompt="How many steps do you want to set\n"
                                                                "this will decide how many epochs you have\n"
                                                                "and will stop exactly at the step set.\n"
                                                                "Default is 1600 (default set by sd_scripts")
        if ret is None:
            args['max_steps'] = 1600
        else:
            args['max_steps'] = ret

    ret = messagebox.askyesno(message="Do you want to save epochs as it trains?")
    if ret:
        ret = simpledialog.askinteger(title="save_epoch",
                                      prompt="How often do you want to save epochs?\nCancel will default to 1")
        if ret is None:
            args['save_every_n_epochs'] = 1
        else:
            args['save_every_n_epochs'] = ret

    ret = messagebox.askyesno(message="Do you want to have a warmup ratio?")
    if ret:
        ret = simpledialog.askfloat(title="warmup_ratio", prompt="What is the ratio of steps to use as warmup "
                                                                 "steps?\nCancel will default to None")
        if ret is None:
            args['warmup_lr_ratio'] = None
        else:
            args['warmup_lr_ratio'] = ret

    ret = messagebox.askyesno(message="Do you want to shuffle captions?")
    if ret:
        args['shuffle_captions'] = True
    else:
        args['shuffle_captions'] = False

    ret = messagebox.askyesno(message="Do you want to keep some tokens at the front of your captions?")
    if ret:
        ret = simpledialog.askinteger(title="keep_tokens", prompt="How many do you want to keep at the front?"
                                                                  "\nCancel will default to 1")
        if ret is None:
            args['keep_tokens'] = 1
        else:
            args['keep_tokens'] = ret

    button = popup_modules.ButtonBox("Select what elements you want to train.\nCancel will default to both",
                                     ["both", "unet_only", "text_only"])
    if button.current_value not in {'both', ""}:
        if button.current_value == "unet_only":
            args['unet_only'] = True
        else:
            args['text_only'] = True

    ret = messagebox.askyesno(message="Do you want to flip all of your images? It is supposed to reduce biases\n"
                                      "within your dataset but it can also ruin learning an asymmetrical element\n")
    if ret:
        args['flip_aug'] = True

    ret = simpledialog.askstring(title="comment", prompt="Do you want to set a comment that gets put into the metadata?"
                                                         "\nA good use of this would be to include how to use, such as "
                                                         "activation keywords.\nCancel will leave empty")
    if ret is not None:
        args['training_comment'] = ret
    else:
        args['training_comment'] = None

    ret = messagebox.askyesno(message="Do you want to prevent upscaling images?")
    if ret:
        args['bucket_no_upscale'] = True

    button = popup_modules.ButtonBox("What Mixed precision do you want?\nCancel will default to fp16",
                                     ["fp16", "bf16", "no"])
    if button.current_value in {""}:
        args['mixed_precision'] = "fp16"
    else:
        args['mixed_precision'] = button.current_value

    button = popup_modules.ButtonBox("What save precision do you want?\nCancel will default to fp16",
                                     ["float", "fp16", "bf16"])
    if button.current_value in {""}:
        args['save_precision'] = "fp16"
    else:
        args['save_precision'] = button.current_value

    button = popup_modules.ButtonBox("Which of random crop or cache latents do you want? "
                                     "cache latents don't work with random crop.\n"
                                     "Cancel will enable cache latents", ["cache latents", "random crop"])
    if button.current_value in {"", "cache latents"}:
        args['cache_latents'] = True
        args['random_crop'] = False
    else:
        args['cache_latents'] = False
        args['random_crop'] = True
