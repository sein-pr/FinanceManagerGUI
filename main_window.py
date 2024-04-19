from PyQt5 import QtWidgets
from chart_display import ChartDisplay
from finance_manager import FinanceManager

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Finance Manager")
        self.setGeometry(100, 100, 800, 600)

        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)

        layout = QtWidgets.QVBoxLayout()
        input_layout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel("Enter the month (e.g., 01 for January):")
        label.setStyleSheet("color: blue; font-size: 18px;")
        input_layout.addWidget(label)

        self.input_month = QtWidgets.QLineEdit()
        input_layout.addWidget(self.input_month)

        button = QtWidgets.QPushButton("Process")
        button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px 24px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;")
        button.clicked.connect(self.process_transactions)
        input_layout.addWidget(button)

        layout.addLayout(input_layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Date", "Name", "Amount"])
        layout.addWidget(self.table)

        self.sum_label = QtWidgets.QLabel()
        self.sum_label.setStyleSheet("color: blue; font-size: 18px;")
        layout.addWidget(self.sum_label)

        self.chart_display = ChartDisplay()
        layout.addWidget(self.chart_display)

        centralWidget.setLayout(layout)

        # Connect the returnPressed signal of the QLineEdit to the click event of the "Process" button
        self.input_month.returnPressed.connect(button.click)

    def process_transactions(self):
        input_month = self.input_month.text()
        if input_month.isdigit() and 1 <= int(input_month) <= 12:
            input_month = input_month.zfill(2)
            transactions = FinanceManager().get_transactions(input_month)
            self.populate_table(transactions)
            total_sum = sum(transaction[2] for transaction in transactions)
            self.sum_label.setText(f'Sum of transactions for {input_month} is {total_sum}')

            previous_month = str(int(input_month) - 1).zfill(2) if int(input_month) > 1 else '12'
            previous_transactions = FinanceManager().get_transactions(previous_month)
            previous_total_sum = sum(transaction[2] for transaction in previous_transactions)

            months = [previous_month, input_month]
            sums = [previous_total_sum, total_sum]

            self.chart_display.display_comparison_chart(months, sums)
        else:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText("Invalid input. Please enter a valid month (01 to 12).")
            msg.setWindowTitle("Error")
            msg.exec_()

    def populate_table(self, transactions):
        self.table.setRowCount(len(transactions))
        for i, transaction in enumerate(transactions):
            date_item = QtWidgets.QTableWidgetItem(transaction[0])
            name_item = QtWidgets.QTableWidgetItem(transaction[1])
            amount_item = QtWidgets.QTableWidgetItem(str(transaction[2]))
            self.table.setItem(i, 0, date_item)
            self.table.setItem(i, 1, name_item)
            self.table.setItem(i, 2, amount_item)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
