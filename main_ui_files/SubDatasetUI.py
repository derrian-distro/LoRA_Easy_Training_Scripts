import os.path

from PySide6 import QtWidgets
from PySide6 import QtCore
from main_ui_files.SubsetUI import SubsetWidget
from modules.CollapsibleWidget import CollapsibleWidget
from modules.LineEditHighlight import LineEditWithHighlight


class SubDatasetWidget(QtWidgets.QWidget):
    CacheChecked = QtCore.Signal(bool)

    def __init__(self, parent: QtWidgets.QWidget = None) -> None:
        super(SubDatasetWidget, self).__init__(parent)
        self.setMinimumSize(600, 300)

        self.elements = set()
        self.cache_latents_checked = False

        self.setLayout(QtWidgets.QGridLayout())

        self.layout().setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self.add_button = QtWidgets.QPushButton()
        self.add_button.setText("Add Data Subset")
        self.add_button.clicked.connect(self.add_empty_subset)
        self.add_button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.layout().addWidget(self.add_button, 0, 1, 1, 1)

        self.add_label = LineEditWithHighlight()
        self.add_label.setPlaceholderText("Name of subset")
        self.add_label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Maximum, QtWidgets.QSizePolicy.Policy.Fixed)
        self.layout().addWidget(self.add_label, 0, 0, 1, 1)

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scrollWidget)
        self.layout().addWidget(self.scrollArea, 1, 0, 1, 2)
        self.scrollLayout = QtWidgets.QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setSpacing(0)
        self.scrollLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self.scrollLayout.setContentsMargins(9, 0, 9, 0)

    @QtCore.Slot()
    def add_empty_subset(self, name: str = None) -> SubsetWidget:
        widget = QtWidgets.QWidget(self.scrollArea)
        widget.setLayout(QtWidgets.QHBoxLayout())
        self.scrollWidget.layout().addWidget(widget)

        colap = CollapsibleWidget(widget, title=self.add_label.text() if not name else name, remove_elem=True)
        colap.layout().setContentsMargins(9, 9, 9, 0)
        colap.extra_elem.clicked.connect(lambda: self.delete_subset((widget, colap, subset)))
        widget.layout().addWidget(colap)
        if len(self.elements) == 0:
            colap.toggle_collapsed()
            colap.title_frame.setChecked(True)

        subset = SubsetWidget()
        self.CacheChecked.connect(subset.enable_disable_cache_dependants)
        self.cache_checked(self.cache_latents_checked)
        subset.sub_widget.layout().setContentsMargins(9, 9, 9, 0)
        colap.add_widget(subset, "main_widget")

        self.elements.add((widget, colap, subset))
        return subset

    @QtCore.Slot(tuple)
    def delete_subset(self, elem: tuple) -> None:
        temp = {elem}
        self.elements = self.elements - temp
        self.scrollWidget.layout().removeWidget(elem[0])
        elem[0].deleteLater()
        self.scrollWidget.layout().update()

    @QtCore.Slot(bool)
    def cache_checked(self, checked: bool):
        self.cache_latents_checked = checked
        self.CacheChecked.emit(checked)

    def get_subset_args(self, skip_check: bool = False) -> list[dict] | None:
        args_list = []
        failed_args = []
        if skip_check:
            for arg in self.elements:
                args_list.append(arg[2].args)
            return args_list
        for arg in self.elements:
            exists = os.path.exists(arg[2].args['image_dir'])
            if (not exists) or (not os.path.isdir(arg[2].args['image_dir'])):
                failed_args.append(arg)
                arg[2].widget.lineEdit.update_stylesheet()
                if arg[1].is_collapsed:
                    arg[1].toggle_collapsed()
                    arg[1].title_frame.update_arrow(False)
                    arg[1].title_frame.setChecked(True)
                continue
            args_list.append(arg[2].args)
        if len(failed_args) > 0:
            print("At least one subset arg doesn't have an input folder set properly")
            return None
        return args_list

    def load_args(self, args: dict):
        if "subsets" not in args:
            return
        for elem in self.elements:
            self.delete_subset(elem)

        subsets = args['subsets']
        for subset in subsets:
            elem = self.add_empty_subset()
            elem.load_args(subset)
        self.cache_checked(self.cache_latents_checked)
