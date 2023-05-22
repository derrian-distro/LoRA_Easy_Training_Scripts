from PySide6 import QtWidgets, QtCore
from ui_files.BucketUI import Ui_bucket_ui
from modules.CollapsibleWidget import CollapsibleWidget


class BucketWidget(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super(BucketWidget, self).__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.colap = CollapsibleWidget(self, "Bucket Args")
        self.layout().addWidget(self.colap)
        self.layout().setContentsMargins(9, 0, 9, 0)
        self.content = QtWidgets.QWidget()
        self.colap.add_widget(self.content, "main_widget")

        self.widget = Ui_bucket_ui()
        self.widget.setupUi(self.content)
        self.dataset_args = {"enable_bucket": True, "min_bucket_reso": 256,
                             "max_bucket_reso": 1024, "bucket_reso_steps": 64}
        self.name = "bucket_args"
        self.widget.bucket_no_upscale.clicked.connect(lambda x: self.edit_args("bucket_no_upscale", x, True))
        self.widget.min_input.valueChanged.connect(lambda x: self.edit_args("min_bucket_reso", x))
        self.widget.max_input.valueChanged.connect(lambda x: self.edit_args("max_bucket_reso", x))
        self.widget.steps_input.valueChanged.connect(lambda x: self.edit_args("bucket_reso_steps", x))
        self.widget.bucket_group.clicked.connect(self.enable_disable_buckets)

    @QtCore.Slot(str, object, bool)
    def edit_args(self, name: str, value: object, optional: bool = False):
        if not optional:
            self.dataset_args[name] = value
            return
        if not value or value is False:
            if name in self.dataset_args:
                del self.dataset_args[name]
            return
        self.dataset_args[name] = value

    @QtCore.Slot(bool)
    def enable_disable_buckets(self, checked: bool):
        self.dataset_args["enable_bucket"] = checked

    def get_args(self, input_args: dict):
        pass

    def get_dataset_args(self, input_args: dict):
        if not self.widget.bucket_group.isChecked():
            if "bucket_args" in input_args:
                del input_args['bucket_args']
            return
        input_args['bucket_args'] = self.dataset_args

    def load_args(self, args: dict):
        if self.name not in args:
            return
        args = args[self.name]['dataset_args']
        self.widget.bucket_no_upscale.setChecked(args.get("bucket_no_upscale", False))
        self.widget.min_input.setValue(args.get("min_bucket_reso", 256))
        self.widget.max_input.setValue(args.get("max_bucket_reso", 1024))
        self.widget.steps_input.setValue(args.get("bucket_reso_steps", 64))
        self.enable_disable_buckets(args['enable_bucket'])
        self.widget.bucket_group.setChecked(args['enable_bucket'])

