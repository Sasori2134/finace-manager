from PyQt5.QtWidgets import QWidget
from budget.budgetframe import BudgetFrame



class Budget(QWidget):
    def __init__(self,spent,budget,label,status,item_data,remove_callback):
        super().__init__()
        self.ui = BudgetFrame()
        self.ui.setupUi(self)

        if label == "food and dining":
            self.ui.label.setStyleSheet("font-size:13pt")
        self.ui.label.setText(label.capitalize())
        self.ui.progressbar.setMinimum(0)
        self.ui.progressbar.setMaximum(budget)
        self.ui.progressbar.setValue(min(spent,budget))
        if status == "You Are Over Budget":
            self.ui.budget.setStyleSheet("color:rgb(170, 0, 0)")
            self.ui.status.setText(f"{status}")
        elif status == "You Are Under Budget":
            self.ui.status.setText("You Are Under Budget")
        else:
            self.ui.status.setText(f"{status}₾")
        self.ui.budget.setText(f"Budget: ₾{budget}")
        self.ui.spent.setText(f"Spent: ₾{spent}")

        self.item_data = item_data
        self.remove_callback = remove_callback

        self.ui.remove_budget.clicked.connect(self.handle_remove)

    def handle_remove(self):
        self.remove_callback(self.item_data['pk'], self)
        