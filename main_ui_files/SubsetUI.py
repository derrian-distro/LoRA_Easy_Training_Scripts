import contextlib
from pathlib import Path
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QFileDialog
from PySide6.QtCore import Signal
from modules.BaseWidget import BaseWidget
from modules.DragDropLineEdit import DragDropLineEdit
from ui_files.sub_dataset_input import Ui_sub_dataset_input
from ui_files.sub_dataset_extra_input import Ui_sub_dataset_extra_input


class SubsetWidget(BaseWidget):
    edited = Signal(dict, str)

    def __init__(
        self, parent: QWidget = None, display_name: str = "", name: str = ""
    ) -> None:
        super().__init__(parent)
        self.colap.set_title(display_name)
        self.colap.set_extra("remove")
        self.widget = Ui_sub_dataset_input()
        self.extra_content = QWidget()
        self.extra_widget = Ui_sub_dataset_extra_input()
        self.name = name

        self.dataset_args = {
            "num_repeats": 1,
            "caption_extension": ".txt",
            "name": self.name,
        }

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)
        self.widget.extra_args.add_widget(self.extra_content, "main_widget")
        self.extra_widget.setupUi(self.extra_content)
        self.widget.extra_args.set_title("Optional Args")
        self.widget.image_folder_input.setMode("folder")
        self.widget.image_folder_input.highlight = True
        self.widget.image_folder_selector.setIcon(
            QIcon(str(Path("icons/more-horizontal.svg")))
        )
        self.extra_widget.face_crop_group.setChecked(False)
        self.extra_widget.caption_dropout_group.setChecked(False)
        self.extra_widget.token_warmup_group.setChecked(False)

    def setup_connections(self) -> None:
        self.widget.image_folder_input.textChanged.connect(
            lambda x: self.edit_dataset_args("image_dir", x, optional=True)
        )
        self.widget.image_folder_input.editingFinished.connect(
            lambda: self.check_validity(self.widget.image_folder_input)
        )
        self.widget.image_folder_selector.clicked.connect(
            lambda: self.set_folder_from_dialog("Subset Image Folder")
        )
        self.widget.repeats_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("num_repeats", x)
        )
        self.widget.shuffle_captions_enable.clicked.connect(
            lambda x: self.edit_dataset_args("shuffle_caption", x, True)
        )
        self.widget.flip_augment_enable.clicked.connect(
            lambda x: self.edit_dataset_args("flip_aug", x, True)
        )
        self.widget.keep_tokens_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("keep_tokens", x, True)
        )
        self.widget.color_augment_enable.clicked.connect(
            lambda x: self.edit_dataset_args("color_aug", x, True)
        )
        self.widget.random_crop_enable.clicked.connect(
            lambda x: self.edit_dataset_args("random_crop", x, True)
        )
        self.widget.caption_extension_selector.currentTextChanged.connect(
            lambda x: self.edit_dataset_args("caption_extension", x)
        )
        self.widget.regularization_images_enable.clicked.connect(
            lambda x: self.edit_dataset_args("is_reg", x, True)
        )
        self.extra_widget.face_crop_group.clicked.connect(self.enable_disable_face_crop)
        self.extra_widget.face_crop_width_input.valueChanged.connect(
            lambda: self.enable_disable_face_crop(True)
        )
        self.extra_widget.face_crop_height_input.valueChanged.connect(
            lambda: self.enable_disable_face_crop(True)
        )
        self.extra_widget.caption_dropout_group.clicked.connect(
            self.enable_disable_caption_dropout
        )
        self.extra_widget.caption_dropout_rate_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("caption_dropout_rate", x, True)
        )
        self.extra_widget.caption_epoch_dropout_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("caption_dropout_every_n_epochs", x, True)
        )
        self.extra_widget.caption_tag_dropout_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("caption_tag_dropout_rate", x, True)
        )
        self.extra_widget.token_warmup_group.clicked.connect(
            self.enable_disable_token_warmup
        )
        self.extra_widget.token_minimum_warmup_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("token_warmup_min", x)
        )
        self.extra_widget.token_warmup_step_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("token_warmup_step", x)
        )

    def check_validity(self, elem: DragDropLineEdit) -> None:
        elem.dirty = True
        if not elem.allow_empty or elem.text() != "":
            elem.update_stylesheet()
        else:
            elem.setStyleSheet("")

    def edit_dataset_args(
        self, name: str, value: object, optional: bool = False
    ) -> None:
        super().edit_dataset_args(name, value, optional)
        self.edited.emit(self.dataset_args, self.name)

    def set_folder_from_dialog(self, title_str: str = "", path: Path = None) -> None:
        if path and path.exists():
            file_name = path
        else:
            default_dir = Path(self.widget.image_folder_input.text())
            file_name = QFileDialog.getExistingDirectory(
                self,
                title_str,
                dir=str(default_dir) if default_dir.exists() else "",
            )
            if not file_name:
                return
            file_name = Path(file_name)
        with contextlib.suppress(ValueError):
            repeats = int(file_name.name.split("_")[0])
            self.widget.repeats_input.setValue(repeats)
        self.widget.image_folder_input.setText(file_name.as_posix())
        self.widget.image_folder_input.update_stylesheet()

    def enable_disable_face_crop(self, checked: bool) -> None:
        if "face_crop_aug_range" in self.dataset_args:
            del self.dataset_args["face_crop_aug_range"]
        if not checked:
            return
        self.edit_dataset_args(
            "face_crop_aug_range",
            [
                self.extra_widget.face_crop_width_input.value(),
                self.extra_widget.face_crop_height_input.value(),
            ],
        )

    def enable_disable_caption_dropout(self, checked: bool) -> None:
        args = [
            "caption_dropout_rate",
            "caption_dropout_every_n_epochs",
            "caption_tag_dropout_rate",
        ]
        for arg in args:
            if arg in self.dataset_args:
                del self.dataset_args[arg]
        if not checked:
            return
        self.edit_dataset_args(
            args[0], self.extra_widget.caption_dropout_rate_input.value(), True
        )
        self.edit_dataset_args(
            args[1], self.extra_widget.caption_epoch_dropout_input.value(), True
        )
        self.edit_dataset_args(
            args[2], self.extra_widget.caption_tag_dropout_input.value(), True
        )

    def enable_disable_token_warmup(self, checked: bool) -> None:
        args = ["token_warmup_min", "token_warmup_step"]
        for arg in args:
            if arg in self.dataset_args:
                del self.dataset_args[arg]
        if not checked:
            return
        self.edit_dataset_args(
            args[0], self.extra_widget.token_minimum_warmup_input.value()
        )
        self.edit_dataset_args(
            args[1], self.extra_widget.token_warmup_step_input.value()
        )

    def enable_disable_cache_dependants(self, checked: bool) -> None:
        self.widget.color_augment_enable.setEnabled(not checked)
        self.widget.random_crop_enable.setEnabled(not checked)
        for arg in ["color_aug", "random_crop"]:
            if arg in self.dataset_args:
                del self.dataset_args[arg]
        self.edit_dataset_args(
            "color_aug",
            False if checked else self.widget.color_augment_enable.isChecked(),
            True,
        )
        self.edit_dataset_args(
            "random_crop",
            False if checked else self.widget.random_crop_enable.isChecked(),
            True,
        )

    def enable_disable_keep_tokens(self, checked: bool) -> None:
        self.widget.keep_tokens_input.setEnabled(not checked)
        if "keep_tokens" in self.dataset_args:
            del self.dataset_args["keep_tokens"]
        self.edit_dataset_args(
            "keep_tokens",
            False if checked else self.widget.keep_tokens_input.value(),
            True,
        )

    def load_dataset_args(self, dataset_args: dict) -> bool:
        # update element inputs
        self.widget.image_folder_input.setText(dataset_args.get("image_dir", ""))
        self.widget.repeats_input.setValue(dataset_args.get("num_repeats", 1))
        self.widget.shuffle_captions_enable.setChecked(
            dataset_args.get("shuffle_caption", False)
        )
        self.widget.flip_augment_enable.setChecked(dataset_args.get("flip_aug", False))
        self.widget.keep_tokens_input.setValue(dataset_args.get("keep_tokens", 0))
        self.widget.color_augment_enable.setChecked(
            dataset_args.get("color_aug", False)
        )
        self.widget.random_crop_enable.setChecked(
            dataset_args.get("random_crop", False)
        )
        self.widget.caption_extension_selector.setCurrentText(
            dataset_args.get("caption_extension", ".txt")
        )
        self.widget.regularization_images_enable.setChecked(
            dataset_args.get("is_reg", False)
        )
        self.extra_widget.face_crop_group.setChecked(
            bool(dataset_args.get("face_crop_aug_range", False))
        )
        self.extra_widget.face_crop_width_input.setValue(
            dataset_args.get("face_crop_aug_range", [1.0, 1.0])[0]
        )
        self.extra_widget.face_crop_height_input.setValue(
            dataset_args.get("face_crop_aug_range", [1.0, 1.0])[1]
        )
        self.extra_widget.caption_dropout_group.setChecked(
            any(
                arg in dataset_args
                for arg in [
                    "caption_dropout_rate",
                    "caption_dropout_every_n_epochs",
                    "caption_tag_dropout_rate",
                ]
            )
        )
        self.extra_widget.caption_dropout_rate_input.setValue(
            dataset_args.get("caption_dropout_rate", 0.0)
        )
        self.extra_widget.caption_epoch_dropout_input.setValue(
            dataset_args.get("caption_dropout_every_n_epochs", 0)
        )
        self.extra_widget.caption_tag_dropout_input.setValue(
            dataset_args.get("caption_tag_dropout_rate", 0.0)
        )
        self.extra_widget.token_warmup_group.setChecked(
            any(
                arg in dataset_args for arg in ["token_warmup_step", "token_warmup_min"]
            )
        )
        self.extra_widget.token_minimum_warmup_input.setValue(
            dataset_args.get("token_warmup_min", 1)
        )
        self.extra_widget.token_warmup_step_input.setValue(
            dataset_args.get("token_warmup_step", 1)
        )

        # edit dataset args to match
        self.edit_dataset_args("image_dir", self.widget.image_folder_input.text(), True)
        self.edit_dataset_args("num_repeats", self.widget.repeats_input.value())
        self.edit_dataset_args(
            "shuffle_caption", self.widget.shuffle_captions_enable.isChecked(), True
        )
        self.edit_dataset_args(
            "flip_aug", self.widget.flip_augment_enable.isChecked(), True
        )
        self.edit_dataset_args(
            "keep_tokens", self.widget.keep_tokens_input.value(), True
        )
        self.edit_dataset_args(
            "color_aug", self.widget.color_augment_enable.isChecked(), True
        )
        self.edit_dataset_args(
            "random_crop", self.widget.random_crop_enable.isChecked(), True
        )
        self.edit_dataset_args(
            "caption_extension", self.widget.caption_extension_selector.currentText()
        )
        self.edit_dataset_args(
            "is_reg", self.widget.regularization_images_enable.isChecked(), True
        )
        self.enable_disable_face_crop(self.extra_widget.face_crop_group.isChecked())
        self.enable_disable_caption_dropout(
            self.extra_widget.caption_dropout_group.isChecked()
        )
        self.enable_disable_token_warmup(
            self.extra_widget.token_warmup_group.isChecked()
        )
        self.edited.emit(self.dataset_args, self.name)
