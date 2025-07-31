from PyQt6.QtWebEngineCore import QWebEngineFullScreenRequest, QWebEngineSettings
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt


class WebVideoPlayer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_volume = 0.5
        self.current_muted = False
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        self._original_layout = None
        self._original_index = None

        # Web view for video playback
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view, stretch=1)
        self.web_view.page().fullScreenRequested.connect(self.handle_fullscreen)
        self.web_view.settings().setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)

        # Status label
        self.status_label = QLabel("Loading video...")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Error handling buttons
        control_layout = QHBoxLayout()

        self.retry_button = QPushButton("Retry")
        self.retry_button.hide()
        self.retry_button.clicked.connect(self.retry_load)
        control_layout.addWidget(self.retry_button)

        self.browser_button = QPushButton("Open in Browser")
        self.browser_button.clicked.connect(self.open_in_browser)
        control_layout.addWidget(self.browser_button)

        layout.addLayout(control_layout)

    def load_video(self, url):
        self.video_url = url
        self.status_label.setText("Loading video...")
        self.retry_button.hide()

        if self.web_view.page():
            self.web_view.page().runJavaScript(
                """
                var v = document.getElementById('myVideo');
                v ? [v.volume, v.muted] : [null, null];
                """,
                self.store_volume_and_muted
            )
        else:
            self.store_volume_and_muted([None, None])

    def store_volume_and_muted(self, result):
        if result and isinstance(result, list) and len(result) == 2:
            volume, muted = result

            if volume is not None and 0 <= volume <= 1:
                self.current_volume = volume

            if muted is not None:
                self.current_muted = muted

        self.load_media()

    def load_media(self):
        # Create HTML video player
        html = f"""
        <html>
        <head>
            <style>
                body, html {{
                    margin: 0;
                    padding: 0;
                    background-color: black;
                    height: 100%;
                    width: 100%;
                    overflow: hidden;
                }}
                video {{
                    width: 100%;
                    height: 100%;
                }}
            </style>
        </head>
        <body>
            <video id="myVideo" controls preload="auto">
                <source src="{self.video_url}" type="video/webm">
                Your browser does not support the video tag.
            </video>
        </body>
        </html>
        """
        self.web_view.setHtml(html)
        self.web_view.loadFinished.connect(self.apply_saved_state)

    def apply_saved_state(self, success):
        self.web_view.loadFinished.disconnect(self.apply_saved_state)

        if success:
            js_code = f"""
                var video = document.getElementById('myVideo');
                if (video) {{
                    video.volume = {self.current_volume};
                    video.muted = {str(self.current_muted).lower()};
                }}
            """
            self.web_view.page().runJavaScript(js_code)
            self.status_label.setText("Video loaded")
        else:
            self.status_label.setText("Error loading video")
            self.retry_button.show()
            self.browser_button.show()

    def retry_load(self):
        self.load_media()

    def open_in_browser(self):
        import webbrowser
        webbrowser.open(self.video_url)

    def handle_fullscreen(self, request: QWebEngineFullScreenRequest):
        request.accept()

        if request.toggleOn():
            self._original_layout = self.web_view.parent().layout()
            self._original_index = self._original_layout.indexOf(self.web_view)

            self.web_view.setParent(None)
            self.web_view.showFullScreen()
        else:
            self.web_view.showNormal()

            if self._original_layout is not None and self._original_index is not None:
                self._original_layout.insertWidget(self._original_index, self.web_view, stretch=1)

            self._original_layout = None
            self._original_index = None


    def unload_video(self):
        self.web_view.setHtml("")