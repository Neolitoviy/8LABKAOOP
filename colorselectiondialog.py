from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QDesktopWidget


class ColorSelectionDialog(QDialog):
    def __init__(self, colors, parent=None):
        super(ColorSelectionDialog, self).__init__(parent)
        self.setWindowTitle('Select a color to use')
        self.layout = QVBoxLayout(self)

        self.list_widget = QListWidget(self)
        for color in colors:
            self.list_widget.addItem(color)
        self.list_widget.itemDoubleClicked.connect(self.accept)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.clicked.connect(self.reject)

        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.exit_button)

        # Get screen size
        screen_geometry = QDesktopWidget().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Calculate window size
        window_width = int(screen_width * 0.5)
        window_height = int(screen_height * 0.5)

        # Calculate window position
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        # Set window size and position
        self.setGeometry(x, y, window_width, window_height)

    def selected_color(self):
        return self.list_widget.currentItem().text()