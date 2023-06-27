import json
import time

import pygraphviz as pgv
from PIL import Image
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget,
    QFileDialog, QGraphicsScene, QInputDialog, QMessageBox, QDialog, QApplication
)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

from ball import Ball
from resizablegraphicsview import ResizableGraphicsView
from colorselectiondialog import ColorSelectionDialog


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setup_ui()
        self.data = None
        self.setWindowTitle("Volleyball colouring")
        self.ball = None

    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.btn_open = QPushButton('Open JSON file')
        self.btn_open.clicked.connect(self.open_file)

        self.btn_manual_input = QPushButton('Manual input')
        self.btn_manual_input.clicked.connect(self.manual_input)

        self.btn_solve = QPushButton('Solve')
        self.btn_solve.clicked.connect(self.solve_problem)

        self.text_edit = QTextEdit()

        self.graph_view = ResizableGraphicsView()
        self.scene = QGraphicsScene()
        self.graph_view.setScene(self.scene)

        self.layout.addWidget(self.btn_open)
        self.layout.addWidget(self.btn_manual_input)
        self.layout.addWidget(self.btn_solve)
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.graph_view)

        # Get screen size
        screen_geometry = QApplication.desktop().availableGeometry()
        screen_width = screen_geometry.width()
        screen_height = screen_geometry.height()

        # Calculate window size
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.6)

        # Calculate window position
        x = int((screen_width - window_width) / 2)
        y = int((screen_height - window_height) / 2)

        # Set window size and position
        self.setGeometry(x, y, window_width, window_height)

    def generate_graph(self):
        if self.data is None:
            self.show_warning()
            return

        if self.ball is None or self.ball.num_sectors != self.data['num_sectors']:
            self.ball = Ball(self.data['num_sectors'])
            self.ball.color_stripes()

        G = pgv.AGraph(directed=True)
        G.graph_attr.update(rankdir='LR')  # horizontal orientation

        # Add stripes as nodes to the graph, naming them with both the stripe index and color
        for i, stripe in enumerate(self.ball.stripes):
            for j, color in enumerate(stripe):
                G.add_node(f"{color} ({i + 1}, {j + 1})", fillcolor=color.lower(), style='filled')

        # Connect each color of the stripe to the next one
        for i, stripe in enumerate(self.ball.stripes):
            for j in range(len(stripe) - 1):
                G.add_edge(f"{stripe[j]} ({i + 1}, {j + 1})", f"{stripe[j + 1]} ({i + 1}, {j + 2})")

        # Connect each stripe of a sector to the first stripe of the next sector
        for i in range(len(self.ball.stripes) - 1):
            for j in range(len(self.ball.stripes[i])):
                G.add_edge(f"{self.ball.stripes[i][j]} ({i + 1}, {j + 1})",
                           f"{self.ball.stripes[i + 1][0]} ({i + 2}, 1)")

        # Connect each stripe of the last sector to the first stripe of the first sector
        for j in range(len(self.ball.stripes[-1])):
            G.add_edge(f"{self.ball.stripes[-1][j]} ({len(self.ball.stripes)}, {j + 1})",
                       f"{self.ball.stripes[0][0]} (1, 1)")

        width = self.graph_view.width() / 20
        height = self.graph_view.height() / 20
        G.graph_attr.update(size=f"{width},{height}!")

        G.layout(prog='dot')

        G.draw('graph.png')

        img = Image.open('graph.png')
        qim = QImage(img.tobytes('raw', 'RGBA'), img.size[0], img.size[1], QImage.Format_RGBA8888)
        pix = QPixmap.fromImage(qim)

        self.scene.clear()
        self.scene.addPixmap(pix)
        self.graph_view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open JSON file", "", "JSON Files (*.json)", options=options
        )
        if file_name:
            try:
                with open(file_name, 'r') as f:
                    self.data = json.load(f)
                self.text_edit.setText(json.dumps(self.data, indent=4))
            except Exception as e:
                QMessageBox.warning(self, 'Warning', f'Failed to open or read file. Error: {str(e)}')

    def manual_input(self):
        num_sectors, ok = QInputDialog.getInt(
            self, 'Input', 'Enter the number of sectors:', min=0, max=200
        )
        if ok:
            colors = Ball(0).colors
            selected_colors = []
            while colors:
                dialog = ColorSelectionDialog(colors, self)
                if dialog.exec_() == QDialog.Accepted:
                    color = dialog.selected_color()
                    selected_colors.append(color)
                    colors.remove(color)
                else:
                    break
            self.data = {'num_sectors': num_sectors, 'colors': selected_colors}
            self.text_edit.setText(json.dumps(self.data, indent=4))

    def solve_problem(self):
        if self.data is None:
            self.show_warning()
            return

        start_time = time.time()
        if self.ball is None or self.ball.num_sectors != self.data['num_sectors'] or self.ball.colors != self.data[
            'colors']:
            self.ball = Ball(self.data['num_sectors'], self.data['colors'])
            self.ball.color_stripes()
        self.generate_graph()
        end_time = time.time()
        self.text_edit.setText(
            f'Time taken: {end_time - start_time} seconds\n{str(self.ball)}'
        )

    def show_warning(self):
        QMessageBox.warning(self, 'Warning', 'No data available. Please open a JSON file or input data manually.')
