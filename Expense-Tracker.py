import json
from datetime import datetime

# Optional color support via colorama (cross-platform). Falls back gracefully if not installed.
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
except Exception:
    class _C:
        def __getattr__(self, name):
            return ""
    Fore = Style = _C()

FILENAME = "expensetracker.json"

# Color shortcuts
H = Fore.CYAN + Style.BRIGHT
PROMPT = Fore.BLUE + Style.BRIGHT
ERROR = Fore.RED + Style.BRIGHT
SUCCESS = Fore.GREEN + Style.BRIGHT
AMOUNT = Fore.YELLOW + Style.BRIGHT
CATEGORY = Fore.MAGENTA + Style.BRIGHT
RESET = Style.RESET_ALL

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
    item_name = input(PROMPT + "Enter the item: " + RESET)
    try:
        amount = int(input(PROMPT + "Enter the amount of money: " + RESET))
    except ValueError:
        print(ERROR + "Invalid amount. Use numbers only." + RESET)
        return
    category = input(PROMPT + "Enter the category: " + RESET)
    description = input(PROMPT + "Enter the description: " + RESET)

    expense = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "item_name": item_name,
        "amount": amount,
        "description": description,
        "category": category
    }

    expenses.append(expense)
    save_expenses(expenses)
    print(SUCCESS + "Expense added." + RESET)

def view_expenses():
    expenses = load_expenses()
    if not expenses:
        print(ERROR + "No expenses found." + RESET)
        return
    print(H + "\nAll expenses:" + RESET)
    for exp in expenses:
        print(
            f"{Fore.GREEN}{exp['item_name']}{RESET} on {Fore.CYAN}{exp['date']}{RESET} "
            f"{AMOUNT}₹{exp['amount']}{RESET} [{CATEGORY}{exp['category']}{RESET}] - {exp['description']}"
        )

def search_expense(item):
    expenses = load_expenses()
    for expense in expenses:
        if expense["item_name"].lower() == item.lower():
            print(
                f"{Fore.GREEN}{expense['item_name']}{RESET} on {Fore.CYAN}{expense['date']}{RESET} "
                f"{AMOUNT}₹{expense['amount']}{RESET} [{CATEGORY}{expense['category']}{RESET}] - {expense['description']}"
            )
            return expense
    return None

def total_expense():
    expenses = load_expenses()
    if not expenses:
        print(ERROR + "No expenses to total." + RESET)
        return
    totals = {}
    for exp in expenses:
        totals[exp["category"]] = totals.get(exp["category"], 0) + exp["amount"]
    print(H + "\nTotal by category:" + RESET)
    for cat, amt in totals.items():
        print(f"{CATEGORY}{cat}{RESET}: {AMOUNT}₹{amt}{RESET}")

def view_by_date(data):
    search_date = input(PROMPT + "Enter date (YYYY-MM-DD): " + RESET)
    found = [exp for exp in data if exp["date"] == search_date]
    if not found:
        print(ERROR + "❌ No expenses found for this date." + RESET)
        return
    print(H + f"\nExpenses on {search_date}:" + RESET)
    for exp in found:
        print(
            f"{Fore.GREEN}{exp['item_name']}{RESET} - {AMOUNT}₹{exp['amount']}{RESET} [{CATEGORY}{exp['category']}{RESET}] - {exp['description']}"
        )

def main():
    while True:
        print(H + "============ Expense Tracker =============" + RESET)
        print(PROMPT + "1. Add Expense" + RESET)
        print(PROMPT + "2. View Expenses" + RESET)
        print(PROMPT + "3. Search Expense" + RESET)
        print(PROMPT + "4. Total Expenses" + RESET)
        print(PROMPT + "5. View by Date" + RESET)
        print(PROMPT + "6. Exit" + RESET)
        print(H + "=========================================" + RESET)
        try:
            choice = int(input(PROMPT + "Enter choice: " + RESET))
        except ValueError:
            print(ERROR + "Invalid input. Enter a number between 1 and 6." + RESET)
            continue

        if choice == 1:
            expenses = load_expenses()
            add_expense(expenses)
        elif choice == 2:
            view_expenses()
        elif choice == 3:
            item = input(PROMPT + "Enter the item: " + RESET)
            expense = search_expense(item)
            if not expense:
                print(ERROR + "Expense not found!" + RESET)
        elif choice == 4:
            total_expense()
        elif choice == 5:
            view_by_date(load_expenses())
        elif choice == 6:
            print(SUCCESS + "Goodbye." + RESET)
            break
        else:
            print(ERROR + "Invalid Choice!" + RESET)

if __name__ == '__main__':
    main()
