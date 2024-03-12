from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QApplication
from qt_material import QtStyleTools, apply_stylesheet
from ui_files.MainUI import Ui_MainWindow
from main_ui_files.MainUI import MainWidget
from pathlib import Path
import json


class MainWindow(QMainWindow, QtStyleTools):
    def __init__(self, app: QApplication = None) -> None:
        super().__init__()
        self.app = app
        self.widget = Ui_MainWindow()
        self.main_widget = MainWidget()
        self.dark_themes: list[QAction] = []
        self.light_themes: list[QAction] = []
        self.no_theme = QAction("", self)

        self.setup_widget()
        self.setup_themes()
        self.setup_connections()

    def setup_widget(self) -> None:
        self.widget.setupUi(self)
        self.setMinimumWidth(739)
        screen_size = QApplication.screens()[0].size()
        self.setGeometry(
            screen_size.width() / 2 - (self.geometry().width() / 2),
            screen_size.height() / 2 - (self.geometry().height() / 2),
            self.geometry().width() + 10,
            750,
        )
        self.centralWidget().layout().addWidget(self.main_widget)

    def setup_themes(self) -> None:
        themes_path = Path("css/themes")
        for theme in themes_path.iterdir():
            if len(theme.name.split("500")) > 1:
                continue
            if len(theme.name.split("dark")) > 1:
                self.dark_themes.append(QAction(theme.stem.split("_")[1], self))
            else:
                self.light_themes.append(QAction(theme.stem.split("_")[1], self))
        for theme in self.dark_themes:
            self.widget.dark_theme_menu.addAction(theme)
        for theme in self.light_themes:
            self.widget.light_theme_menu.addAction(theme)

    def setup_connections(self) -> None:
        self.widget.save_toml.triggered.connect(self.main_widget.save_toml)
        self.widget.load_toml.triggered.connect(self.main_widget.load_toml)
        for i, action in enumerate(self.dark_themes):
            action.triggered.connect(
                lambda _=False, index=i: self.change_theme(index, False)
            )
        for i, action in enumerate(self.light_themes):
            action.triggered.connect(
                lambda _=False, index=i: self.change_theme(index, True)
            )
        self.widget.no_theme_action.triggered.connect(
            lambda _=False: self.change_theme(0, False, True)
        )

    def change_theme(
        self, index: int, is_light: bool = False, no_theme: bool = False
    ) -> None:
        if no_theme:
            theme_path = None
            self.app.setStyleSheet("")
        else:
            prefix = "light" if is_light else "dark"
            if is_light:
                name = self.light_themes[index].text()
            else:
                name = self.dark_themes[index].text()
            theme_path = Path(f"css/themes/{prefix}_{name}.xml")
            apply_stylesheet(
                self.app,
                theme=str(theme_path),
                invert_secondary=is_light,
            )
        config = Path("config.json")
        config_dict = json.loads(config.read_text()) if config.exists() else {}
        config_dict["theme"] = {
            "location": theme_path.as_posix() if theme_path else None,
            "is_light": is_light,
        }
        config.write_text(json.dumps(config_dict, indent=2))
