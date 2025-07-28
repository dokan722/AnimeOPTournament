from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpacerItem,
    QSizePolicy, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from widgets.video_player import WebVideoPlayer
from data_collection.models import Opening


class MatchWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)

        # Round info
        self.round_label = QLabel()
        self.round_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.round_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(self.round_label)

        # Match info
        self.match_label = QLabel()
        self.match_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.match_label)

        # Videos area
        videos_layout = QHBoxLayout()
        videos_layout.setContentsMargins(20, 20, 20, 20)

        # Left video
        left_frame = QFrame()
        left_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        left_layout = QVBoxLayout(left_frame)

        self.left_video = WebVideoPlayer()
        left_layout.addWidget(self.left_video)

        self.left_info = QLabel()
        self.left_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(self.left_info)

        self.left_button = QPushButton("Select Winner")
        self.left_button.clicked.connect(lambda: self.select_winner(0))
        left_layout.addWidget(self.left_button)

        videos_layout.addWidget(left_frame)

        # Right video
        right_frame = QFrame()
        right_frame.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        right_layout = QVBoxLayout(right_frame)

        self.right_video = WebVideoPlayer()
        right_layout.addWidget(self.right_video)

        self.right_info = QLabel()
        self.right_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.right_info)

        self.right_button = QPushButton("Select Winner")
        self.right_button.clicked.connect(lambda: self.select_winner(1))
        right_layout.addWidget(self.right_button)

        videos_layout.addWidget(right_frame)
        main_layout.addLayout(videos_layout, stretch=1)

        videos_layout.setStretch(0, 1)  # left_frame
        videos_layout.setStretch(1, 1)

        # Save button
        self.save_button = QPushButton("Save Tournament")
        self.save_button.setFixedHeight(40)
        main_layout.addWidget(self.save_button)

    def set_match_info(self, round_name: str, match_num: int, total_matches: int):
        self.round_label.setText(round_name)
        self.match_label.setText(f"Match {match_num + 1} of {total_matches}")

    def set_openings(self, left: Opening, right: Opening):
        # Left opening
        self.left_video.load_video(left.VideoLink)
        self.left_info.setText(
            f"<p style=\"font-size:20px;\"><b>{left.Title}</b></p>"
            f"<p style=\"font-size:12px; color:grey\">by <b>{left.Artist}</b></p>"
            f"<p style=\"font-size:12px;\">{left.AnimeName} ({left.Num})</b></p>"
        )
        self.left_button.setProperty('opening', left)

        # Right opening
        self.right_video.load_video(right.VideoLink)
        self.right_info.setText(
            f"<p style=\"font-size:20px;\"><b>{right.Title}</b></p>"
            f"<p style=\"font-size:12px; color:grey\">by <b>{right.Artist}</b></p>"
            f"<p style=\"font-size:12px;\">{right.AnimeName} ({right.Num})</b></p>"
        )
        self.right_button.setProperty('opening', right)

    def select_winner(self, side: int):
        button = self.left_button if side == 0 else self.right_button
        self.left_video.unload_video()
        self.right_video.unload_video()
        winner = button.property('opening')
        self.winnerSelected.emit(winner)

    winnerSelected = pyqtSignal(Opening)