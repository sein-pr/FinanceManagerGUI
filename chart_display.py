from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.font_manager as font_manager
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ChartDisplay(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.chart_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.chart_layout)

    def display_comparison_chart(self, months, sums):
        # Clear any existing widgets in the layout
        for i in reversed(range(self.chart_layout.count())):
            widget = self.chart_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        # Define a custom color palette
        colors = ['#2196F3', '#FF9800', '#E91E63', '#4CAF50']

        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.bar(months, sums, color=colors, width=0.6)
        ax.set_xlabel('Month', fontsize=14, fontweight='bold', labelpad=10)
        ax.set_ylabel('Total Sum', fontsize=14, fontweight='bold', labelpad=10)
        ax.set_title('Comparison of Total Sums', fontsize=16, fontweight='bold', pad=20)
        ax.grid(True, linestyle='-', linewidth=0.5)

        canvas = FigureCanvas(fig)
        self.chart_layout.addWidget(canvas)
