import csv

def get_debts():
    with open('data/debts.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            yield {
                'from': row[0],
                'to': row[1],
                'amount': float(row[2]),
                'paid': row[3] == 'True'
            }

# Compute the debt for each user and add it to the DB
def add_debts_from_expense(expense, shares):
    with open('data/debts.csv', 'a', newline='') as f:
        writer = csv.writer(f)

        for user in expense['shared']:
            debt = float(shares[user])
            writer.writerow([user, expense['spender'], debt, False])
