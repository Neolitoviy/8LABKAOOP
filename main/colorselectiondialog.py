from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton

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
        self.setGeometry(1000, 750, 800, 600)  # x, y, width, height

    def selected_color(self):
        return self.list_widget.currentItem().text()