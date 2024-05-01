from pyqtgraph import QtCore


class CategoryManager:
    def __init__(self):
        self.categories = self.load_categories()
        self.category_changed_signal = CategoryChangedSignal()

    def load_categories(self):
        # Load categories from a configuration file or database
        return ["Food", "Rent", "Transportation", "Entertainment", "Utilities"]

    def get_categories(self):
        return self.categories

    def add_category(self, category_name):
        # Add a new category to the list
        self.categories.append(category_name)
        self.category_changed_signal.emit()

    def edit_category(self, category_index, new_name):
        # Update the name of an existing category
        self.categories[category_index] = new_name
        self.category_changed_signal.emit()

    def remove_category(self, category_index):
        # Remove a category from the list
        del self.categories[category_index]
        self.category_changed_signal.emit()

    def assign_category(self, transaction, category_index):
        # Assign a category to a transaction
        transaction = list(transaction)
        transaction[3] = self.categories[category_index]
        return tuple(transaction)

class CategoryChangedSignal(QtCore.QObject):
    signal = QtCore.pyqtSignal()

    def emit(self):
        self.signal.emit()
