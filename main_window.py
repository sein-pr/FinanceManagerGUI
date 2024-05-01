import sys
from PyQt5 import QtWidgets, QtCore
from chart_display import ChartDisplay
from finance_manager import FinanceManager
from category_manager import CategoryManager
from category_management_window import CategoryManagementWindow

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

        label_category = QtWidgets.QLabel("Select a category:")
        label_category.setStyleSheet("color: blue; font-size: 18px;")
        input_layout.addWidget(label_category)

        self.category_combobox = QtWidgets.QComboBox()
        self.category_manager = CategoryManager()
        self.category_manager.category_changed_signal.signal.connect(self.populate_category_combobox)
        self.populate_category_combobox()
        input_layout.addWidget(self.category_combobox)

        self.category_management_button = QtWidgets.QPushButton("Manage Categories")
        self.category_management_button.clicked.connect(self.open_category_management)
        input_layout.addWidget(self.category_management_button)

        button = QtWidgets.QPushButton("Process")
        button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px 24px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;")
        button.clicked.connect(self.process_transactions)
        input_layout.addWidget(button)

        layout.addLayout(input_layout)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Date", "Name", "Amount", "Category"])
        layout.addWidget(self.table)

        self.sum_label = QtWidgets.QLabel()
        self.sum_label.setStyleSheet("color: blue; font-size: 18px;")
        layout.addWidget(self.sum_label)

        self.chart_display = ChartDisplay(self)
        layout.addWidget(self.chart_display)

        centralWidget.setLayout(layout)

        self.input_month.returnPressed.connect(button.click)

    def populate_category_combobox(self):
        self.category_combobox.clear()
        categories = self.category_manager.get_categories()
        self.category_combobox.addItem("All")
        self.category_combobox.addItems(categories)

    def open_category_management(self):
        self.category_management_window = CategoryManagementWindow(self)
        self.category_management_window.exec_()

    def process_transactions(self):
        input_month = self.input_month.text()
        if input_month.isdigit() and 1 <= int(input_month) <= 12:
            input_month = input_month.zfill(2)
            transactions = FinanceManager().get_transactions(input_month)
            selected_category_index = self.category_combobox.currentIndex()
            self.populate_table(transactions, selected_category_index)
            total_sum = sum(transaction[2] for transaction in transactions)
            self.sum_label.setText(f'Sum of transactions for {input_month} is {total_sum:.2f}')

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

    def populate_table(self, transactions, selected_category_index):
        self.table.clearContents()
        self.table.setRowCount(0)

        for i, transaction in enumerate(transactions):
            if selected_category_index == 0 or transaction[3] == self.category_manager.get_categories()[selected_category_index - 1]:
                row = self.table.rowCount()
                self.table.insertRow(row)
                date_item = QtWidgets.QTableWidgetItem(transaction[0])
                name_item = QtWidgets.QTableWidgetItem(transaction[1])
                amount_item = QtWidgets.QTableWidgetItem(f"{transaction[2]:.2f}")
                category_item = QtWidgets.QTableWidgetItem(transaction[3])
                self.table.setItem(row, 0, date_item)
                self.table.setItem(row, 1, name_item)
                self.table.setItem(row, 2, amount_item)
                self.table.setItem(row, 3, category_item)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
