from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError
import csv

from debt import add_debts_from_expense
from user import get_user_list

class NumberValidator(Validator):
    def validate(self, document):
        try:
            float(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end


expense_questions = [
    {
        "type":"input",
        "name":"amount",
        "message":"New Expense - Amount:",
        "validate": NumberValidator,
    },
    {
        "type":"input",
        "name":"label",
        "message":"New Expense - Label:",
    },
    {
        "type":"list",
        "name":"spender",
        "message":"Choose a spender:",
        "choices": [], # computed for each invocation
    },
    {
        "type":"checkbox",
        "name":"shared",
        "message":"Expense shared with:",
        "choices": [], # computed for each invocation
        "validate": lambda answer: 'You must choose at least one shared user.' \
            if len(answer) == 0 else True
    }
]


def check_sum(expense, shares):
    total = 0
    for user in shares:
        total += float(shares[user])
    return total <= float(expense['amount'])


def get_expense_list():
    def parse_shared(shared):
        return shared.split("|")

    with open('data/expense_report.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            yield {
                'amount': row[0],
                'label': row[1],
                'spender': row[2],
                'shared': parse_shared(row[3])
            }


def save_expense_to_csv(expense, shares):
    with open('data/expense_report.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        shares_to_shared = []
        for user in expense['shared']:
            shares_to_shared.append(user + ";" + shares[user])
        shared = "|".join(shares_to_shared)
        writer.writerow([expense['amount'], expense['label'], expense['spender'], shared])


# This function creates a new expense
def new_expense(*args):
    # Get the last version of users
    users = get_user_list()
    if len(users) == 0:
        print("No user found, create one first.")
        return False

    expense_questions[2]['choices'] = users

    # Build spenders checkbox
    expense_questions[3]['choices'].clear()
    for user in users:
        expense_questions[3]['choices'].append({'name': user})

    expense = prompt(expense_questions)

    # Check if the spender is in the shared list
    if expense['spender'] in expense['shared']:
        print("You can't share with yourself.")
        return False

    shares_questions = []
    for user in expense['shared']:
        shares_questions.append({
            "type":"input",
            "name": user,
            "message":"How much do " + user + " owes?",
            "validate": NumberValidator,
        })

    shares = prompt(shares_questions)
    if not check_sum(expense, shares):
        print("The sum of shares is greater than the expense amount.")
        return False

    save_expense_to_csv(expense, shares)
    add_debts_from_expense(expense, shares)
    print("Expense Added !")
    return True
