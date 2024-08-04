from PySide6 import QtWidgets
import sys

# from main_ui_files.MainUI import MainWidget

# from main_ui_files.QueueUI import QueueWidget

# from main_ui_files.ArgsListUI import ArgsWidget

# from main_ui_files.SubsetListUI import SubsetListWidget

# from main_ui_files.NetworkUI import NetworkWidget

# from main_ui_files.GeneralUI import GeneralWidget

# from main_ui_files.OptimizerUI import OptimizerWidget

# from main_ui_files.SavingUI import SavingWidget

# from main_ui_files.SampleUI import SampleWidget

# from main_ui_files.NoiseOffsetUI import NoiseOffsetWidget

# from main_ui_files.LoggingUI import LoggingWidget

# from main_ui_files.BucketUI import BucketWidget


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    window.setGeometry(
        QtWidgets.QApplication.screens()[0].size().width() / 2
        - (window.geometry().width() / 2),
        QtWidgets.QApplication.screens()[0].size().height() / 2
        - (window.geometry().height() / 2),
        window.geometry().width() + 10,
        750,
    )
    central_widget = QtWidgets.QWidget(window)
    central_widget.setLayout(QtWidgets.QVBoxLayout())
    window.setCentralWidget(central_widget)
    test_widget = MainWidget()

    get_args = QtWidgets.QPushButton()
    get_args.setText("Get Args")
    get_args.clicked.connect(lambda: print(test_widget.get_args))

    save_toml = QtWidgets.QPushButton()
    save_toml.setText("Save Toml")
    save_toml.clicked.connect(lambda: test_widget.save_toml())

    load_toml = QtWidgets.QPushButton()
    load_toml.setText("Load Toml")
    load_toml.clicked.connect(lambda: test_widget.load_toml())

    central_widget.layout().addWidget(test_widget)
    central_widget.layout().addWidget(get_args)
    central_widget.layout().addWidget(save_toml)
    central_widget.layout().addWidget(load_toml)
    window.show()
    app.exec()


def test_load_args(test_widget):
    args = {
        "general_args": {
            "pretrained_model_name_or_path": "F:/ai_stuff/stable_diffusion/AnimeFullFinal.safetensors",
            "mixed_precision": "bf16",
            "seed": 23,
            "max_data_loader_n_workers": 1,
            "persistent_data_loader_workers": True,
            "max_token_length": 225,
            "prior_loss_weight": 1.0,
            "clip_skip": 2,
            "xformers": True,
            "max_train_epochs": 10,
            "gradient_accumulation_steps": 4,
        },
        "network_args": {
            "network_dim": 4,
            "network_alpha": 1.0,
            "min_timestep": 0,
            "max_timestep": 1000,
            "network_dropout": 0.5,
            "network_args": {
                "conv_dim": 16,
                "conv_alpha": 8.0,
                "module_dropout": 0.25,
                "down_lr_weight": [
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                ],
                "mid_lr_weight": 1.0,
                "up_lr_weight": [
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                ],
                "block_dims": [
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                ],
                "block_alphas": [
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                ],
                "conv_block_dims": [
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                    32,
                ],
                "conv_block_alphas": [
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                    16.0,
                ],
            },
        },
        "optimizer_args": {
            "optimizer_type": "AdamW8bit",
            "lr_scheduler": "cosine",
            "learning_rate": 0.0001,
            "max_grad_norm": 1.0,
            "lr_scheduler_type": "LoraEasyCustomOptimizer.CustomOptimizers.CosineAnnealingWarmupRestarts",
            "lr_scheduler_num_cycles": 4,
            "unet_lr": 0.0005,
            "warmup_ratio": 0.1,
            "min_snr_gamma": 8,
            "scale_weight_norms": 5.0,
            "lr_scheduler_args": {"min_lr": 1e-06, "gamma": 0.85},
            "optimizer_args": {"weight_decay": "0.1", "betas": "0.9,0.99"},
        },
        "saving_args": {
            "output_dir": "F:/Desktop/wdas",
            "save_precision": "fp16",
            "save_model_as": "safetensors",
            "output_name": "szcb911",
            "save_every_n_epochs": 2,
            "save_toml": True,
        },
        "noise_args": {"multires_noise_iterations": 6, "multires_noise_discount": 0.3},
    }
    dataset = {
        "general_args": {"resolution": 896, "batch_size": 2},
        "bucket_args": {
            "enable_bucket": True,
            "min_bucket_reso": 256,
            "max_bucket_reso": 1024,
            "bucket_reso_steps": 64,
        },
        "subsets": [
            {
                "num_repeats": 4,
                "caption_extension": ".txt",
                "shuffle_caption": True,
                "random_crop": True,
                "image_dir": "F:/ai_stuff/stable_diffusion/lora_datasets/styles/szcb911",
                "keep_tokens": 0,
                "caption_dropout_rate": 0.04,
                "caption_dropout_every_n_epochs": 0,
                "caption_tag_dropout_rate": 0.0,
            },
            {
                "num_repeats": 4,
                "caption_extension": ".txt",
                "shuffle_caption": True,
                "random_crop": True,
                "image_dir": "F:/ai_stuff/stable_diffusion/lora_datasets/styles/szcb911",
                "keep_tokens": 0,
                "caption_dropout_rate": 0.04,
                "caption_dropout_every_n_epochs": 0,
                "caption_tag_dropout_rate": 0.0,
                "name": "test_12327381923798",
            },
        ],
    }
    test_widget.load_args(args, dataset)


if __name__ == "__main__":
    main()
