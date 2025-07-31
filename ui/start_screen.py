from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QComboBox, QPushButton,
    QHBoxLayout, QSizePolicy, QSpacerItem, QSpinBox
)
from PyQt6.QtCore import Qt
from data_collection.data_loader import get_counts


class StartScreen(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.opening_count, self.anime_count = get_counts()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        title = QLabel("Anime Opening Tournament")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Tournament name
        name_layout = QHBoxLayout()
        name_label = QLabel("Tournament Name:")
        name_label.setFixedHeight(30)
        name_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.name_input = QLineEdit()
        self.name_input.setFixedHeight(30)
        self.name_input.setPlaceholderText("Enter tournament name")
        self.name_input.setMinimumWidth(250)
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        # take
        take_layout = QHBoxLayout()
        take_label = QLabel("Take:")
        take_label.setFixedHeight(30)
        self.take_sb = QSpinBox()
        self.take_sb.setRange(2, self.opening_count)
        self.take_sb.setSingleStep(1)
        self.take_sb.setValue(64)
        take_layout.addWidget(take_label, stretch=1)
        take_layout.addWidget(self.take_sb, stretch=1)
        layout.addLayout(take_layout)

        # choose
        choose_layout = QHBoxLayout()
        choose_label = QLabel("Choose:")
        choose_label.setFixedHeight(30)
        self.choose_combo = QComboBox()
        self.choose_combo.addItems(["2", "4", "8", "16", "32", "64", "128", "256", "512", "1024", "2048"])
        self.choose_combo.setCurrentIndex(5)
        choose_layout.addWidget(choose_label, stretch=1)
        choose_layout.addWidget(self.choose_combo, stretch=1)
        layout.addLayout(choose_layout)

        # Mode selection
        mode_layout = QHBoxLayout()
        mode_label = QLabel("Selection Mode:")
        mode_label.setFixedHeight(30)
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Top", "Random"])
        mode_layout.addWidget(mode_label, stretch=1)
        mode_layout.addWidget(self.mode_combo, stretch=1)
        layout.addLayout(mode_layout)

        # Opening selection
        op_layout = QHBoxLayout()
        op_label = QLabel("Opening Selection:")
        op_label.setFixedHeight(30)
        self.op_combo = QComboBox()
        self.op_combo.addItems(["All", "First", "Random"])
        op_layout.addWidget(op_label, stretch=1)
        op_layout.addWidget(self.op_combo, stretch=1)

        layout.addLayout(op_layout)

        # Buttons
        button_layout = QHBoxLayout()

        self.info_button = QPushButton("Show Info")
        self.info_button.setFixedHeight(40)

        button_layout.addWidget(self.info_button)

        self.load_button = QPushButton("Load Tournament")
        self.load_button.setFixedHeight(40)
        button_layout.addWidget(self.load_button)

        layout.addLayout(button_layout)

        start_layout = QHBoxLayout()

        self.start_button = QPushButton("Start Tournament")
        self.start_button.setFixedHeight(40)
        start_layout.addWidget(self.start_button)

        layout.addLayout(start_layout)

        # Add some spacing
        layout.addSpacerItem(QSpacerItem(20, 40))

    def get_tournament_params(self):
        return {
            "name": self.name_input.text().strip(),
            "take": int(self.take_sb.value()),
            "choose": int(self.choose_combo.currentText()),
            "mode": self.mode_combo.currentText().lower(),
            "selection": self.op_combo.currentText().lower()
        }