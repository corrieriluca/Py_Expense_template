from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError
import csv

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


def get_expense_list():
    def parse_shared(shared):
        return shared.split("|")

    with open('expense_report.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            yield {
                'amount': row[0],
                'label': row[1],
                'spender': row[2],
                'shared': parse_shared(row[3])
            }


def save_expense_to_csv(expense):
    with open('expense_report.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        shared = "|".join(expense['shared'])
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

    save_expense_to_csv(expense)
    print("Expense Added !")
    return True
