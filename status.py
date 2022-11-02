from PyInquirer import prompt

from debt import get_debts
from user import get_user_list

user_questions = [
]

def is_not_owing(debts, user):
    for spender in debts[user].keys():
        if debts[user][spender] > 0:
            return False
    return True

# This function computes who owes what overall and prints it
def show_status(*args):
    raw_debts = get_debts()
    user_debts = {}

    # Get the last version of users to populate the dict
    users = get_user_list()
    if len(users) == 0:
        print("No user found, create one first.")
        return False
    for user in users:
        user_debts[user] = {}

    # Compute debts for each user
    for debt in raw_debts:
        if not debt['to'] in user_debts[debt['from']]:
            user_debts[debt['from']][debt['to']] = 0
        if not debt['from'] in user_debts[debt['to']]:
            user_debts[debt['to']][debt['from']] = 0

        if not debt['paid']:
            user_debts[debt['from']][debt['to']] += debt['amount']
            user_debts[debt['to']][debt['from']] -= debt['amount']

    # Print the debts
    print("Current status of expenses:")
    for user in user_debts.keys():
        if is_not_owing(user_debts, user):
            print(f"{user} owes nothing.")
            continue
        print(f"{user} owes:")
        for spender in user_debts[user].keys():
            if (user_debts[user][spender] > 0):
                print(f"  - {user_debts[user][spender]} euros to {spender}.")

    print()
    paid = prompt([
        {
            "type": "checkbox",
            "name": "paid",
            "message": "Mark as paid?",
            "choices": [{"name": "Not implemented"}],
        }
    ])

    return True
