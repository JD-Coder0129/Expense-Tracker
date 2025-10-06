import json
from datetime import datetime

FILENAME = "expensetracker.json"

def load_expenses():
    try:
        with open(FILENAME, "r") as f:
            expenses = json.load(f)
    except FileNotFoundError:
        expenses = []
    return expenses

def save_expenses(expenses):
    with open(FILENAME, "w") as f:
        json.dump(expenses, f, indent=4)

def add_expense(expenses):
    item_name = input("Enter the item: ")
    amount = int(input("Enter the amount of money: "))
    category = input("Enter the category: ")
    description = input("Enter the description: ")

    expense = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "item_name": item_name,
        "amount": amount,
        "description": description,
        "category": category
    }

    expenses.append(expense)
    save_expenses(expenses)

def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses found.")
        return
    for exp in expenses:
        print(f"{exp['item_name']} on {exp['date']} ₹{exp['amount']} [{exp['category']}] - {exp['description']}")

def search_expense(item):
    expenses = load_expenses()
    for expense in expenses:
        if expense["item_name"].lower() == item.lower():
            print(f"₹{expense['amount']} [{expense['category']}] - {expense['description']}")
            return expense
    return None

def total_expense():
    expenses = load_expenses()
    total = {}
    for exp in expenses:
        if exp["category"] in total:
            total[exp["category"]] += exp["amount"]
        else:
            total[exp["category"]] = exp["amount"]
    print(total)

def view_by_date(data):
    search_date = input("Enter date (YYYY-MM-DD): ")
    found = [exp for exp in data if exp["date"] == search_date]
    if not found:
        print("❌ No expenses found for this date.")
        return
    print(f"\nExpenses on {search_date}:")
    for exp in found:
        print(f"₹{exp['amount']} [{exp['category']}] - {exp['description']}")
def main():
    while True:
        print("============Expence Tracker==============")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Search Expense")
        print("4. Total Expenses")
        print("5. View by Date")
        print("6. Exit")
        print("=========================================")
        choice = int(input("Enter choice: "))
        if choice == 1:
            expenses = load_expenses()
            add_expense(expenses)
        elif choice == 2:
            view_expenses()
        elif choice == 3:
            item = input("Enter the item: ")
            expense = search_expense(item)
            if expense:
                print(expense)
            else:
                print("Expense not found!")
        elif choice == 4:
            print("Total Expenses: ", total_expense())
        elif choice == 5:
            view_by_date(load_expenses())
        elif choice == 6:
            break
        else:
            print("Invalid Choice!")

if __name__ == '__main__':
    main()        
