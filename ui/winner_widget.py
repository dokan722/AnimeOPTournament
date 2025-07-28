from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFrame, QHBoxLayout
)
from PyQt6.QtCore import Qt
from widgets.video_player import WebVideoPlayer


class WinnerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Title
        self.title_label = QLabel("Tournament Winner")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)

        video_layout = QHBoxLayout()
        video_layout.setContentsMargins(20, 20, 20, 20)

        # Winner container
        winner_frame = QFrame()
        winner_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        winner_layout = QVBoxLayout(winner_frame)

        self.video_player = WebVideoPlayer()
        winner_layout.addWidget(self.video_player, stretch=1)

        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        winner_layout.addWidget(self.info_label)

        video_layout.addWidget(winner_frame, stretch=1)
        layout.addLayout(video_layout, stretch=1)

        # Restart button
        self.restart_button = QPushButton("New Tournament")
        self.restart_button.setFixedHeight(40)
        layout.addWidget(self.restart_button)

    def set_winner(self, opening):
        self.video_player.load_video(opening.VideoLink)
        self.info_label.setText(
            f"<p style=\"font-size:40px;\"><b>Winner of the Tournament</b></p>"
            f"<p style=\"font-size:32px;\"><b>{opening.Title}</b></p>"
            f"<p style=\"font-size:20px; color:grey\">by <b>{opening.Artist}</b></p>"
            f"<p style=\"font-size:20px;\">{opening.AnimeName} ({opening.Num})</b></p>"
        )