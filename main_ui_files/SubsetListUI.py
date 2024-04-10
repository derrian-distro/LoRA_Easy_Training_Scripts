from pathlib import Path
import time
from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog
from main_ui_files.SubsetUI import SubsetWidget
from ui_files.SubsetListUI import Ui_subset_list_ui


class SubsetListWidget(QWidget):
    def __init__(self, parent: QWidget = None) -> None:
        super().__init__(parent)
        self.content = QWidget(self)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(9, 0, 9, 0)
        self.layout().addWidget(self.content)
        self.widget = Ui_subset_list_ui()
        self.widget.setupUi(self.content)
        self.widget.subset_scroll_area_content.layout().setAlignment(
            QtCore.Qt.AlignmentFlag.AlignTop
        )
        self.widget.subset_scroll_area.setWidgetResizable(True)
        self.cache_latents_checked = False
        self.variable_keep_tokens_checked = False
        self.args = {}
        self.dataset_args = {}
        self.elements: list[SubsetWidget] = []

        self.widget.add_subset_button.clicked.connect(
            lambda: self.add_empty_subset(self.widget.add_subset_name_input.text())
        )
        self.widget.add_bulk_button.clicked.connect(self.add_from_root_folder)

    def add_empty_subset(self, display_name: str = "") -> SubsetWidget:
        if display_name in self.dataset_args:
            name = f"{display_name}_{str(time.time_ns())}"
        else:
            name = display_name
        subset = SubsetWidget(display_name=display_name, name=name)
        subset.colap.extra_elem.clicked.connect(lambda: self.remove_subset(subset))
        subset.edited.connect(self.update_args)
        subset.enable_disable_cache_dependants(self.cache_latents_checked)
        subset.enable_disable_keep_tokens(self.variable_keep_tokens_checked)
        if not self.elements:
            subset.colap.toggle_collapsed()
            subset.colap.title_frame.setChecked(True)
        self.widget.subset_scroll_area_content.layout().addWidget(subset)
        self.elements.append(subset)
        self.dataset_args[(name or subset.name)] = subset.dataset_args
        return subset

    def remove_subset(self, elem: SubsetWidget) -> None:
        self.elements.pop(self.elements.index(elem))
        if elem.name in self.dataset_args:
            del self.dataset_args[elem.name]
        index = self.widget.subset_scroll_area_content.layout().indexOf(elem)
        val = self.widget.subset_scroll_area_content.layout().takeAt(index)
        if val.widget() is not None:
            val.widget().deleteLater()

    def add_from_root_folder(self) -> None:
        root_folder_path = QFileDialog.getExistingDirectory(
            self, "Root folder containing subset folders"
        )
        if not root_folder_path or not Path(root_folder_path).is_dir():
            return
        root_folder_path = Path(root_folder_path)
        while self.elements:
            self.remove_subset(self.elements[0])
        for elem in root_folder_path.iterdir():
            if not elem.is_dir():
                continue
            subset = self.add_empty_subset(elem.name)
            subset.set_folder_from_dialog(elem.name, elem)

    def update_args(self, subset_args: dict, subset_name: str) -> None:
        self.dataset_args[subset_name] = subset_args

    def enable_disable_cache_latents(self, checked: bool) -> None:
        self.cache_latents_checked = checked
        for elem in self.elements:
            elem.enable_disable_cache_dependants(checked)

    def enable_disable_variable_keep_tokens(self, checked: bool) -> None:
        self.variable_keep_tokens_checked = checked
        for elem in self.elements:
            elem.enable_disable_keep_tokens(checked)

    def load_args(self, _: dict) -> bool:
        return False

    def load_dataset_args(self, dataset_args: dict) -> bool:
        while self.elements:
            self.remove_subset(self.elements[0])
        if "subsets" not in dataset_args:
            return False

        subsets = dataset_args["subsets"]
        for subset in subsets:
            subset_name = (
                subset["name"].split("_")[0]
                if "name" in subset and subset["name"].split("_")[0]
                else Path(subset["image_dir"]).name
            )
            elem = self.add_empty_subset(subset_name)
            elem.load_dataset_args(subset)
        self.enable_disable_cache_latents(self.cache_latents_checked)
        self.enable_disable_variable_keep_tokens(self.variable_keep_tokens_checked)
        return True
