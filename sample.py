print("Hello")
import json
from datetime import datetime
from collections import defaultdict
import os


# -------------------------
# Model
# -------------------------
class Expense:
    def __init__(self, amount, category, description, date=None):
        self.amount = float(amount)
        self.category = category
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }

    @staticmethod
    def from_dict(data):
        return Expense(
            data["amount"],
            data["category"],
            data["description"],
            data["date"]
        )


# -------------------------
# Core Logic
# -------------------------
class FinanceManager:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = []
        self.load_data()1

    def add_expense(self, expense):
        self.expenses.append(expense)
        self.save_data()

    def save_data(self):
        with open(self.filename, "w") as f:
            json.dump([e.to_dict() for e in self.expenses], f, indent=4)

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.expenses = [Expense.from_dict(e) for e in data]

    def get_total_spent(self):
        return sum(e.amount for e in self.expenses)

    def expenses_by_category(self):
        summary = defaultdict(float)
        for e in self.expenses:
            summary[e.category] += e.amount
        return summary

    def expenses_by_month(self):
        summary = defaultdict(float)
        for e in self.expenses:
            month = e.date[:7]  # YYYY-MM
            summary[month] += e.amount
        return summary

    def list_expenses(self):
        return self.expenses


# -------------------------
# CLI Interface
# -------------------------
class CLI:
    def __init__(self):
        self.manager = FinanceManager()

    def run(self):
        while True:
            self.show_menu()
            choice = input("Choose an option: ")

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_expenses()
            elif choice == "3":
                self.show_reports()
            elif choice == "4":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice")

    def show_menu(self):
        print("\n📊 Personal Finance Manager")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Reports & Analysis")
        print("4. Exit")

    def add_expense(self):
        amount = input("Amount: ")
        category = input("Category (Food, Rent, Transport, etc.): ")
        description = input("Description: ")
        date = input("Date (YYYY-MM-DD, leave blank for today): ")

        expense = Expense(amount, category, description, date if date else None)
        self.manager.add_expense(expense)
        print("✅ Expense added successfully")

    def view_expenses(self):
        expenses = self.manager.list_expenses()
        if not expenses:
            print("No expenses recorded.")
            return

        print("\n📋 Expenses:")
        for i, e in enumerate(expenses, 1):
            print(f"{i}. {e.date} | {e.category} | ${e.amount:.2f} | {e.description}")

        print(f"\n💰 Total Spent: ${self.manager.get_total_spent():.2f}")

    def show_reports(self):
        print("\n📈 Reports")
        print("1. Spending by Category")
        print("2. Spending by Month")

        choice = input("Choose report: ")

        if choice == "1":
            self.report_by_category()
        elif choice == "2":
            self.report_by_month()
        else:
            print("❌ Invalid option")

    def report_by_category(self):
        data = self.manager.expenses_by_category()
        print("\n📂 Spending by Category:")
        for category, amount in data.items():
            print(f"{category}: ${amount:.2f}")

    def report_by_month(self):
        data = self.manager.expenses_by_month()
        print("\n🗓️ Spending by Month:")
        for month, amount in sorted(data.items()):
            print(f"{month}: ${amount:.2f}")


# -------------------------
# Entry Point
# -------------------------
if __name__ == "__main__":
    app = CLI()
    app.run()
from expense import Expense
from storage import load_expenses, save_expense, backup_data, restore_data
from reports import generate_report
from utils import get_input, validate_amount, validate_date

def add_expense():
    amount = get_input("Amount: $", validate_amount)
    category = get_input("Category: ")
    date = get_input("Date (YYYY-MM-DD): ", validate_date)
    description = get_input("Description: ")

    expense = Expense(amount, category, date, description)
    save_expense(expense)
    print("✅ Expense added successfully!")

def main_menu():
    while True:
        print("\n💰 Personal Finance Manager")
        print("1. Add Expense")
        print("2. View Report")
        print("3. Backup Data")
        print("4. Restore Data")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            expenses = load_expenses()
            generate_report(expenses)
        elif choice == "3":
            backup_data()
            print("📦 Backup completed.")
        elif choice == "4":
            restore_data()
            print("♻️ Data restored from backup.")
        elif choice == "5":
            print("Goodbye 👋")
            break
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main_menu()
