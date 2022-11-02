# Python Group Expense tracker

## Abstract

Ever wondered why Tricount and Splitwise never made a CLI version of their respectives applications ? Don't keep on waiting, do it yourself ! Today we'll be creating a CLI application allowing to track your expenses and their repartition within your friends or your family.

## Todo-list

- [X] A new expense can be added (Mandatory expense information : Amount, label, Spender)
- [X] Expense registry is stored in an external file on an appropriate format for persistency (CSV is fine, any other relevant format would be cool)
- [X] A new user can be created (Mandatory user information : Name)
- [X] Users are stored in an external file for persistency
- [X] When adding a new expense, Spender should be chosen among existing users
- [X] An expense can be divided between several existing users. By default, total amount of the expense will be evenly split between all involved users and spender should automatically be checked as involved in the expense
- [X] New mandatory expense information : People involved in the expense

- [X] A status report can be accessed from the main menu, synthesizing who owes who. Every user must appear only once in the report, so you must synthesize reimbursements.
Exemple: 3 Users :
- User1 owes 34,56€ to User2
- User2 owes nothing
- User3 owes 14,72€ to User2
- [X] Add the possibility to mark a debt as payed from the status report
- [X] Think of new ways of spliting the expense (Percentage / person, Amount / person, anything that makes sense)
- [X] User Input Validation : Throw an error if an expense amount is not a number, and so on ..
- [ ] All implemented features should have relevant test cases
    - If I just have to run your test suite to check project quality and features : Automatic bonus
- [ ] Bonus : Improve your app in any way you want : More features, fancy report, any good idea will be rewarded


## Explanations on what I implemented

- Advanded checks on input (the shares of an expense must be valid, name cannot contain special characters used during parsing, ...)
- Ways of spliting the expense: the user must specify the sum the other users owe him/her (amount/person)
- Debts and their status (paid or unpaid) is stored into the `debts.csv` file at the moment the expense is inserted

## What would I do if I had to start again?

- Use a different storage backend more flexible than CSV, like SQLite, or maybe something more fancy like a graph database (since debts can be represented with graphs!)
