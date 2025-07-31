import os
from typing import Dict, Any

from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QFileDialog, QMessageBox
from ui.start_screen import StartScreen
from ui.match_widget import MatchWidget
from ui.winner_widget import WinnerWidget
from tournament.manager import TournamentManager
from utils.storage import save_tournament, load_tournament, get_saved_tournaments
from data_collection.data_loader import get_openings

dark_stylesheet = """
QWidget {
    background-color: #121212;
    color: #ffffff;
}
QPushButton {
    background-color: #1f1f1f;
    border: 1px solid #3a3a3a;
    padding: 5px;
}
QPushButton:hover {
    background-color: #2a2a2a;
}
"""


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Anime Opening Tournament")
        self.resize(1200, 700)

        self.manager = TournamentManager()
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Create screens
        self.start_screen = StartScreen()
        self.match_widget = MatchWidget()
        self.winner_widget = WinnerWidget()

        # Add to stack
        self.stacked_widget.addWidget(self.start_screen)
        self.stacked_widget.addWidget(self.match_widget)
        self.stacked_widget.addWidget(self.winner_widget)

        # Connect signals
        self.start_screen.start_button.clicked.connect(self.start_tournament)
        self.start_screen.load_button.clicked.connect(self.load_tournament)
        self.start_screen.info_button.clicked.connect(self.show_info_window)
        self.start_screen.op_combo.currentIndexChanged.connect(self.selection_value_changed)
        self.start_screen.mode_combo.currentIndexChanged.connect(self.mode_value_changed)
        self.match_widget.winnerSelected.connect(self.handle_winner)
        self.match_widget.save_button.clicked.connect(self.save_current_tournament)
        self.winner_widget.restart_button.clicked.connect(self.return_to_main_window)
        self.setStyleSheet(dark_stylesheet)

    def mode_value_changed(self):
        if self.start_screen.mode_combo.currentIndex() == 0:
            self.start_screen.take_sb.show()
        else:
            self.start_screen.take_sb.hide()

    def selection_value_changed(self):
        if self.start_screen.op_combo.currentIndex() == 0:
            self.start_screen.take_sb.setRange(2, self.start_screen.opening_count)
        else:
            self.start_screen.take_sb.setRange(2, self.start_screen.anime_count)

    def return_to_main_window(self):
        self.winner_widget.video_player.unload_video()
        self.stacked_widget.setCurrentWidget(self.start_screen)

    def start_tournament(self):
        params = self.start_screen.get_tournament_params()
        if not self.check_constraints(params):
            return

        # Load openings
        openings = get_openings(
            take=params['take'],
            choose=params['choose'],
            mode=params['mode'],
            selection=params['selection']
        )

        # Initialize tournament
        self.manager.new_tournament(params['name'], openings)
        self.show_next_match()

    def load_tournament(self):
        saved = get_saved_tournaments()
        if not saved:
            QMessageBox.information(self, "Load Error", "No tournaments saved")
            return

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Load Tournament",
            "saved_tournaments",
            "JSON Files (*.json)"
        )

        if filename:
            self.manager = load_tournament(os.path.basename(filename).replace('.json', ''))
            if not self.manager:
                QMessageBox.critical(self, "Load Error", "Failed to load tournament")
                return
            if self.manager.is_complete():
                self.show_winner()
            else:
                self.show_next_match()

    def check_constraints(self, params: Dict[str, Any]):
        if not params['name']:
            QMessageBox.information(self, "Name missing", "Provide tournament name.")
            return False
        if params['choose'] > params['take']:
            QMessageBox.information(self, "Wrong size", "You cannot choose more anime than you take.")
            return False
        return True

    def save_current_tournament(self):
        if not self.manager.name:
            return

        save_result = save_tournament(self.manager, self.manager.name)
        if save_result:
            QMessageBox.information(self, "Saved", "Tournament saved successfully!")
        else:
            QMessageBox.critical(self, "Save Error", "Failed to save tournament")

    def show_next_match(self):
        match = self.manager.get_current_match()
        if not match:
            if self.manager.is_complete():
                self.show_winner()
            return

        # Calculate round information
        total_rounds = len(self.manager.bracket.rounds)
        current_round = self.manager.bracket.current_round
        round_size = len(self.manager.bracket.rounds[current_round])

        round_names = {
            0: "Winner",
            1: "Finals",
            2: "Semifinals",
            3: "Quarterfinals"
        }
        round_name = round_names.get(
            total_rounds - current_round - 1,
            f"Round of {round_size}"
        )

        # Configure match widget
        self.match_widget.set_match_info(
            round_name,
            self.manager.current_match_index,
            len(self.manager.bracket.get_current_matches())
        )
        self.match_widget.set_openings(match[0], match[1])
        self.stacked_widget.setCurrentWidget(self.match_widget)

    def handle_winner(self, winner):
        self.manager.record_winner(winner)
        self.show_next_match()

    def show_winner(self):
        winner = self.manager.get_winner()
        if winner:
            self.winner_widget.set_winner(winner)
            self.stacked_widget.setCurrentWidget(self.winner_widget)

    def show_info_window(self):
        QMessageBox.information(self, "Info", "<h3>Tournament Name</h3>"
"Name of the tournament, save file name will be based on it."
"<h3>Take</h3>"
"How many openings to take."
"<h3>Choose</h3>"
"How many of the openings taken to choose."
"<h3>Selection mode</h3>"
"<b>Top</b> - openings will be taken from top animes (based on popularity on anilist.co).<br>"
"<b>Random</b> - random openings will be selected."
"<h3>Opening selection</h3>"
"<b>All</b> - all openigs per anime will be taken.<br>"
"<b>First</b> - first opening per anime will be taken.<br>"
"<b>Random</b> - random opening per anime will be taken.")