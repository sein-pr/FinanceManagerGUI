from PyQt5 import QtWidgets
from category_manager import CategoryManager

class CategoryManagementWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Category Management")
        self.setGeometry(100, 100, 600, 400)

        self.category_manager = CategoryManager()

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.category_table = QtWidgets.QTableWidget()
        self.category_table.setColumnCount(2)
        self.category_table.setHorizontalHeaderLabels(["Category Name", ""])
        self.category_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.category_table)

        button_layout = QtWidgets.QHBoxLayout()
        self.add_button = QtWidgets.QPushButton("Add")
        self.edit_button = QtWidgets.QPushButton("Edit")
        self.remove_button = QtWidgets.QPushButton("Remove")
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.remove_button)
        layout.addLayout(button_layout)

        self.populate_category_table()

        self.add_button.clicked.connect(self.add_category)
        self.edit_button.clicked.connect(self.edit_category)
        self.remove_button.clicked.connect(self.remove_category)

    def populate_category_table(self):
        self.category_table.clearContents()
        self.category_table.setRowCount(len(self.category_manager.get_categories()))
        for i, category in enumerate(self.category_manager.get_categories()):
            category_item = QtWidgets.QTableWidgetItem(category)
            edit_button = QtWidgets.QPushButton("Edit")
            self.category_table.setItem(i, 0, category_item)
            self.category_table.setCellWidget(i, 1, edit_button)
            edit_button.clicked.connect(lambda checked, row=i: self.edit_category(row))

    def add_category(self):
        new_category, ok = QtWidgets.QInputDialog.getText(self, "Add Category", "Enter new category name:")
        if ok and new_category:
            self.category_manager.add_category(new_category)
            self.category_manager.category_changed_signal.emit()
            self.populate_category_table()

    def edit_category(self, row):
        category = self.category_table.item(row, 0).text()
        new_category, ok = QtWidgets.QInputDialog.getText(self, "Edit Category", "Enter new category name:", text=category)
        if ok and new_category:
            self.category_manager.edit_category(row, new_category)
            self.category_manager.category_changed_signal.emit()
            self.populate_category_table()

    def remove_category(self):
        selected_rows = set(index.row() for index in self.category_table.selectedIndexes())
        for row in sorted(selected_rows, reverse=True):
            self.category_manager.remove_category(row)
        self.category_manager.category_changed_signal.emit()
        self.populate_category_table()
