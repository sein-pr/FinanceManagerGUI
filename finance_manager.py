import csv

class FinanceManager:
    def get_transactions(self, month):
        transactions = []
        file_placeholder = f'C:\\Users\\Prince Sein\\Documents\\Python Dev\\automations\\csv manipulation\\test files\\transactions_{month}.csv'
        with open(file_placeholder, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)
            for row in csv_reader:
                date = row[0]
                name = row[4]
                amount = float(row[5])
                transaction_month = date.split('-')[1]
                if transaction_month == month:
                    transaction = (date, name, amount)
                    transactions.append(transaction)
        return transactions
