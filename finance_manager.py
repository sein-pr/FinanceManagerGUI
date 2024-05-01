import csv
import os

class FinanceManager:
    def get_transactions(self, month):
        transactions = []
        file_path = os.path.join(r'C:\Users\Prince Sein\Documents\Python Dev\automations\csv manipulation\test files', f'transactions_{month}.csv')
        try:
            with open(file_path, mode='r') as csv_file:
                csv_reader = csv.reader(csv_file)
                header = next(csv_reader)
                for row in csv_reader:
                    date = row[0]
                    name = row[1]
                    amount = float(row[2])
                    category = row[3]
                    transaction_month = date.split('-')[1]
                    if transaction_month == month:
                        transaction = (date, name, amount, category)
                        transactions.append(transaction)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except Exception as e:
            print(f"Error: {e}")
        return transactions
