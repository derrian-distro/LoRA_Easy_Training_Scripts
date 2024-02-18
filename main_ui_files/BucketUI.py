from PySide6.QtWidgets import QWidget
from ui_files.BucketUI import Ui_bucket_ui
from modules.BaseWidget import BaseWidget


class BucketWidget(BaseWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.colap.set_title("Bucket Args")
        self.widget = Ui_bucket_ui()

        self.name = "bucket_args"
        self.dataset_args = {
            "enable_bucket": True,
            "min_bucket_reso": 256,
            "max_bucket_reso": 1024,
            "bucket_reso_steps": 64,
        }

        self.setup_widget()
        self.setup_connections()

    def setup_widget(self) -> None:
        super().setup_widget()
        self.widget.setupUi(self.content)

    def setup_connections(self) -> None:
        self.widget.bucket_no_upscale.clicked.connect(
            lambda x: self.edit_dataset_args("bucket_no_upscale", x, True)
        )
        self.widget.min_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("min_bucket_reso", x)
        )
        self.widget.max_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("max_bucket_reso", x)
        )
        self.widget.steps_input.valueChanged.connect(
            lambda x: self.edit_dataset_args("bucket_reso_steps", x)
        )
        self.widget.bucket_group.clicked.connect(self.enable_disable)

    def enable_disable(self, checked: bool) -> None:
        self.dataset_args = {}
        if not checked:
            self.edit_dataset_args("enable_bucket", False)
            return
        self.edit_dataset_args("enable_bucket", True)
        self.edit_dataset_args(
            "bucket_no_upscale", self.widget.bucket_no_upscale.isChecked(), True
        )
        self.edit_dataset_args("min_bucket_reso", self.widget.min_input.value())
        self.edit_dataset_args("max_bucket_reso", self.widget.max_input.value())
        self.edit_dataset_args("bucket_reso_steps", self.widget.steps_input.value())

    def load_dataset_args(self, dataset_args: dict) -> bool:
        if not super().load_dataset_args(dataset_args):
            self.widget.bucket_group.setChecked(False)
            self.edit_dataset_args("enable_bucket", False)
            return False

        dataset_args: dict = dataset_args[self.name]

        # update element inputs
        self.widget.bucket_group.setChecked(dataset_args.get("enable_bucket", False))
        self.widget.bucket_no_upscale.setChecked(
            dataset_args.get("bucket_no_upscale", False)
        )
        self.widget.min_input.setValue(dataset_args.get("min_bucket_reso", 256))
        self.widget.max_input.setValue(dataset_args.get("max_bucket_reso", 1024))
        self.widget.steps_input.setValue(dataset_args.get("bucket_reso_steps", 64))

        # edit dataset_args to match
        self.enable_disable(self.widget.bucket_group.isChecked())
        return True
