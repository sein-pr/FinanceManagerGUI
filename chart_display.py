from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ChartDisplay(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.chart_layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.chart_layout)

    def display_comparison_chart(self, months, sums):
        for i in reversed(range(self.chart_layout.count())):
            widget = self.chart_layout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        fig = Figure()
        ax = fig.add_subplot(111)
        ax.bar(months, sums, color=['blue', 'green'])
        ax.set_xlabel('Month')
        ax.set_ylabel('Total Sum')
        ax.set_title('Comparison of Total Sums')
        canvas = FigureCanvas(fig)
        self.chart_layout.addWidget(canvas)
