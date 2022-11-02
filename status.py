from expense import get_expense_list
from user import get_user_list

user_questions = [
]


# This function computes who owes what overall and prints it
def show_status(*args):
    user_debts = {}

    # Get the last version of users to populate the dict
    users = get_user_list()
    if len(users) == 0:
        print("No user found, create one first.")
        return False
    for user in users:
        user_debts[user] = {}

    expenses = get_expense_list()

    for expense in expenses:
        amount = float(expense['amount'])
        shared = expense['shared']
        spender = expense['spender']

        # Compute the amount each user has to pay to the spender
        for user in shared:
            if spender not in user_debts[user].keys():
                user_debts[user][spender] = 0 # Initialize the user debts to the spender

            # Naive equal split
            user_debts[user][spender] += amount / len(shared)

    # Print the debts
    for user in user_debts.keys():
        if len(user_debts[user]) == 0:
            print(f"{user} owes nothing.")
            continue
        print(f"{user} owes:")
        for spender in user_debts[user].keys():
            print(f"  - {user_debts[user][spender]} euros to {spender}.")

    return True
