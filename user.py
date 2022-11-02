from PyInquirer import prompt
from prompt_toolkit.validation import Validator, ValidationError
import csv

class ValidateUsername(Validator):
    def validate(self, document):
        if document.text in get_user_list():
            raise ValidationError(
                message='Username already exists',
                cursor_position=len(document.text)) # Move cursor to end
        elif len(document.text) == 0:
            raise ValidationError(
                message='Username must not be empty',
                cursor_position=len(document.text))
        elif document.text.contains("|") or document.text.contains(",") or document.text.contains(";"):
            raise ValidationError(
                message='Username must not contain special characters',
                cursor_position=len(document.text))

user_questions = [
    {
        "type":"input",
        "name":"name",
        "message":"New User - Name:",
        "validate": ValidateUsername,
    },
]

# Return the list of spender usernames
def get_user_list():
    result = []
    with open('data/users.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            result.append(row[0])
    return result


def save_user_to_csv(user):
    with open('data/users.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([user['name']])


# This function creates a new user, asking for its name
def add_user(*args):
    user = prompt(user_questions)
    save_user_to_csv(user)
    print("User Added !")
    return True
