from PyInquirer import prompt
import csv

user_questions = [
    {
        "type":"input",
        "name":"name",
        "message":"New User - Name:",
    },
]

# Return the list of spender usernames
def get_user_list():
    result = []
    with open('users.csv', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            result.append(row[0])
    return result


def save_user_to_csv(user):
    with open('users.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([user['name']])


# This function creates a new user, asking for its name
def add_user(*args):
    user = prompt(user_questions)
    save_user_to_csv(user)
    print("User Added !")
    return True
