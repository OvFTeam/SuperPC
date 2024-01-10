import os
import shutil
import subprocess
import sys
from configparser import ConfigParser

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
                             QMainWindow, QMessageBox, QPushButton,
                             QVBoxLayout, QWidget)


def autohotkey_install():
    script = sys._MEIPASS
    autohotkey_path = r"C:\Program Files\AutoHotkey\AutoHotkey.exe"
    compiler_path = r"C:\Program Files\AutoHotkey\Compiler"

    if not os.path.exists(autohotkey_path):
        subprocess.run([f"{script}\\AutoHotKey.exe", "/S",
                       "/D=C:\Program Files\AutoHotkey"], check=True)

    os.makedirs(compiler_path, exist_ok=True)
    current_path = os.environ.get("PATH", "")
    if compiler_path not in current_path:
        os.environ["PATH"] = f"{current_path};{compiler_path}"


autohotkey_install()


def run():
    script = sys._MEIPASS
    current_dir = os.getcwd()
    config_file = os.path.join(os.getcwd(), "config.ini")
    output_file = os.path.join(current_dir, "browser.exe")
    shutil.copy(config_file, script)
    os.system(
        f"AHk2Exe.exe /in {script}\\browser.ahk /out \"{output_file}\" /icon {script}\\icon.ico /bin {script}\\AutoHotkeySC.bin")

class SuperPC(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SuperPC")
        self.resize(400, 40)
        self.setStyleSheet("""
        * {
            background-color: #282a36;
            color: #f8f8f2;
        }
        QLabel {
            color: #f8f8f2;
        }
        QLineEdit {
            background-color: #44475a;
            color: #f8f8f2;
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton {
            background-color: #bd93f9;
            color: #f8f8f2;
            border: none;
            border-radius: 5px;
            padding: 5px 10px;
        }

        QPushButton:hover {
            background-color: #e683d9;
            background-image: linear-gradient(to bottom right, #e683d9, #bd93f9);
        }

        QPushButton:pressed {
            background-color: #a75dbb;
            padding: 6px 11px;
        }

        QMainWindow {
            background-color: #282a36;
        }

        QMessageBox {
            background-color: #282a36;
            color: #f8f8f2;
            border-radius: 5px;
            border: 1px solid #6272a4;
        }
        """)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        self.config = ConfigParser()
        if not os.path.exists("config.ini"):
            config = ConfigParser()
            config.add_section("Links")
            with open("config.ini", "w") as configfile:
                config.write(configfile)
        self.config.read("config.ini")
        self.links_section = "Links"
        self.link_entries = []
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        self.create_export_button()
        self.create_add_button()
        self.create_link_entries()

    def create_link_entries(self):
        for key, value in self.config.items(self.links_section):
            link_layout = QHBoxLayout()
            link_label = QLabel(key, self)
            link_entry = QLineEdit(value, self)
            remove_button = QPushButton("Xoá trang", self)
            remove_button.clicked.connect(lambda _, entry=(link_label, link_entry, remove_button): self.remove_link(entry))
            remove_button.clicked.connect(lambda: self.resize(400, 40))
            link_layout.addWidget(link_label)
            link_layout.addWidget(link_entry)
            link_layout.addWidget(remove_button)
            self.layout.addLayout(link_layout)
            self.link_entries.append((link_label, link_entry, remove_button))

    def create_add_button(self):
        add_button = QPushButton("Thêm trang mới", self)
        add_button.clicked.connect(self.add_link)
        self.layout.addWidget(add_button)

    def add_link(self):
        link_layout = QHBoxLayout()
        link_label = QLabel("Link" + str(len(self.link_entries) + 1), self)
        link_entry = QLineEdit(self)
        remove_button = QPushButton("Xoá trang", self)
        remove_button.clicked.connect(lambda _, entry=(link_label, link_entry, remove_button): self.remove_link(entry))
        remove_button.clicked.connect(lambda: self.resize(400, 40))
        link_layout.addWidget(link_label)
        link_layout.addWidget(link_entry)
        link_layout.addWidget(remove_button)
        self.layout.addLayout(link_layout)
        self.link_entries.append((link_label, link_entry, remove_button))

    def remove_link(self, entry):
        link_label, link_entry, remove_button = entry
        link_label.deleteLater()
        link_entry.deleteLater()
        remove_button.deleteLater()
        self.link_entries.remove(entry)

    def create_export_button(self):
        export_button = QPushButton("Tạo trình duyệt", self)
        export_button.clicked.connect(self.export_exe)
        self.layout.addWidget(export_button)

    def export_exe(self):
        self.config.remove_section(self.links_section)
        self.config.add_section(self.links_section)
        for link_label, link_entry, _ in self.link_entries:
            key = link_label.text()
            value = link_entry.text()
            self.config.set(self.links_section, key, value)
        with open("config.ini", "w") as configfile:
            self.config.write(configfile)
        run()
        os.remove("config.ini")
        QMessageBox.information(
            self, "Thành công", "Chrome đã được tạo thành công!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SuperPC()
    window.show()
    sys.exit(app.exec_())